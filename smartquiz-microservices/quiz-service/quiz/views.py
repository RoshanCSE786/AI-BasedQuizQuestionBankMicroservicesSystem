import uuid
import requests
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .redis_client import redis_client
import redis
import json

from .models import QuizAttempt

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generate_quiz(request):

    # 🔹 Extract user's token
    auth_header = request.headers.get("Authorization")

    # 🔹 Call Question Service with same token
    response = requests.get(
        settings.QUESTION_SERVICE_URL,
        headers={"Authorization": auth_header}
    )

    if response.status_code != 200:
        return Response(
            {"error": "Failed to fetch questions"},
            status=response.status_code
        )

    questions = response.json()

    import uuid
    quiz_id = str(uuid.uuid4())

    correct_answers = {}

    for q in questions:
        correct_answers[str(q["id"])] = q["correct_answer"]
        del q["correct_answer"]

    from .redis_client import redis_client

    redis_client.setex(
        f"quiz:{quiz_id}",
        600,
        json.dumps(correct_answers)
    )

    return Response({
        "quiz_id": quiz_id,
        "questions": questions
    })

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def submit_quiz(request):
    quiz_id = request.data.get("quiz_id")
    user_answers = request.data.get("answers")

    if not quiz_id or not user_answers:
        return Response({"error": "quiz_id and answers required"}, status=400)

    # Connect to Redis
    r = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=0
    )

    key = f"quiz:{quiz_id}"
    correct_answers_json = r.get(key)

    if not correct_answers_json:
        return Response({"error": "Quiz not found or expired"}, status=404)

    correct_answers = json.loads(correct_answers_json)

    score = 0
    total = len(correct_answers)

    for question_id, correct_answer in correct_answers.items():
        if user_answers.get(str(question_id)) == correct_answer:
            score += 1

    # Optional: delete quiz after submission
    r.delete(key)

    return Response({
        "quiz_id": quiz_id,
        "score": score,
        "total": total
    })
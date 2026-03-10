import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["POST"])
def analyze_user(request):

    user_id = request.user.id

    if not user_id:
        return Response({"error": "user_id required"}, status=400)

    # Call result-service
    response = requests.get(
        f"{settings.RESULT_SERVICE_URL}?user_id={user_id}"
    )

    if response.status_code != 200:
        return Response({"error": "Failed to fetch results"}, status=500)

    results = response.json()

    if not results:
        return Response({
            "message": "No quiz attempts found"
        })

    total_score = sum(r["score"] for r in results)
    total_questions = sum(r["total"] for r in results)

    attempts = len(results)

    average = (total_score / total_questions) * 100

    if average >= 80:
        performance = "Excellent"
        recommendation = "Try hard difficulty quizzes"

    elif average >= 50:
        performance = "Good"
        recommendation = "Practice medium questions"

    else:
        performance = "Needs Improvement"
        recommendation = "Focus on basics"

    return Response({
        "user_id": user_id,
        "attempts": attempts,
        "average_score": round(average, 2),
        "performance": performance,
        "recommendation": recommendation
    })

@api_view(["GET"])
def recommend_difficulty(request):

    user_id = request.query_params.get("user_id")

    if not user_id:
        return Response({"error": "user_id required"}, status=400)

    # Call result-service
    response = requests.get(
        f"{settings.RESULT_SERVICE_URL}?user_id={user_id}"
    )

    if response.status_code != 200:
        return Response({"error": "Result service unavailable"}, status=500)

    results = response.json()

    if not results:
        return Response({
            "message": "User has no quiz attempts yet"
        })

    total_score = sum(r["score"] for r in results)
    total_questions = sum(r["total"] for r in results)

    average = (total_score / total_questions) * 100

    if average >= 80:
        difficulty = "hard"
    elif average >= 50:
        difficulty = "medium"
    else:
        difficulty = "easy"

    return Response({
        "user_id": user_id,
        "recommended_difficulty": difficulty,
        "average_score": round(average, 2)
    })
@api_view(["GET"])
def user_insights(request):

    user_id = request.query_params.get("user_id")

    if not user_id:
        return Response({"error": "user_id required"}, status=400)

    response = requests.get(
        f"{settings.RESULT_SERVICE_URL}?user_id={user_id}"
    )

    if response.status_code != 200:
        return Response({"error": "Result service unavailable"}, status=500)

    results = response.json()

    if not results:
        return Response({
            "message": "User has not attempted any quizzes"
        })

    attempts = len(results)

    total_score = sum(r["score"] for r in results)
    total_questions = sum(r["total"] for r in results)

    average = (total_score / total_questions) * 100

    # Determine insights
    if average >= 80:
        strength = "High accuracy"
    elif average >= 50:
        strength = "Moderate performance"
    else:
        strength = "Needs improvement"

    if attempts < 3:
        weakness = "Low practice frequency"
        suggestion = "Attempt quizzes more frequently"
    else:
        weakness = "Performance consistency"
        suggestion = "Focus on improving accuracy"

    return Response({
        "user_id": user_id,
        "attempts": attempts,
        "average_score": round(average,2),
        "strength": strength,
        "weakness": weakness,
        "suggestion": suggestion
    })
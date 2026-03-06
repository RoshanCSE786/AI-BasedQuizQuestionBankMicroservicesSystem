from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import QuizResult
from .serializers import QuizResultSerializer
from django.db.models import Sum, Count

# ✅ POST + GET (All Results)
@api_view(["GET", "POST"])
def results_list(request):

    # 🔹 GET → return all results
    if request.method == "GET":
        results = QuizResult.objects.all()
        serializer = QuizResultSerializer(results, many=True)
        return Response(serializer.data)

    # 🔹 POST → create new result
    if request.method == "POST":
        serializer = QuizResultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ GET → Only Specific User Results
@api_view(["GET"])
def my_results(request):
    user_id = request.query_params.get("user_id")

    if not user_id:
        return Response({"error": "user_id required"}, status=400)

    results = QuizResult.objects.filter(user_id=user_id)
    serializer = QuizResultSerializer(results, many=True)
    return Response(serializer.data)

# ✅ GET → Leaderboard
@api_view(["GET"])
def leaderboard(request):

    leaderboard_data = (
        QuizResult.objects
        .values("username")
        .annotate(
            total_score=Sum("score"),
            attempts=Count("id")
        )
        .order_by("-total_score")[:10]
    )

    return Response(leaderboard_data)
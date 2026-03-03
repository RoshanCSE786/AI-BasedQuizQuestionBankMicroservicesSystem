from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Question
from .serializers import QuestionSerializer
from .permissions import IsAdminRole

from .models import Category
from .serializers import CategorySerializer

from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import QuerySet
import random

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_permissions(self):
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            permission_classes = [IsAdminRole]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]
    
    def get_serializer_context(self):
        return {"request": self.request}

    @action(detail=False, methods=["get"], url_path="quiz")
    def generate_quiz(self, request):

        category = request.query_params.get("category")
        difficulty = request.query_params.get("difficulty")
        limit = request.query_params.get("limit")

        queryset = self.get_queryset()

        if category:
            queryset = queryset.filter(category_id=category)

        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)

        if limit:
            try:
                limit = int(limit)
            except ValueError:
                return Response({"error": "Limit must be an integer"}, status=400)
        else:
            limit = 5

        questions_list = list(queryset)
        random.shuffle(questions_list)
        selected_questions = questions_list[:limit]

        serializer = self.get_serializer(selected_questions, many=True)
        return Response(serializer.data)

    
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            permission_classes = [IsAdminRole]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]
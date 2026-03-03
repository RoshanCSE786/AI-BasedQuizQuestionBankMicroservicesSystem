from rest_framework import serializers
from .models import Question, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"
    
    def to_representation(self, instance):
        data = super().to_representation(instance)

        request = self.context.get("request")

        if request and hasattr(request, "user"):
            if request.user.role != "admin":
                data.pop("correct_answer", None)

        return data
from django.urls import path
from .views import analyze_user, recommend_difficulty, user_insights

urlpatterns = [
    path("analyze/", analyze_user),
    path("recommend/", recommend_difficulty),
    path("insights/", user_insights),
]
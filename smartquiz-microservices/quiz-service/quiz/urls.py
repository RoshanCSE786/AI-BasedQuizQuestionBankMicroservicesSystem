from django.urls import path
from .views import generate_quiz, submit_quiz

urlpatterns = [
    path("generate/", generate_quiz),
    path("submit/", submit_quiz),
]
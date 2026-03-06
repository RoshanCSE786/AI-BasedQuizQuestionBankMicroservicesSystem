from django.urls import path
from .views import results_list, my_results, leaderboard

urlpatterns = [
    path("", results_list, name="results-list"),
    path("my/", my_results, name="my-results"),
    path("leaderboard/", leaderboard, name="leaderboard"),
]
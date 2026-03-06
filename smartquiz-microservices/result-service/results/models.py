from django.db import models

class QuizResult(models.Model):
    user_id = models.IntegerField()
    username = models.CharField(max_length=150)

    quiz_id = models.CharField(max_length=100)

    score = models.IntegerField()
    total = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.score}/{self.total}"
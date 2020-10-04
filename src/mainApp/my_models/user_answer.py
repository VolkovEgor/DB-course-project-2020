from django.db import models
from .word import Word
from .exercise import Exercise


class UserAnswer(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='user_answer')
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='user_answer')
    answer = models.CharField(max_length=50, verbose_name='Ответ')


from django.db import models
from flashcard.models import Flashcard
# Create your models here.


class MultipleChoice(Flashcard):
    pass


class Solution(models.Model):
    answer = models.TextField()
    solution = models.BooleanField()
    multiple_choice = models.ForeignKey("multiple_choices.MultipleChoice", null=False, on_delete=models.CASCADE)

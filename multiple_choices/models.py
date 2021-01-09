from django.db import models
from django.db.transaction import atomic

from flashcard.abstract_models import AbstractFlashcard
from django.db.models.signals import post_save
from flashcard.models import create_flashcard
from django.contrib.auth import get_user_model
User = get_user_model()


class MultipleChoice(AbstractFlashcard):
    pass


class Solution(models.Model):
    answer = models.TextField()
    solution = models.BooleanField()
    multiple_choice = models.ForeignKey("multiple_choices.MultipleChoice", null=False, on_delete=models.CASCADE)


class MultipleChoiceSolutionAnswer(models.Model):
    answer = models.BooleanField()
    solution = models.ForeignKey(Solution, blank=False, null=True, on_delete=models.CASCADE)


post_save.connect(create_flashcard, sender=MultipleChoice)

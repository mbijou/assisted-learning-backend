from django.db import models
from flashcard.abstract_models import AbstractFlashcard
from django.db.models.signals import post_save
from flashcard.models import create_flashcard


class MultipleChoice(AbstractFlashcard):
    pass


class Solution(models.Model):
    answer = models.TextField()
    solution = models.BooleanField()
    multiple_choice = models.ForeignKey("multiple_choices.MultipleChoice", null=False, on_delete=models.CASCADE)


post_save.connect(create_flashcard, sender=MultipleChoice)

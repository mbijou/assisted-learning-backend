from django.db import models
from django.db.models.signals import post_save
from flashcard.abstract_models import AbstractFlashcard
from flashcard.models import create_flashcard


class SingleChoice(AbstractFlashcard):
    solution = models.BooleanField()


class SingleChoiceAnswer(models.Model):
    answer = models.BooleanField()
    single_choice = models.ForeignKey("single_choices.SingleChoice", null=True, blank=False, on_delete=models.CASCADE)


post_save.connect(create_flashcard, sender=SingleChoice)


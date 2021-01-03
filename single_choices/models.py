from django.db import models
from django.db.models.signals import post_save
from flashcard.abstract_models import AbstractFlashcard
from flashcard.models import create_flashcard


class SingleChoice(AbstractFlashcard):
    solution = models.BooleanField()


post_save.connect(create_flashcard, sender=SingleChoice)


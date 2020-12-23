from django.db import models
from flashcard.models import Flashcard
# Create your models here.


class SingleChoice(Flashcard):
    solution = models.BooleanField()

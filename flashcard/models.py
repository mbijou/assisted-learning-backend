from django.db import models

# Create your models here.


class Flashcard(models.Model):
    class Meta:
        abstract = True

    question = models.TextField()
    workload = models.IntegerField()
    deadline = models.DateField()


class SingleChoice(Flashcard):
    solution = models.BooleanField()


class MultipleChoice(Flashcard):
    pass


class Solution(models.Model):
    solution = models.BooleanField()
    multiple_choice = models.ForeignKey()

from django.db import models

# Create your models here.


class Flashcard(models.Model):
    class Meta:
        abstract = True

    question = models.TextField()
    workload = models.IntegerField()
    deadline = models.DateField()

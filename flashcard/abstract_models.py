from django.db import models


class AbstractFlashcard(models.Model):
    class Meta:
        abstract = True

    question = models.TextField()
    workload = models.IntegerField()
    deadline = models.DateField()
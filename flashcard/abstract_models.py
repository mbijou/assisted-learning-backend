from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class AbstractFlashcard(models.Model):
    class Meta:
        abstract = True

    question = models.TextField()
    workload = models.IntegerField()
    deadline = models.DateField()
    user = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE)

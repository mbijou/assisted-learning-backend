from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
User = get_user_model()


def get_status(instance):
    deadline = instance.deadline
    today = now()

    if instance.workload == 0:
        return "DONE"
    elif deadline > today.date() and instance.workload > 0:
        return "OPEN"
    else:
        return "FAILED"


class AbstractFlashcard(models.Model):
    class Meta:
        abstract = True

    question = models.TextField()
    workload = models.IntegerField()
    deadline = models.DateField()
    user = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE)

    @property
    def status(self):
        return get_status(self)

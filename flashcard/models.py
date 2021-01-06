from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import F, Max

from flashcard.abstract_models import AbstractFlashcard
from django.contrib.auth import get_user_model
User = get_user_model()


class Flashcard(AbstractFlashcard):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    rank = models.IntegerField(null=True, blank=False, default=1)

    def __str__(self):
        return f"{self.question}"

    def set_initial_rank(self):
        max_rank_aggregate = Flashcard.objects.filter(user=self.user).aggregate(max_rank=Max("rank"))
        if max_rank_aggregate.get("max_rank") is None or max_rank_aggregate.get("max_rank") <= 0:
            max_rank = 1
        else:
            max_rank = max_rank_aggregate.get("max_rank") + 1

        self.rank = max_rank

    @classmethod
    def update_ranks(cls, multiple_choice_id, content_type_model):
        flashcard = cls.objects.get(content_type__model=content_type_model, object_id=multiple_choice_id)
        user = flashcard.user
        flashcard.rank = Flashcard.objects.filter(user=user).aggregate(max_rank=Max("rank")).get("max_rank")
        flashcard.save()
        print("RANK ", flashcard.rank)
        print("askdosa", Flashcard.objects.get(id=flashcard.id).rank)
        Flashcard.objects.filter(user=user).exclude(id=flashcard.id, rank__gt=1).update(rank=F("rank") - 1)


def create_flashcard(sender, instance, created, **kwargs):
    content_type = ContentType.objects.get_for_model(instance)
    try:
        flashcard = Flashcard.objects.get(content_type=content_type, object_id=instance.id)
    except Flashcard.DoesNotExist:
        flashcard = Flashcard(content_type=content_type, object_id=instance.id)
        flashcard.user = instance.user
        flashcard.set_initial_rank()
    flashcard.question = instance.question
    flashcard.workload = instance.workload
    flashcard.deadline = instance.deadline
    flashcard.user = instance.user
    flashcard.save()




















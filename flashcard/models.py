from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from flashcard.abstract_models import AbstractFlashcard


class Flashcard(AbstractFlashcard):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.question}"


def create_flashcard(sender, instance, created, **kwargs):
    content_type = ContentType.objects.get_for_model(instance)
    try:
        flashcard = Flashcard.objects.get(content_type=content_type, object_id=instance.id)
    except Flashcard.DoesNotExist:
        flashcard = Flashcard(content_type=content_type, object_id=instance.id)
    flashcard.question = instance.question
    flashcard.workload = instance.workload
    flashcard.deadline = instance.deadline
    flashcard.save()

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.db.transaction import atomic
from flashcard.abstract_models import AbstractFlashcard
from flashcard.models import create_flashcard, delete_flashcard


class SingleChoice(AbstractFlashcard):
    solution = models.BooleanField()


class SingleChoiceAnswer(models.Model):
    answer = models.BooleanField()
    single_choice = models.ForeignKey("single_choices.SingleChoice", null=True, blank=False, on_delete=models.CASCADE)

    @atomic
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.single_choice.workload -= 1
        self.single_choice.save()
        return super().save(force_insert=force_insert, force_update=force_update, using=using,
                            update_fields=update_fields)


post_save.connect(create_flashcard, sender=SingleChoice)
post_delete.connect(delete_flashcard, sender=SingleChoice)


from rest_framework.serializers import ModelSerializer
from django.utils.timezone import now
from flashcard.models import Flashcard
from single_choices.models import SingleChoice, SingleChoiceAnswer
from django.db.transaction import atomic
from rest_framework.validators import ValidationError


class SingleChoiceSerializer(ModelSerializer):
    class Meta:
        model = SingleChoice
        fields = ('id', 'question', 'workload', 'deadline', 'solution',  "user", )


class SingleChoiceAnswerSerializer(ModelSerializer):
    class Meta:
        model = SingleChoiceAnswer
        fields = ("id", "answer", )

    @atomic
    def create(self, validated_data):
        single_choice_id = self.context.get("single_choice_id")
        instance = SingleChoiceAnswer.objects.create(single_choice_id=single_choice_id, **validated_data)

        Flashcard.update_ranks(single_choice_id, "singlechoice")

        return instance

    def validate(self, attrs):
        single_choice_id = self.context.get("single_choice_id")
        single_choice = SingleChoice.objects.get(pk=single_choice_id)
        deadline = single_choice.deadline
        today = now().date()
        if deadline < today:
            raise ValidationError("Flashcard expired! Please change the deadline in order to solve the task.")
        elif single_choice.status == "DONE":
            raise ValidationError("Flashcard DONE! Please set a new workload in order to solve the task again.")
        return super().validate(attrs)

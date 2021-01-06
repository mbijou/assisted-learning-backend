from rest_framework.serializers import ModelSerializer

from flashcard.models import Flashcard
from single_choices.models import SingleChoice, SingleChoiceAnswer
from django.db.transaction import atomic


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

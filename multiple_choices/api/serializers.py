from rest_framework.serializers import ModelSerializer
from multiple_choices.models import MultipleChoice


class MultipleChoiceSerializer(ModelSerializer):
    class Meta:
        model = MultipleChoice
        fields = ("id", "question", "workload", "deadline",)

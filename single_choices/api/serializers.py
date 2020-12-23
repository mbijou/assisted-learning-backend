from rest_framework.serializers import ModelSerializer

from single_choices.models import SingleChoice


class SingleChoiceSerializer(ModelSerializer):
    class Meta:
        model = SingleChoice
        fields = ('id', 'question', 'workload', 'deadline', 'solution',)

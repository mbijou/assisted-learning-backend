from rest_framework import serializers
from multiple_choices.models import MultipleChoice, Solution


class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = ('id', "answer", "solution", )


class MultipleChoiceSerializer(serializers.ModelSerializer):
    solution_set = SolutionSerializer(many=True)

    class Meta:
        model = MultipleChoice
        fields = ("id", "question", "workload", "deadline", "solution_set",)


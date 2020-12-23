from rest_framework import serializers
from multiple_choices.models import MultipleChoice, Solution
from django.db.transaction import atomic


class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = ('id', "answer", "solution", )
        extra_kwargs = {'id': {'read_only': False}}


class MultipleChoiceSerializer(serializers.ModelSerializer):
    solution_set = SolutionSerializer(many=True)

    class Meta:
        model = MultipleChoice
        fields = ("id", "question", "workload", "deadline", "solution_set",)

    @atomic
    def create(self, validated_data):
        solution_set = validated_data.pop("solution_set")
        multiple_choice = MultipleChoice.objects.create(**validated_data)
        for solution in solution_set:
            Solution.objects.create(multiple_choice=multiple_choice, **solution)
        return multiple_choice

    @atomic
    def update(self, instance, validated_data):
        solution_set = validated_data.pop("solution_set")

        instance = MultipleChoice(pk=instance.pk, **validated_data)
        instance.save()

        for solution in solution_set:
            solution_id = solution.get("id")
            solution_instance = Solution.objects.get(id=solution_id)

            if solution_instance.multiple_choice == instance:
                Solution(pk=solution_id, multiple_choice=instance, **solution).save()
        return instance

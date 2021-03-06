from rest_framework import serializers
from multiple_choices.models import MultipleChoice, Solution, MultipleChoiceSolutionAnswer
from django.db.transaction import atomic
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404


class SolutionSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get("context").get("id_read_only") is False:
            self.fields.get("id").read_only = False
        elif kwargs.get("context").get("id_read_only") is True:
            self.fields.get("id").read_only = True

    class Meta:
        model = Solution
        fields = ('id', "answer", "solution",)
        # Bei CREATE -> 'read_only' : True, Bei Update -> 'read_only' : False
        # extra_kwargs = {'id': {'read_only': False}}


class MultipleChoiceSerializer(serializers.ModelSerializer):
    solution_set = SolutionSerializer(many=True, context={"id_read_only": True})

    class Meta:
        model = MultipleChoice
        fields = ("id", "question", "workload", "deadline", "solution_set", "user", )

    @atomic
    def create(self, validated_data):
        solution_set = validated_data.pop("solution_set")
        multiple_choice = MultipleChoice.objects.create(**validated_data)

        for solution in solution_set:
            Solution.objects.create(multiple_choice=multiple_choice, **solution)

        return multiple_choice


class MultipleChoiceUpdateSerializer(serializers.ModelSerializer):
    solution_set = SolutionSerializer(many=True, context={"id_read_only": False})

    class Meta:
        model = MultipleChoice
        fields = ("id", "question", "workload", "deadline", "solution_set", "user", )

    def validate(self, attrs):
        for solution_dict in attrs.get("solution_set"):
            solution = Solution.objects.get(pk=solution_dict.get("id"))
            if solution.multiple_choice.id != int(self.context.get("pk")):
                raise ValidationError("Solution must be of the same Multiple Choice")
        return super().validate(attrs)

    @atomic
    def update(self, instance, validated_data):
        solution_set = validated_data.pop("solution_set")

        instance = get_object_or_404(MultipleChoice, pk=instance.pk)
        instance.__dict__.update(validated_data)
        instance.save()

        for solution in solution_set:
            solution_id = solution.get("id")
            solution_instance = Solution.objects.get(id=solution_id)

            if solution_instance.multiple_choice == instance:
                Solution(pk=solution_id, multiple_choice=instance, **solution).save()
        return instance


class MultipleChoiceSolutionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleChoiceSolutionAnswer
        fields = ("id", "solution", "answer", )

    def validate(self, attrs):
        solution = attrs.get("solution")
        if solution.multiple_choice.id != self.context.get("multiple_choice_id"):
            raise ValidationError("Answers solution must be of the same Multiple Choice")
        return super().validate(attrs)

    @atomic
    def create(self, validated_data):
        self.instance = MultipleChoiceSolutionAnswer.objects.create(**validated_data)
        return self.instance


class MultipleChoiceSolutionAnswerSetSerializer(serializers.ModelSerializer):
    multiplechoicesolutionanswer_set = MultipleChoiceSolutionAnswerSerializer(many=True, write_only=True)

    class Meta:
        model = MultipleChoiceSolutionAnswer
        fields = ("id", "solution", "answer", "multiplechoicesolutionanswer_set", )

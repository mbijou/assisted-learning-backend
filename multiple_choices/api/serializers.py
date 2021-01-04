from rest_framework import serializers
from multiple_choices.models import MultipleChoice, Solution, MultipleChoiceSolutionAnswer
from django.db.transaction import atomic


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
        fields = ("id", "question", "workload", "deadline", "solution_set",)

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
        fields = ("id", "question", "workload", "deadline", "solution_set",)

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


class MultipleChoiceSolutionAnswerSerializer(serializers.Serializer):
    solution = serializers.IntegerField()
    answer = serializers.BooleanField()


class MultipleChoiceAnswerSerializer(serializers.ModelSerializer):
    multiplechoicesolutionanswer_set = MultipleChoiceSolutionAnswerSerializer(many=True, write_only=True)

    class Meta:
        model = MultipleChoice
        fields = ("id", "multiplechoicesolutionanswer_set")

    @atomic
    def create(self, validated_data):
        answer_set = validated_data.pop("multiplechoicesolutionanswer_set")
        user_id = self.context.get("user_id")
        multiple_choice_id = self.context.get("multiple_choice_id")
        for answer in answer_set:
            MultipleChoiceSolutionAnswer.objects.create(solution_id=answer.get("solution_id"), user_id=user_id,
                                                        answer=answer.get("answer"))
        print("asdsa", answer_set)
        self.instance = MultipleChoice.objects.get(pk=multiple_choice_id)
        return self.instance

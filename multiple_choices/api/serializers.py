from rest_framework import serializers
from multiple_choices.models import MultipleChoice, Solution
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
    def __init__(self, *args, **kwargs):

        # self.solution_set = SolutionSerializer(
        #             many=True, context={"id_read_only": False}
        #         )


        super().__init__(*args, **kwargs)

        self.solution_set.context["id_read_only"] = False

        # instance = self.instance[0]

        print("KOMMENTAR", self.instance)

        # if self.instance and self.instance.pk:
        #     self.solution_set = SolutionSerializer(
        #         many=True, context={"id_read_only": True}
        #     )





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

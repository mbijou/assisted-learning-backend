from django.db.models import Max, F
from django.db.transaction import atomic
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin, ListModelMixin
from flashcard.models import Flashcard
from multiple_choices.api.serializers import MultipleChoiceSerializer, MultipleChoiceUpdateSerializer, \
    MultipleChoiceSolutionAnswerSetSerializer, MultipleChoiceSolutionAnswerSerializer
from multiple_choices.models import MultipleChoice, MultipleChoiceSolutionAnswer
from rest_framework.response import Response
from django.utils.timezone import now
from rest_framework.validators import ValidationError


class MultipleChoiceViewSet(ModelViewSet):
    queryset = MultipleChoice.objects.all()
    serializer_class = MultipleChoiceSerializer

    def get_serializer(self, *args, **kwargs):
        context = {"pk": self.kwargs.get("pk")}
        serializer = super().get_serializer(*args, context=context, **kwargs)
        return serializer

    def get_serializer_class(self):
        if self.kwargs.get("pk"):
            return MultipleChoiceUpdateSerializer
        return super().get_serializer_class()


class MultipleChoiceAnswerViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, ListModelMixin):
    queryset = MultipleChoiceSolutionAnswer.objects.all()
    serializer_class = MultipleChoiceSolutionAnswerSetSerializer

    @atomic
    def create(self, request, *args, **kwargs):
        answer_set = request.data.get("multiplechoicesolutionanswer_set")
        multiple_choice_id = self.kwargs.get("multiple_choice_id")

        answer_serializers = self.get_answer_serializers(answer_set, multiple_choice_id)

        multiple_choice = MultipleChoice.objects.get(pk=multiple_choice_id)

        errors = self.validate_and_get_error_messages(multiple_choice, answer_serializers)

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            response_data = self.create_answers(answer_serializers)
            headers = self.get_success_headers(response_data)

            Flashcard.update_ranks(multiple_choice_id, "multiplechoice")

            multiple_choice.workload -= 1
            multiple_choice.save()

            return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    def create_answers(self, answer_serializers):
        response_data = []
        for answer_serializer in answer_serializers:
            if answer_serializer.is_valid():
                self.perform_create(answer_serializer)
                response_data.append(answer_serializer.data)
        return response_data

    @staticmethod
    def get_answer_serializers(answer_set, multiple_choice_id):
        answer_serializers = []
        for answer in answer_set:
            context = {"multiple_choice_id": multiple_choice_id}
            serializer = MultipleChoiceSolutionAnswerSerializer(data=answer, context=context)
            answer_serializers.append(serializer)
        return answer_serializers

    def validate_and_get_error_messages(self, multiple_choice, answer_serializers):
        answer_errors = {"multiplechoicesolutionanswer_set": []}
        serializer_has_errors = False
        for answer_serializer in answer_serializers:
            if answer_serializer.is_valid():
                answer_errors["multiplechoicesolutionanswer_set"].append({})
            else:
                answer_errors["multiplechoicesolutionanswer_set"].append(answer_serializer.errors)
                serializer_has_errors = True

        if serializer_has_errors is False:
            is_valid, deadline_not_expired_errors = self.validate_deadline_not_expired(multiple_choice)
            if is_valid is False:
                return deadline_not_expired_errors

        if serializer_has_errors:
            return answer_errors

    @staticmethod
    def validate_deadline_not_expired(multiple_choice):
        deadline = multiple_choice.deadline
        today = now().date()

        if deadline < today:
            error_message = {
                "non_field_errors": ["Flashcard expired! Please change the deadline in order to solve the task."]
            }
            return False, error_message
        return True, None

    def get_queryset(self):
        return MultipleChoiceSolutionAnswer.objects.filter(
            solution__multiple_choice__user_id=self.kwargs.get("user_id"),
            solution__multiple_choice__id=self.kwargs.get("multiple_choice_id")
        ).distinct()

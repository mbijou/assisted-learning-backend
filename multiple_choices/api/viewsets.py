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
        response_data = []
        answer_errors = {"multiplechoicesolutionanswer_set": []}
        serializer_has_errors = False
        for answer in answer_set:
            context = {"multiple_choice_id": multiple_choice_id}
            serializer = MultipleChoiceSolutionAnswerSerializer(data=answer, context=context)
            if serializer.is_valid():
                self.perform_create(serializer)
                response_data.append(serializer.data)
                answer_errors["multiplechoicesolutionanswer_set"].append({})
            else:
                answer_errors["multiplechoicesolutionanswer_set"].append(serializer.errors)
                serializer_has_errors = True
        if serializer_has_errors:
            print("ERRORS ", answer_errors)
            return Response(answer_errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            headers = self.get_success_headers(response_data)

            Flashcard.update_ranks(multiple_choice_id, "multiplechoice")

            multiple_choice = MultipleChoice.objects.get(pk=multiple_choice_id)
            multiple_choice.workload -= 1
            multiple_choice.save()

            return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


    def get_queryset(self):
        return MultipleChoiceSolutionAnswer.objects.filter(
            solution__multiple_choice__user_id=self.kwargs.get("user_id"),
            solution__multiple_choice__id=self.kwargs.get("multiple_choice_id")
        ).distinct()

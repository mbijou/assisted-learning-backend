from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin, ListModelMixin
from multiple_choices.api.serializers import MultipleChoiceSerializer, MultipleChoiceUpdateSerializer, \
    MultipleChoiceAnswerSetSerializer, MultipleChoiceSolutionAnswerSerializer
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
    serializer_class = MultipleChoiceAnswerSetSerializer

    # def get_serializer_context(self):
    #     return {"user_id": self.kwargs.get("user_id"), "multiple_choice_id": self.kwargs.get("multiple_choice_id")}

    def create(self, request, *args, **kwargs):
        answer_set = request.data.get("multiplechoicesolutionanswer_set")
        response_data = []
        for answer in answer_set:
            context = {"user_id": self.kwargs.get("user_id"),
                       "multiple_choice_id": self.kwargs.get("multiple_choice_id")}
            serializer = MultipleChoiceSolutionAnswerSerializer(data=answer, context=context)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            response_data.append(serializer.data)
        headers = self.get_success_headers(response_data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        return MultipleChoiceSolutionAnswer.objects.filter(
            user_id=self.kwargs.get("user_id"), solution__multiple_choice__id=self.kwargs.get("multiple_choice_id")
        ).distinct()

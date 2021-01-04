from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin, ListModelMixin
from multiple_choices.api.serializers import MultipleChoiceSerializer, MultipleChoiceUpdateSerializer, \
    MultipleChoiceAnswerSerializer
from multiple_choices.models import MultipleChoice


class MultipleChoiceViewSet(ModelViewSet):
    queryset = MultipleChoice.objects.all()
    serializer_class = MultipleChoiceSerializer

    def get_serializer_class(self):
        if self.kwargs.get("pk"):
            return MultipleChoiceUpdateSerializer
        return super().get_serializer_class()


class MultipleChoiceAnswerViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, ListModelMixin):
    queryset = MultipleChoice.objects.all()
    serializer_class = MultipleChoiceAnswerSerializer

    def get_serializer_context(self):
        return {"user_id": self.kwargs.get("user_id"), "multiple_choice_id": self.kwargs.get("multiple_choice_id")}

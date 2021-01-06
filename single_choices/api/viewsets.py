from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin

from single_choices.api.serializers import SingleChoiceSerializer, SingleChoiceAnswerSerializer
from single_choices.models import SingleChoice, SingleChoiceAnswer


class SingleChoiceViewSet(ModelViewSet):
    queryset = SingleChoice.objects.all()
    serializer_class = SingleChoiceSerializer


class SingleChoiceAnswerViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, ListModelMixin):
    queryset = SingleChoiceAnswer.objects.all()
    serializer_class = SingleChoiceAnswerSerializer

    def get_serializer_context(self):
        context = {"single_choice_id": self.kwargs.get("single_choice_id")}
        return context

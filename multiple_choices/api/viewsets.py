from rest_framework.viewsets import ModelViewSet

from multiple_choices.api.serializers import MultipleChoiceSerializer, MultipleChoiceUpdateSerializer
from multiple_choices.models import MultipleChoice


class MultipleChoiceViewSet(ModelViewSet):
    queryset = MultipleChoice.objects.all()
    serializer_class = MultipleChoiceSerializer

    def get_serializer_class(self):
        if self.kwargs.get("pk"):
            return MultipleChoiceUpdateSerializer
        return super().get_serializer_class()

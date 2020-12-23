from rest_framework.viewsets import ModelViewSet

from multiple_choices.api.serializers import MultipleChoiceSerializer
from multiple_choices.models import MultipleChoice


class MultipleChoiceViewSet(ModelViewSet):
    queryset = MultipleChoice.objects.all()
    serializer_class = MultipleChoiceSerializer

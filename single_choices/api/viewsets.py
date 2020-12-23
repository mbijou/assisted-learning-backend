from rest_framework.viewsets import ModelViewSet

from single_choices.api.serializers import SingleChoiceSerializer
from single_choices.models import SingleChoice


class SingleChoiceViewSet(ModelViewSet):
    queryset = SingleChoice.objects.all()
    serializer_class = SingleChoiceSerializer

from rest_framework.viewsets import ReadOnlyModelViewSet
from flashcard.api.serializers import FlashcardSerializer
from flashcard.models import Flashcard


class FlashcardViewSet(ReadOnlyModelViewSet):
    serializer_class = FlashcardSerializer
    queryset = Flashcard.objects.all()

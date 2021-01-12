from rest_framework.decorators import action
from rest_framework.viewsets import ReadOnlyModelViewSet
from flashcard.api.serializers import FlashcardSerializer
from flashcard.models import Flashcard
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class FlashcardPagination(PageNumberPagination):
    page_size = 4


class FlashcardViewSet(ReadOnlyModelViewSet):
    serializer_class = FlashcardSerializer
    queryset = Flashcard.objects.all().order_by("-id")
    pagination_class = FlashcardPagination

    @action(detail=False, url_path="rank-one-flashcards")
    def rank_one_flashcards(self, request, user_id=None):
        rank_one_flashcards = Flashcard.objects.filter(rank=1)[:1]

        serializer = self.get_serializer(rank_one_flashcards, many=True)
        return Response(serializer.data)

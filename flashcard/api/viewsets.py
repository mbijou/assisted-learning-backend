from rest_framework.decorators import action
from rest_framework.viewsets import ReadOnlyModelViewSet
from flashcard.api.serializers import FlashcardSerializer
from flashcard.models import Flashcard
from rest_framework.response import Response


class FlashcardViewSet(ReadOnlyModelViewSet):
    serializer_class = FlashcardSerializer
    queryset = Flashcard.objects.all()

    @action(detail=False, url_path="rank-one-flashcards")
    def rank_one_flashcards(self, request, user_id=None):
        rank_one_flashcards = Flashcard.objects.filter(rank=1)[:1]
        print("ASKOD")
        page = self.paginate_queryset(rank_one_flashcards)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(rank_one_flashcards, many=True)
        return Response(serializer.data)

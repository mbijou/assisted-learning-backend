from rest_framework.routers import SimpleRouter
from flashcard.api.viewsets import FlashcardViewSet
from django.urls import path


router = SimpleRouter()

# router.register("users/<int:user_id>/flashcards", FlashcardViewSet)

flashcard_urls = [
    path("users/<int:user_id>/flashcards/",
         FlashcardViewSet.as_view({"get": "list"})),

    path("users/<int:user_id>/flashcards/rank-one-flashcards/",
         FlashcardViewSet.as_view({"get": "rank_one_flashcards"})),

    path("users/<int:user_id>/flashcards/<int:pk>/",
         FlashcardViewSet.as_view({"get": "retrieve"})),
]

urlpatterns = flashcard_urls

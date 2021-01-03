from rest_framework.routers import SimpleRouter
from flashcard.api.viewsets import FlashcardViewSet

router = SimpleRouter()

router.register("flashcards", FlashcardViewSet)

urlpatterns = router.urls

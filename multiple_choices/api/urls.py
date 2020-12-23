from rest_framework.routers import SimpleRouter

from multiple_choices.api.viewsets import MultipleChoiceViewSet

router = SimpleRouter()

router.register("multiple-choices", MultipleChoiceViewSet)

urlpatterns = router.urls

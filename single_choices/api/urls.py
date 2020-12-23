from rest_framework.routers import SimpleRouter

from single_choices.api.viewsets import SingleChoiceViewSet

router = SimpleRouter()
router.register('single-choices', SingleChoiceViewSet)

urlpatterns = router.urls

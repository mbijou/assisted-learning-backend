from rest_framework.routers import SimpleRouter
from django.urls import path
from single_choices.api.viewsets import SingleChoiceViewSet, SingleChoiceAnswerViewSet

router = SimpleRouter()
router.register('single-choices', SingleChoiceViewSet)


answer_urls = [
    path("users/<int:user_id>/single-choices/<int:single_choice_id>/answers/",
         SingleChoiceAnswerViewSet.as_view({"get": "list", "post": "create"})),

    path("users/<int:user_id>/single-choices/<int:single_choice_id>/answers/<int:pk>/",
         SingleChoiceAnswerViewSet.as_view({"get": "retrieve"})),
]

urlpatterns = router.urls + answer_urls

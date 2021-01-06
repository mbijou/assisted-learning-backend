from rest_framework.routers import SimpleRouter
from django.urls import path
from multiple_choices.api.viewsets import MultipleChoiceViewSet, MultipleChoiceAnswerViewSet

router = SimpleRouter()
router.register("multiple-choices", MultipleChoiceViewSet)

answer_urls = [
    path("multiple-choices/<int:multiple_choice_id>/answers/",
         MultipleChoiceAnswerViewSet.as_view({"get": "list", "post": "create"})),

    path("multiple-choices/<int:multiple_choice_id>/answers/<int:pk>/",
         MultipleChoiceAnswerViewSet.as_view({"get": "retrieve"})),
]

urlpatterns = router.urls + answer_urls


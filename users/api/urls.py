from rest_framework.routers import SimpleRouter
from users.api.viewsets import UserViewSet, RegistrationView
from django.urls import path


# router = SimpleRouter()
#
# router.register("api/v1/users", UserViewSet)

user_urls = [
    path("users/",
         UserViewSet.as_view({"get": "list"})),

    path("users/<int:pk>/users-and-accomplishments/",
         UserViewSet.as_view({"get": "get_users_and_accomplishments"})),

    path("users/<int:pk>/",
         UserViewSet.as_view({"get": "retrieve"})),
    path('users/registration/', RegistrationView.as_view()),
]

urlpatterns = user_urls

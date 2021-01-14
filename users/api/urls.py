from rest_framework.routers import SimpleRouter
from users.api.viewsets import UserViewSet
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
]

urlpatterns = user_urls

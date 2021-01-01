from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
User = get_user_model()


class UserTests(APITestCase):
    fixtures = ["users/api/fixtures/users.json", ]

    def setUp(self):
        self.user = User.objects.get(username='admin')

    def test_Should_ReturnSingleChoices_When_TokenSentToEndpoint(self):
        response = self.client.post("/api/v1/api-token-auth/", data={"username": "admin", "password": "admin"})
        self.assertEqual(response.status_code, 200)
        token = response.json()['token']
        print(token)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get("/api/v1/single-choices/")
        self.assertEqual(response.status_code, 200)

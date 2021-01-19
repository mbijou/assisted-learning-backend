from datetime import datetime

from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from flashcard.models import Flashcard
from unittest import mock
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
        print(response.json()["user"])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get("/api/v1/single-choices/")
        self.assertEqual(response.status_code, 200)


class AccomplishmentTests(APITestCase):
    fixtures = ["users/api/fixtures/users.json", "users/api/fixtures/single_choices.json",
                "users/api/fixtures/multiple_choices.json", "users/api/fixtures/solutions.json"]

    def setUp(self):
        self.user = User.objects.get(username='admin')
        self.client.force_authenticate(self.user)
        self.patcher = mock.patch('users.api.viewsets.now')
        self.mock_now = self.patcher.start()
        self.mock_now.return_value = datetime(2000, 1, 1)


    def test_Should_ReturnAmountOfAccomplishedTasks(self):
        print("FLASHCARD", Flashcard.objects.all())
        response = self.client.get(f"/api/v1/users/{self.user.id}/users-and-accomplishments/", format="json")
        print(response.json())
        self.assertEqual(response.status_code, 200)
        # results = {"amount_flashcards_done": 2, "percentage_flashcards_done": 33.33,
        #            "amount_flashcards_open": 2, "percentage_flashcards_open": 33.33,
        #            "amount_flashcards_expired": 2, "percentage_flashcards_expired": 33.33,
        #            }
        self.assertEqual(response.json().get("amount_flashcards_done"), 2)
        self.assertEqual(response.json().get("amount_flashcards_open"), 2)
        self.assertEqual(response.json().get("amount_flashcards_expired"), 2)

    def tearDown(self):
        self.patcher.stop()

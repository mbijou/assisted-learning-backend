from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class FlashcardTests(APITestCase):
    fixtures = ["flashcard/api/fixtures/single_choices.json", "flashcard/api/fixtures/multiple_choice.json",
                "flashcard/api/fixtures/solutions.json"]

    def setUp(self):
        user = User.objects.create(username='lauren')
        self.client.force_authenticate(user=user)

    def test_Should_ReturnFlashcardsWithRank(self):
        response = self.client.get("/api/v1/flashcards/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0].get("rank"), 1)
        # TODO Beim answern muss der Rank für die beantwortete flashcard und alle anderen flashcards
        #  von dem Nutzer neu gesetzt werden
        # TODO RANK MACHEN

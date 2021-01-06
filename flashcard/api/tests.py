from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from flashcard.models import Flashcard

User = get_user_model()


class FlashcardTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='admin')
        self.client.force_authenticate(user=self.user)

        self.single_choice_data_1 = {"question": "Nenn mir alle Primzahlen, wie?", "workload": 42,
                                     "deadline": "2020-03-12", "solution": False, "user": self.user.id}
        self.single_choice_data_2 = {"question": "Fibonacci ist gut?", "workload": 42,
                                     "deadline": "2020-03-12", "solution": True, "user": self.user.id}
        self.multiple_choice_data_1 = {"question": "Was ist die Hauptstadt von Amerika?", "workload": 60,
                                       "deadline": "2020-04-03",
                                       "solution_set": [
                                           {"answer": "Bonn", "solution": False},
                                           {"answer": "Frankfurt", "solution": False},
                                           {"answer": "Berlin", "solution": True}
                                       ], "user": self.user.id
                                       }
        self.multiple_choice_data_2 = {"question": "Was ist die Hauptstadt von Polen?", "workload": 60,
                                       "deadline": "2020-04-03",
                                       "solution_set": [
                                           {"answer": "Bonn", "solution": False},
                                           {"answer": "Frankfurt", "solution": False},
                                           {"answer": "Berlin", "solution": True}
                                       ], "user": self.user.id
                                       }

    def create_flashcards(self):
        response1 = self.client.post("/api/v1/single-choices/", self.single_choice_data_1, format="json")
        response2 = self.client.post("/api/v1/multiple-choices/", self.multiple_choice_data_1, format="json")
        response3 = self.client.post("/api/v1/single-choices/", self.single_choice_data_2, format="json")
        response4 = self.client.post("/api/v1/multiple-choices/", self.multiple_choice_data_2, format="json")

        return response1, response2, response3, response4

    def get_flashcards(self, response1, response2, response3, response4):
        single_choice_1_flashcard = Flashcard.objects.get(
            content_type__model="singlechoice", object_id=response1.json().get("id")
        )
        multiple_choice_1_flashcard = Flashcard.objects.get(
            content_type__model="multiplechoice", object_id=response2.json().get("id")
        )
        single_choice_2_flashcard = Flashcard.objects.get(
            content_type__model="singlechoice", object_id=response3.json().get("id")
        )
        multiple_choice_2_flashcard = Flashcard.objects.get(
            content_type__model="multiplechoice", object_id=response4.json().get("id")
        )
        return single_choice_1_flashcard, multiple_choice_1_flashcard, single_choice_2_flashcard,\
            multiple_choice_2_flashcard

    def create_and_get_flashcards(self):
        response1, response2, response3, response4 = self.create_flashcards()
        flashcards = self.get_flashcards(response1, response2, response3, response4)
        return flashcards

    def test_Should_IncrementRanks_When_EachSingleChoiceAndMultipleChoiceCreation(self):
        response1, response2, response3, response4 = self.create_flashcards()

        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response2.status_code, 201)
        self.assertEqual(response3.status_code, 201)
        self.assertEqual(response4.status_code, 201)

        flashcards = self.get_flashcards(response1, response2, response3, response4)

        single_choice_1_flashcard = flashcards[0]
        multiple_choice_1_flashcard = flashcards[1]
        single_choice_2_flashcard = flashcards[2]
        multiple_choice_2_flashcard = flashcards[3]

        self.assertEqual(single_choice_1_flashcard.rank, 1)
        self.assertEqual(multiple_choice_1_flashcard.rank, 2)
        self.assertEqual(single_choice_2_flashcard.rank, 3)
        self.assertEqual(multiple_choice_2_flashcard.rank, 4)

    def test_Should_RotateRanks_When_SingleAndMultipleChoicesAreAnswered(self):
        flashcards = self.create_and_get_flashcards()

        single_choice_1_flashcard, multiple_choice_1_flashcard = flashcards[0], flashcards[1]
        single_choice_2_flashcard, multiple_choice_2_flashcard = flashcards[2], flashcards[3]

        single_choice_1_response = self.answer_single_choice_1(single_choice_1_flashcard)
        self.refresh_flashcards(flashcards)
        self.assertEqual(single_choice_1_response.status_code, 201)
        self.assertEqual(single_choice_1_flashcard.rank, 4)
        self.assertEqual(multiple_choice_1_flashcard.rank, 1)
        self.assertEqual(single_choice_2_flashcard.rank, 2)
        self.assertEqual(multiple_choice_2_flashcard.rank, 3)



        multiple_choice_1_response = self.answer_multiple_choice_1(multiple_choice_1_flashcard)
        self.refresh_flashcards(flashcards)
        self.assertEqual(multiple_choice_1_response.status_code, 201)
        self.assertEqual(multiple_choice_1_flashcard.rank, 4)
        self.assertEqual(single_choice_1_flashcard.rank, 3)
        self.assertEqual(single_choice_2_flashcard.rank, 1)
        self.assertEqual(multiple_choice_2_flashcard.rank, 2)


        single_choice_2_response = self.answer_single_choice_2(single_choice_2_flashcard)
        self.refresh_flashcards(flashcards)
        self.assertEqual(single_choice_2_response.status_code, 201)
        self.assertEqual(single_choice_2_flashcard.rank, 4)
        self.assertEqual(multiple_choice_1_flashcard.rank, 3)
        self.assertEqual(single_choice_1_flashcard.rank, 2)
        self.assertEqual(multiple_choice_2_flashcard.rank, 1)


        multiple_choice_2_response = self.answer_multiple_choice_2(multiple_choice_2_flashcard)
        self.refresh_flashcards(flashcards)
        self.assertEqual(multiple_choice_2_response.status_code, 201)
        self.assertEqual(multiple_choice_2_flashcard.rank, 4)
        self.assertEqual(multiple_choice_1_flashcard.rank, 2)
        self.assertEqual(single_choice_1_flashcard.rank, 1)
        self.assertEqual(single_choice_2_flashcard.rank, 3)

    def answer_single_choice_1(self, single_choice_1_flashcard):
        single_choice_id = single_choice_1_flashcard.object_id
        single_choice_1_response = self.client.post(f"/api/v1/single-choices/{single_choice_id}/answers/",
                                                    {"answer": True})
        return single_choice_1_response

    def answer_multiple_choice_1(self, multiple_choice_1_flashcard):
        multiple_choice_id = multiple_choice_1_flashcard.object_id
        multiple_choice_1_answer_data = {"multiplechoicesolutionanswer_set": [
            {"solution": 1, "answer": False}, {"solution": 2, "answer": False},
            {"solution": 3, "answer": False}
        ]}
        multiple_choice_1_response = self.client.post(f"/api/v1/multiple-choices/{multiple_choice_id}/answers/",
                                                      multiple_choice_1_answer_data, format="json")
        return multiple_choice_1_response

    def answer_single_choice_2(self, single_choice_2_flashcard):
        single_choice_id = single_choice_2_flashcard.object_id
        single_choice_2_response = self.client.post(f"/api/v1/single-choices/{single_choice_id}/answers/",
                                                    {"answer": True})
        return single_choice_2_response

    def answer_multiple_choice_2(self, multiple_choice_2_flashcard):
        multiple_choice_id = multiple_choice_2_flashcard.object_id
        multiple_choice_2_answer_data = {"multiplechoicesolutionanswer_set": [
            {"solution": 4, "answer": False}, {"solution": 5, "answer": False},
            {"solution": 6, "answer": False}
        ]}
        multiple_choice_2_response = self.client.post(f"/api/v1/multiple-choices/{multiple_choice_id}/answers/",
                                                      multiple_choice_2_answer_data, format="json")
        return multiple_choice_2_response

    def refresh_flashcards(self, flashcards):
        for f in flashcards:
            f.refresh_from_db()

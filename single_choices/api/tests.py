from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from flashcard.models import Flashcard
from single_choices.models import SingleChoice
from datetime import datetime
from unittest import mock
User = get_user_model()


class SingleChoiceTests(APITestCase):
    fixtures = ["single_choices/api/fixtures/users.json"]

    def setUp(self):
        self.user = User.objects.get(username="admin")
        self.client.force_authenticate(user=self.user)

    def test_single_choice_can_be_created(self):
        response = self.client.post(f"/api/v1/single-choices/",
                                    {"question": "Was ist die Hauptstadt von Frankreich?", "workload": 42,
                                     "deadline": "2020-03-12", "solution": False, "user": self.user.id})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(SingleChoice.objects.count(), 1)


class SingleChoiceUpdateAndDeletionTests(APITestCase):
    fixtures = ["single_choices/api/fixtures/single_choices.json", "single_choices/api/fixtures/users.json"]

    def setUp(self):
        self.user = User.objects.get(username="admin")
        self.client.force_authenticate(user=self.user)
        self.single_choice = SingleChoice.objects.get(pk=1)

    def test_single_choice_can_be_updated(self):
        new_question, new_workload, new_solution, new_deadline, new_user_id = "Was bist du?", 50, True, "2050-09-12", 2

        response = self.client.put(f"/api/v1/single-choices/{self.single_choice.id}/",
                                   {"question": new_question, "workload": new_workload,
                                    "deadline": new_deadline, "solution": new_solution, "user": new_user_id})
        self.single_choice.refresh_from_db()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.single_choice.question, new_question)
        self.assertEqual(self.single_choice.workload, new_workload)
        self.assertEqual(self.single_choice.solution, new_solution)
        self.assertEqual(str(self.single_choice.deadline), new_deadline)
        self.assertEqual(self.single_choice.user_id, new_user_id)

    def test_single_choice_can_be_deleted(self):
        response = self.client.delete(f"/api/v1/single-choices/{self.single_choice.id}/")
        self.assertEqual(response.status_code, 204)

        self.assertEqual(SingleChoice.objects.filter(pk=self.single_choice.pk).count(), 0)
        self.assertEqual(Flashcard.objects.filter(
            object_id=self.single_choice.pk, content_type__model="singlechoice").count(), 0
                         )


class SingleChoiceAnswerTests(APITestCase):
    fixtures = ["single_choices/api/fixtures/single_choices.json", "single_choices/api/fixtures/users.json"]

    def setUp(self):
        self.user = User.objects.get(username="admin")
        self.client.force_authenticate(user=self.user)
        self.single_choice = SingleChoice.objects.get(pk=1)

        self.patcher = mock.patch('single_choices.api.serializers.now')
        self.mock_now = self.patcher.start()
        self.mock_now.return_value = datetime(2000, 1, 1)

    # @mock.patch('single_choices.api.serializers.now')
    def test_single_choice_can_be_answered(self):  # , mock_now
        # mock_now.return_value = datetime(2000, 1, 1)
        response = self.client.post(f"/api/v1/single-choices/{self.single_choice.id}/answers/",
                                    {"answer": True})
        self.assertEqual(response.status_code, 201)
        answer_id = response.json().get("id")
        answer_set = self.single_choice.singlechoiceanswer_set.all()
        self.assertIn(answer_id, answer_set.values_list("id", flat=True))


    def test_Should_DecreaseWorkloadByOne_When_SingleChoiceIsAnsweredSuccessfully(self):
        initial_workload = self.single_choice.workload
        response = self.client.post(f"/api/v1/single-choices/{self.single_choice.id}/answers/",
                                    {"answer": True})
        self.assertEqual(response.status_code, 201)
        self.single_choice.refresh_from_db()
        self.assertEqual(self.single_choice.workload, initial_workload-1)

    def tearDown(self):
        self.patcher.stop()

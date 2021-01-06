from rest_framework.test import APITestCase
from multiple_choices.models import MultipleChoice, Solution, MultipleChoiceSolutionAnswer
from django.contrib.auth import get_user_model
User = get_user_model()


class MultipleChoiceTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='lauren')
        self.client.force_authenticate(user=self.user)

    def test_create_multiple_choice(self):
        data = {"question": "Was ist die Hauptstadt von Deutschland?", "workload": 42, "deadline": "2020-03-12",
                "solution_set": [
                    {"answer": "Bonn", "solution": False},
                    {"answer": "Frankfurt", "solution": False},
                    {"answer": "Berlin", "solution": True}
                ], "user": self.user.id
                }
        response = self.client.post("/api/v1/multiple-choices/", data, format="json")
        self.assertEqual(response.status_code, 201, "response.status_code should be 201")
        multiple_choice = MultipleChoice.objects.get(id=1)
        self.assertNotEqual(MultipleChoice.objects.count(), None, "MultipleChoice.objects.count() should be 1")
        self.assertEqual(multiple_choice.user_id, self.user.id)

    def test_multiple_choice_throw_error_upon_creation(self):
        data = {"question": "Was ist die Hauptstadt von Deutschland?", "workload": 42, "deadline": "2020-03-12",
                "solution_set": [
                    {},
                    {},
                    {"answer": "Berlin", "solution": True}
                ]
                }
        response = self.client.post("/api/v1/multiple-choices/", data, format="json")
        self.assertEqual(response.status_code, 400, "response.status_code should be 400")


class MultipleChoiceUpdateTests(APITestCase):
    fixtures = ["multiple_choices/api/fixtures/multiple_choice.json", "multiple_choices/api/fixtures/solutions.json"]

    def setUp(self):
        self.user = User.objects.create(username='lauren')
        self.client.force_authenticate(user=self.user)
        self.data = {"question": "Was ist die Hauptstadt von Deutschland?", "workload": 60, "deadline": "2020-04-03",
                     "solution_set": [
                         {"id": 1, "answer": "Bonn", "solution": False},
                         {"id": 2, "answer": "Frankfurt", "solution": False},
                         {"id": 3, "answer": "Berlin", "solution": True}
                     ], "user": self.user.id
                     }
        self.multiple_choice = MultipleChoice.objects.get(id=2)
        self.url = f"/api/v1/multiple-choices/{self.multiple_choice.id}/"

    def test_update_multiple_choice(self):
        response = self.client.put(self.url, self.data, format="json")
        self.assertEqual(response.status_code, 200, "response.status_code should be 200")

        updated_solution = Solution.objects.get(id=3)
        self.assertEqual(updated_solution.solution, True, "updated_solution.solution should be True")

    def test_Should_RaiseException_When_SolutionIsUpdatedWhichIsNotPartOfTheMultipleChoice(self):
        url = f"/api/v1/multiple-choices/3/"
        response = self.client.put(url, self.data, format="json")
        self.assertEqual(response.status_code, 400)


class MultipleChoiceAnswerTests(APITestCase):
    fixtures = ["multiple_choices/api/fixtures/multiple_choice.json", "multiple_choices/api/fixtures/solutions.json",
                "multiple_choices/api/fixtures/users.json"]

    def setUp(self):
        self.user = User.objects.get(username="admin")
        self.client.force_authenticate(user=self.user)
        self.multiple_choice = MultipleChoice.objects.get(pk=2)

        self.data = {
            "multiplechoicesolutionanswer_set": [
                {"solution": 1, "answer": False}, {"solution": 2, "answer": False},
                {"solution": 3, "answer": False}, {"solution": 4, "answer": True}
            ], "user": self.user.id
        }

    def test_multiple_choice_can_be_answered(self):
        response = self.client.post(
            f"/api/v1/multiple-choices/{self.multiple_choice.id}/answers/",
            self.data, format="json")
        print(response.json())
        self.assertEqual(response.status_code, 201)


    def test_Should_NotAcceptAnswersOfOtherMultipleChoices(self):
        self.client.post(f"/api/v1/multiple-choices/{self.multiple_choice.id}/answers/", self.data, format="json")
        data = {
            "multiplechoicesolutionanswer_set": [
                {"solution": 5, "answer": False}, {"solution": 6, "answer": False},
                {"solution": 7, "answer": False}, {"solution": 8, "answer": True}
            ]
        }
        self.client.post(f"/api/v1/multiple-choices/3/answers/", data, format="json")
        response = self.client.get(f"/api/v1/multiple-choices/3/answers/")
        for answer_json in response.json():
            self.assertIn(answer_json.get("solution"), [5, 6, 7, 8])
        self.assertEqual(response.status_code, 200)


    def test_Should_NotCreateAnswersForSolutionsWhichAreNoSolutionsOfMultipleChoice(self):
        data = {
            "multiplechoicesolutionanswer_set": [
                {"solution": 5, "answer": False}, {"solution": 6, "answer": False},
                {"solution": 7, "answer": False}, {"solution": 8, "answer": True}
            ]
        }
        response = self.client.post(f"/api/v1/multiple-choices/{self.multiple_choice.id}/answers/",
                                    data, format="json")
        self.assertEqual(response.status_code, 400)

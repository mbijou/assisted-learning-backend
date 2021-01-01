from django.test import TestCase
from rest_framework.test import APITestCase
from multiple_choices.models import MultipleChoice, Solution
from django.contrib.auth import get_user_model
User = get_user_model()


class MultipleChoiceTests(APITestCase):
    def setUp(self):
        user = User.objects.create(username='lauren')
        self.client.force_authenticate(user=user)

    def test_create_multiple_choice(self):
        data = {"question": "Was ist die Hauptstadt von Deutschland?", "workload": 42, "deadline": "2020-03-12",
                "solution_set": [
                    {"answer": "Bonn", "solution": False},
                    {"answer": "Frankfurt", "solution": False},
                    {"answer": "Berlin", "solution": True}
                ]
                }
        response = self.client.post("/api/v1/multiple-choices/", data, format="json")
        self.assertEqual(response.status_code, 201, "response.status_code should be 201")
        self.assertEqual(MultipleChoice.objects.count(), 1, "MultipleChoice.objects.count() should be 1")

    def test_multiple_choice_throw_error_upon_creation(self):
        data = {"question": "Was ist die Hauptstadt von Deutschland?", "workload": 42, "deadline": "2020-03-12",
                "solution_set": [
                    {},
                    {},
                    {"answer": "Berlin", "solution": True}
                ]
                }
        response = self.client.post("/api/v1/multiple-choices/", data, format="json")
        print("Fehlercode: ", response.status_code, "\nFehlertext", response.content)
        self.assertEqual(response.status_code, 400, "response.status_code should be 400")


class MultipleChoiceUpdateTests(APITestCase):
    fixtures = ["multiple_choices/api/fixtures/multiple_choice.json", "multiple_choices/api/fixtures/solutions.json"]

    def setUp(self):
        user = User.objects.create(username='lauren')
        self.client.force_authenticate(user=user)

    def test_update_multiple_choice(self):
        multiple_choice = MultipleChoice.objects.first()
        print(MultipleChoice.objects.all(), Solution.objects.all())
        data = {"question": "Was ist die Hauptstadt von Deutschland?", "workload": 60, "deadline": "2020-04-03",
                "solution_set": [
                    {"id": 4, "answer": "Bonn", "solution": False},
                    {"id": 5, "answer": "Frankfurt", "solution": False},
                    {"id": 6, "answer": "Berlin", "solution": True}
                ]
                }
        response = self.client.put(f"/api/v1/multiple-choices/{multiple_choice.id}/", data, format="json")
        self.assertEqual(response.status_code, 200, "response.status_code should be 200")

        updated_solution = Solution.objects.get(id=6)
        self.assertEqual(updated_solution.solution, True, "updated_solution.solution should be True")

# Create your tests here.

# {
# 	"question": "Wie siehst du das eigentlich?",
# 	"workload": 100,
# 	"deadline": "2020-12-03",
# 	"solution_set": [
# 		{"answer": "abc", "solution": false},
# 		{"answer": "def", "solution": false},
# 		{"answer": "ghi", "solution": false}
# 	]
#
# }


# {
# 	"question": "Wie siehst du das eigentlich 2.0?",
# 	"workload": 100,
# 	"deadline": "2020-12-03",
# 	"solution_set": [
# 		{"id": 4, "answer": "fff", "solution": false},
# 		{"id": 5, "answer": "ggg", "solution": false},
# 		{"id": 6, "answer": "hhh", "solution": true}
# 	]
#
# }

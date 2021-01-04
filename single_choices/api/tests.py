from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from single_choices.models import SingleChoice
User = get_user_model()


class SingleChoiceAnswerTests(APITestCase):
    fixtures = ["single_choices/api/fixtures/single_choices.json", "single_choices/api/fixtures/users.json"]

    def setUp(self):
        self.user = User.objects.get(username="admin")
        self.client.force_authenticate(user=self.user)
        self.single_choice = SingleChoice.objects.get(pk=1)

    def test_single_choice_can_be_answered(self):
        response = self.client.post(f"/api/v1/users/{self.user.id}/single-choices/{self.single_choice.id}/answers/",
                                    {"answer": True})
        self.assertEqual(response.status_code, 201)
        answer_id = response.json().get("id")
        self.assertIn(answer_id, self.single_choice.singlechoiceanswer_set.values_list("id", flat=True))
        self.assertIn(self.user.id, self.single_choice.singlechoiceanswer_set.values_list("user__id", flat=True))

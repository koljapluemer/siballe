from rest_framework.test import APITestCase

from learning.models import Node, Rel, Situation, SituationRelation


class GenerateExerciseViewTests(APITestCase):
    def setUp(self):
        self.situation = Situation.objects.create(language="fra", description="Test")

    def test_requires_situation_id(self):
        response = self.client.get("/api/exercises/generate/")
        self.assertEqual(response.status_code, 400)

    def test_rejects_non_integer_situation_id(self):
        response = self.client.get("/api/exercises/generate/?situation_id=abc")
        self.assertEqual(response.status_code, 400)

    def test_404_for_missing_situation(self):
        response = self.client.get("/api/exercises/generate/?situation_id=999")
        self.assertEqual(response.status_code, 404)

    def test_404_for_no_exercisable_content(self):
        response = self.client.get(
            f"/api/exercises/generate/?situation_id={self.situation.id}"
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "no_exercisable_content")

    def test_open_to_anonymous_users_and_returns_exercise(self):
        node = Node.objects.create(kind=Node.Kind.VOCAB, language="fra", content="chat")
        eng = Node.objects.create(kind=Node.Kind.VOCAB, language="eng", content="cat")
        Rel.objects.create(sender=node, receiver=eng, label=Rel.Label.TRANSLATION)
        SituationRelation.objects.create(situation=self.situation, node=node, relevance=3)

        response = self.client.get(
            f"/api/exercises/generate/?situation_id={self.situation.id}"
        )
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["kind"], "FlashcardVocab")
        self.assertIn("chat", body["front"])

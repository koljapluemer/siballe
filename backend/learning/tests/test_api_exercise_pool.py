from rest_framework.test import APITestCase

from learning.models import Node, Rel, Situation, SituationRelation


class ExercisePoolViewTests(APITestCase):
    def setUp(self):
        self.situation_a = Situation.objects.create(language="fra", description="A")
        self.situation_b = Situation.objects.create(language="fra", description="B")

    def _make_vocab_with_translation(self, content="chat"):
        node = Node.objects.create(kind=Node.Kind.VOCAB, language="fra", content=content)
        eng = Node.objects.create(kind=Node.Kind.VOCAB, language="eng", content=content)
        Rel.objects.create(sender=node, receiver=eng, label=Rel.Label.TRANSLATION)
        return node

    def test_requires_situation_ids(self):
        response = self.client.get("/api/exercises/pool/")
        self.assertEqual(response.status_code, 400)

    def test_rejects_non_integer_situation_ids(self):
        response = self.client.get("/api/exercises/pool/?situation_ids=abc")
        self.assertEqual(response.status_code, 400)

    def test_open_to_anonymous_users(self):
        response = self.client.get(f"/api/exercises/pool/?situation_ids={self.situation_a.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"results": []})

    def test_returns_one_entry_per_node_with_stable_id(self):
        node = self._make_vocab_with_translation()
        SituationRelation.objects.create(situation=self.situation_a, node=node, relevance=3)

        response = self.client.get(f"/api/exercises/pool/?situation_ids={self.situation_a.id}")
        self.assertEqual(response.status_code, 200)
        results = response.json()["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], node.id)
        self.assertEqual(results[0]["situation_ids"], [self.situation_a.id])

    def test_dedups_node_eligible_under_multiple_situations(self):
        node = self._make_vocab_with_translation()
        SituationRelation.objects.create(situation=self.situation_a, node=node, relevance=3)
        SituationRelation.objects.create(situation=self.situation_b, node=node, relevance=3)

        response = self.client.get(
            f"/api/exercises/pool/?situation_ids={self.situation_a.id},{self.situation_b.id}"
        )
        results = response.json()["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(sorted(results[0]["situation_ids"]), sorted([self.situation_a.id, self.situation_b.id]))

    def test_two_distinct_nodes_yield_two_entries(self):
        node_a = self._make_vocab_with_translation("chat")
        node_b = self._make_vocab_with_translation("chien")
        SituationRelation.objects.create(situation=self.situation_a, node=node_a, relevance=3)
        SituationRelation.objects.create(situation=self.situation_a, node=node_b, relevance=3)

        response = self.client.get(f"/api/exercises/pool/?situation_ids={self.situation_a.id}")
        results = response.json()["results"]
        self.assertEqual({r["id"] for r in results}, {node_a.id, node_b.id})

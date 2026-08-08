from rest_framework.test import APITestCase

from learning.models import Node


class NodeSearchViewTests(APITestCase):
    def setUp(self):
        Node.objects.create(kind=Node.Kind.VOCAB, language="fra", content="chat")
        Node.objects.create(kind=Node.Kind.VOCAB, language="fra", content="chatte")
        Node.objects.create(kind=Node.Kind.VOCAB, language="fra", content="chien")
        Node.objects.create(kind=Node.Kind.VOCAB, language="eng", content="chat")
        Node.objects.create(kind=Node.Kind.SENTENCE, language="fra", content="chat noir")

    def test_requires_kind_and_language(self):
        response = self.client.get("/api/nodes/search/", {"q": "chat"})
        self.assertEqual(response.status_code, 400)

    def test_blank_query_returns_nothing(self):
        response = self.client.get("/api/nodes/search/", {"kind": "VOCAB", "language": "fra"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_matches_are_scoped_by_kind_and_language(self):
        response = self.client.get(
            "/api/nodes/search/", {"kind": "VOCAB", "language": "fra", "q": "chat"}
        )
        self.assertEqual(response.status_code, 200)
        contents = {row["content"] for row in response.json()}
        self.assertEqual(contents, {"chat", "chatte"})

    def test_case_insensitive(self):
        response = self.client.get(
            "/api/nodes/search/", {"kind": "VOCAB", "language": "fra", "q": "CHAT"}
        )
        contents = {row["content"] for row in response.json()}
        self.assertEqual(contents, {"chat", "chatte"})

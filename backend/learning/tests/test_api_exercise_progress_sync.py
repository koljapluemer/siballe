from rest_framework.test import APITestCase

from learning.models import ExerciseProgress, Node, User


class ExerciseProgressSyncViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", email="a@example.com", password="x")
        self.node = Node.objects.create(kind=Node.Kind.VOCAB, language="fra", content="chat")
        self.client.force_authenticate(user=self.user)

    def _item(self, node_id, due, updated_at):
        return {
            "node_id": node_id,
            "card_data": {"due": due, "stability": 1.0},
            "updated_at": updated_at,
        }

    def test_requires_authentication(self):
        self.client.force_authenticate(user=None)
        response = self.client.post("/api/sync/exercise-progress/", {"progress": []}, format="json")
        self.assertEqual(response.status_code, 401)

    def test_creates_new_progress(self):
        item = self._item(self.node.id, "2026-08-13T10:00:00Z", "2026-08-12T10:00:00Z")
        response = self.client.post(
            "/api/sync/exercise-progress/", {"progress": [item]}, format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ExerciseProgress.objects.count(), 1)
        body = response.json()["progress"]
        self.assertEqual(len(body), 1)
        self.assertEqual(body[0]["node_id"], self.node.id)

    def test_newer_update_overwrites(self):
        self.client.post(
            "/api/sync/exercise-progress/",
            {"progress": [self._item(self.node.id, "2026-08-13T10:00:00Z", "2026-08-12T10:00:00Z")]},
            format="json",
        )
        response = self.client.post(
            "/api/sync/exercise-progress/",
            {"progress": [self._item(self.node.id, "2026-08-14T10:00:00Z", "2026-08-12T11:00:00Z")]},
            format="json",
        )
        progress = ExerciseProgress.objects.get(user=self.user, node=self.node)
        self.assertEqual(progress.card_data["due"], "2026-08-14T10:00:00Z")

    def test_older_update_is_dropped(self):
        self.client.post(
            "/api/sync/exercise-progress/",
            {"progress": [self._item(self.node.id, "2026-08-13T10:00:00Z", "2026-08-12T11:00:00Z")]},
            format="json",
        )
        response = self.client.post(
            "/api/sync/exercise-progress/",
            {"progress": [self._item(self.node.id, "2026-08-10T10:00:00Z", "2026-08-12T10:00:00Z")]},
            format="json",
        )
        progress = ExerciseProgress.objects.get(user=self.user, node=self.node)
        self.assertEqual(progress.card_data["due"], "2026-08-13T10:00:00Z")
        # response still reports the server's (unchanged, winning) state
        body = response.json()["progress"]
        self.assertEqual(body[0]["card_data"]["due"], "2026-08-13T10:00:00Z")

    def test_response_returns_full_current_state_not_just_delta(self):
        other_node = Node.objects.create(kind=Node.Kind.VOCAB, language="fra", content="chien")
        self.client.post(
            "/api/sync/exercise-progress/",
            {"progress": [self._item(self.node.id, "2026-08-13T10:00:00Z", "2026-08-12T10:00:00Z")]},
            format="json",
        )
        response = self.client.post(
            "/api/sync/exercise-progress/",
            {"progress": [self._item(other_node.id, "2026-08-13T10:00:00Z", "2026-08-12T10:00:00Z")]},
            format="json",
        )
        node_ids = {item["node_id"] for item in response.json()["progress"]}
        self.assertEqual(node_ids, {self.node.id, other_node.id})

    def test_rejects_progress_scoped_to_authenticated_user_only(self):
        other_user = User.objects.create_user(username="bob", email="b@example.com", password="x")
        ExerciseProgress.objects.create(
            user=other_user,
            node=self.node,
            card_data={"due": "2026-08-13T10:00:00Z"},
            due="2026-08-13T10:00:00Z",
            client_updated_at="2026-08-12T10:00:00Z",
        )
        response = self.client.post(
            "/api/sync/exercise-progress/", {"progress": []}, format="json"
        )
        self.assertEqual(response.json()["progress"], [])

    def test_missing_due_in_card_data_rejected(self):
        response = self.client.post(
            "/api/sync/exercise-progress/",
            {"progress": [{"node_id": self.node.id, "card_data": {}, "updated_at": "2026-08-12T10:00:00Z"}]},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

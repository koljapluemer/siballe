from rest_framework.test import APITestCase

from learning.models import User


class RegisterViewTests(APITestCase):
    def _payload(self, **overrides):
        payload = {
            "username": "alice",
            "email": "alice@example.com",
            "password": "correct-horse-battery-staple",
            "password_confirm": "correct-horse-battery-staple",
        }
        payload.update(overrides)
        return payload

    def test_creates_user_and_returns_tokens(self):
        response = self.client.post("/api/auth/register/", self._payload())
        self.assertEqual(response.status_code, 201)
        body = response.json()
        self.assertIn("access", body)
        self.assertIn("refresh", body)
        self.assertTrue(User.objects.filter(username="alice").exists())

    def test_password_is_hashed(self):
        self.client.post("/api/auth/register/", self._payload())
        user = User.objects.get(username="alice")
        self.assertNotEqual(user.password, "correct-horse-battery-staple")
        self.assertTrue(user.check_password("correct-horse-battery-staple"))

    def test_rejects_duplicate_username(self):
        User.objects.create_user(username="alice", email="other@example.com", password="x")
        response = self.client.post("/api/auth/register/", self._payload())
        self.assertEqual(response.status_code, 400)

    def test_rejects_duplicate_email(self):
        User.objects.create_user(username="bob", email="alice@example.com", password="x")
        response = self.client.post("/api/auth/register/", self._payload())
        self.assertEqual(response.status_code, 400)

    def test_rejects_mismatched_passwords(self):
        response = self.client.post(
            "/api/auth/register/", self._payload(password_confirm="different")
        )
        self.assertEqual(response.status_code, 400)

    def test_rejects_weak_password(self):
        response = self.client.post(
            "/api/auth/register/", self._payload(password="pw", password_confirm="pw")
        )
        self.assertEqual(response.status_code, 400)


class MeViewTests(APITestCase):
    def test_requires_authentication(self):
        response = self.client.get("/api/auth/me/")
        self.assertEqual(response.status_code, 401)

    def test_returns_current_user(self):
        user = User.objects.create_user(
            username="alice", email="alice@example.com", password="x"
        )
        self.client.force_authenticate(user=user)
        response = self.client.get("/api/auth/me/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"username": "alice", "email": "alice@example.com"})

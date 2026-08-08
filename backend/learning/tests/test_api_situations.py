from rest_framework.test import APITestCase

from learning.models import Situation


class SituationListViewTests(APITestCase):
    def test_open_to_anonymous_users(self):
        response = self.client.get("/api/situations/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_grouped_by_language(self):
        Situation.objects.create(language="fra", description="Smalltalk in French")
        Situation.objects.create(language="fra", description="Buying bread")
        Situation.objects.create(language="deu", description="Ordering coffee")

        response = self.client.get("/api/situations/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        languages = [group["language"] for group in data]
        self.assertEqual(languages, ["deu", "fra"])

        fra_group = next(g for g in data if g["language"] == "fra")
        descriptions = {s["description"] for s in fra_group["situations"]}
        self.assertEqual(descriptions, {"Smalltalk in French", "Buying bread"})

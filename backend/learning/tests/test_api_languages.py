from rest_framework.test import APITestCase


class LanguageListViewTests(APITestCase):
    def test_returns_full_iso639_3_list_sorted_by_name(self):
        response = self.client.get("/api/languages/")
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertGreater(len(data), 1000)  # not a hardcoded handful of languages

        codes = {entry["code"]: entry["name"] for entry in data}
        self.assertEqual(codes["eng"], "English")
        self.assertEqual(codes["vie"], "Vietnamese")

        names = [entry["name"] for entry in data]
        self.assertEqual(names, sorted(names))

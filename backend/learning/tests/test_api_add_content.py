from unittest.mock import patch

from rest_framework.test import APITestCase

from learning.models import Node, Rel, Situation, SituationRelation

URL = "/api/nodes/add-content/"


class AddContentValidationTests(APITestCase):
    def test_missing_both_content_and_translation_rejected(self):
        response = self.client.post(
            URL, {"kind": "VOCAB", "language": "fra", "translations": []}, format="json"
        )
        self.assertEqual(response.status_code, 400)


class AddContentBaseSaveTests(APITestCase):
    def test_content_only_creates_node_and_default_situation(self):
        response = self.client.post(
            URL, {"kind": "VOCAB", "language": "fra", "content": "chat"}, format="json"
        )
        self.assertEqual(response.status_code, 201)

        node = Node.objects.get(kind=Node.Kind.VOCAB, language="fra", content="chat")
        self.assertEqual(node.state, Node.State.NEEDS_CHECKING)

        situation = Situation.objects.get(language="fra")
        self.assertEqual(situation.description, "General French")

        rel = SituationRelation.objects.get(situation=situation, node=node)
        self.assertEqual(rel.relevance, 3)

    def test_translation_only_creates_translation_node_but_no_main_node(self):
        response = self.client.post(
            URL,
            {
                "kind": "VOCAB",
                "language": "fra",
                "translations": [{"content": "cat", "note": ""}],
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertIsNone(response.json()["node_id"])

        self.assertTrue(
            Node.objects.filter(kind=Node.Kind.VOCAB, language="eng", content="cat").exists()
        )
        self.assertEqual(SituationRelation.objects.count(), 0)

    def test_duplicate_submission_reuses_nodes_and_merges_note(self):
        self.client.post(
            URL,
            {
                "kind": "VOCAB",
                "language": "fra",
                "content": "chat",
                "translations": [{"content": "cat", "note": "pet"}],
            },
            format="json",
        )
        response = self.client.post(
            URL,
            {
                "kind": "VOCAB",
                "language": "fra",
                "content": "chat",
                "translations": [{"content": "cat", "note": "animal"}],
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)

        self.assertEqual(
            Node.objects.filter(kind=Node.Kind.VOCAB, language="fra", content="chat").count(), 1
        )
        chat = Node.objects.get(kind=Node.Kind.VOCAB, language="fra", content="chat")
        cat = Node.objects.get(kind=Node.Kind.VOCAB, language="eng", content="cat")
        rel = Rel.objects.get(sender=chat, receiver=cat, label=Rel.Label.TRANSLATION)
        self.assertEqual(rel.note, "pet; animal")


class AddContentGenerationTests(APITestCase):
    @patch("learning.services.generation.generate_examples")
    @patch("learning.services.generation.translate_missing")
    def test_missing_translation_and_examples_are_generated_and_marked(
        self, mock_translate_missing, mock_generate_examples
    ):
        mock_translate_missing.return_value = {"content": "cat", "note": ""}
        mock_generate_examples.return_value = [
            {"sentence": "Le chat dort.", "translation": "The cat sleeps.", "note": ""}
        ]

        response = self.client.post(
            URL,
            {
                "kind": "VOCAB",
                "language": "fra",
                "content": "chat",
                "openai_api_key": "sk-test",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)

        mock_translate_missing.assert_called_once_with(
            api_key="sk-test",
            kind="VOCAB",
            source_language="fra",
            target_language="eng",
            text="chat",
        )

        chat = Node.objects.get(kind=Node.Kind.VOCAB, language="fra", content="chat")
        cat = Node.objects.get(kind=Node.Kind.VOCAB, language="eng", content="cat")
        self.assertEqual(cat.state, Node.State.AUTO_GENERATED)
        translation_rel = Rel.objects.get(sender=chat, receiver=cat, label=Rel.Label.TRANSLATION)
        self.assertEqual(translation_rel.state, Rel.State.AUTO_GENERATED)

        mock_generate_examples.assert_called_once_with(
            api_key="sk-test", word="chat", translation="cat", language="fra"
        )

        sentence = Node.objects.get(
            kind=Node.Kind.SENTENCE, language="fra", content="Le chat dort."
        )
        self.assertEqual(sentence.state, Node.State.AUTO_GENERATED)
        self.assertTrue(
            Rel.objects.filter(
                sender=chat, receiver=sentence, label=Rel.Label.PART_OF, state=Rel.State.AUTO_GENERATED
            ).exists()
        )
        self.assertTrue(
            Rel.objects.filter(
                sender=sentence, receiver=chat, label=Rel.Label.EXAMPLE, state=Rel.State.AUTO_GENERATED
            ).exists()
        )

        eng_translation = Node.objects.get(
            kind=Node.Kind.SENTENCE, language="eng", content="The cat sleeps."
        )
        self.assertEqual(eng_translation.state, Node.State.AUTO_GENERATED)

        situation = Situation.objects.get(language="fra")
        self.assertEqual(
            SituationRelation.objects.get(situation=situation, node=sentence).relevance, 2
        )

    @patch("learning.services.generation.extract_vocab")
    def test_sentence_split_creates_reciprocal_part_of_and_example_rels(self, mock_extract_vocab):
        mock_extract_vocab.return_value = [
            {"word": "chat", "translation": "cat", "note": ""},
            {"word": "noir", "translation": "black", "note": "adjective"},
        ]

        response = self.client.post(
            URL,
            {
                "kind": "SENTENCE",
                "language": "fra",
                "content": "Le chat noir.",
                "translations": [{"content": "The black cat.", "note": ""}],
                "openai_api_key": "sk-test",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)

        mock_extract_vocab.assert_called_once_with(
            api_key="sk-test",
            sentence="Le chat noir.",
            translation="The black cat.",
            language="fra",
        )

        sentence = Node.objects.get(kind=Node.Kind.SENTENCE, language="fra", content="Le chat noir.")
        chat = Node.objects.get(kind=Node.Kind.VOCAB, language="fra", content="chat")
        noir = Node.objects.get(kind=Node.Kind.VOCAB, language="fra", content="noir")
        self.assertEqual(chat.state, Node.State.AUTO_GENERATED)

        for word in (chat, noir):
            self.assertTrue(
                Rel.objects.filter(sender=word, receiver=sentence, label=Rel.Label.PART_OF).exists()
            )
            self.assertTrue(
                Rel.objects.filter(sender=sentence, receiver=word, label=Rel.Label.EXAMPLE).exists()
            )

        noir_translation = Node.objects.get(kind=Node.Kind.VOCAB, language="eng", content="black")
        noir_rel = Rel.objects.get(
            sender=noir, receiver=noir_translation, label=Rel.Label.TRANSLATION
        )
        self.assertEqual(noir_rel.note, "adjective")

        situation = Situation.objects.get(language="fra")
        self.assertEqual(SituationRelation.objects.get(situation=situation, node=chat).relevance, 2)
        self.assertEqual(SituationRelation.objects.get(situation=situation, node=noir).relevance, 2)

    @patch("learning.services.generation.translate_missing")
    def test_generation_failure_does_not_lose_saved_data(self, mock_translate_missing):
        mock_translate_missing.side_effect = Exception("boom")

        response = self.client.post(
            URL,
            {
                "kind": "VOCAB",
                "language": "fra",
                "content": "chat",
                "openai_api_key": "sk-test",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("boom", response.json()["generation_error"])

        node = Node.objects.get(kind=Node.Kind.VOCAB, language="fra", content="chat")
        self.assertEqual(node.state, Node.State.NEEDS_CHECKING)

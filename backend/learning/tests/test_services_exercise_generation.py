from django.test import TestCase

from learning.models import Node, Rel, Situation, SituationRelation
from learning.services.exceptions import NoExercisableContent
from learning.services.exercise_generation import (
    generate_exercise_for_situation,
    get_examples,
    get_parts,
    get_translations,
)


def make_node(kind, language, content, **kwargs):
    return Node.objects.create(kind=kind, language=language, content=content, **kwargs)


class TranslationLookupTests(TestCase):
    def test_bidirectional_lookup(self):
        fra = make_node(Node.Kind.VOCAB, "fra", "chat")
        eng = make_node(Node.Kind.VOCAB, "eng", "cat")
        Rel.objects.create(sender=fra, receiver=eng, label=Rel.Label.TRANSLATION)

        self.assertEqual([n for n, _ in get_translations(fra)], [eng])
        # reverse direction: eng -> fra, target_language fra
        self.assertEqual([n for n, _ in get_translations(eng, target_language="fra")], [fra])

    def test_filters_by_kind_and_language(self):
        fra_vocab = make_node(Node.Kind.VOCAB, "fra", "chat")
        eng_sentence = make_node(Node.Kind.SENTENCE, "eng", "The cat sleeps.")
        deu_vocab = make_node(Node.Kind.VOCAB, "deu", "Katze")
        Rel.objects.create(sender=fra_vocab, receiver=eng_sentence, label=Rel.Label.TRANSLATION)
        Rel.objects.create(sender=fra_vocab, receiver=deu_vocab, label=Rel.Label.TRANSLATION)

        self.assertEqual(get_translations(fra_vocab), [])  # no eng VOCAB translation


class ExampleAndPartLookupTests(TestCase):
    def test_get_examples_direction(self):
        vocab = make_node(Node.Kind.VOCAB, "fra", "chat")
        sentence = make_node(Node.Kind.SENTENCE, "fra", "Le chat dort.")
        Rel.objects.create(sender=sentence, receiver=vocab, label=Rel.Label.EXAMPLE)

        self.assertEqual([n for n, _ in get_examples(vocab)], [sentence])

    def test_get_parts_direction(self):
        sentence = make_node(Node.Kind.SENTENCE, "fra", "Le chat dort.")
        part = make_node(Node.Kind.VOCAB, "fra", "chat")
        Rel.objects.create(sender=part, receiver=sentence, label=Rel.Label.PART_OF)

        self.assertEqual([n for n, _ in get_parts(sentence)], [part])


class GenerateExerciseForSituationTests(TestCase):
    def setUp(self):
        self.situation = Situation.objects.create(language="fra", description="Test")

    def test_no_exercisable_content_raises(self):
        with self.assertRaises(NoExercisableContent):
            generate_exercise_for_situation(self.situation)

    def test_low_relevance_excluded(self):
        node = make_node(Node.Kind.VOCAB, "fra", "chat")
        eng = make_node(Node.Kind.VOCAB, "eng", "cat")
        Rel.objects.create(sender=node, receiver=eng, label=Rel.Label.TRANSLATION)
        SituationRelation.objects.create(situation=self.situation, node=node, relevance=1)

        with self.assertRaises(NoExercisableContent):
            generate_exercise_for_situation(self.situation)

    def test_vocab_exercise_generated(self):
        node = make_node(Node.Kind.VOCAB, "fra", "chat", credit="dict")
        eng = make_node(Node.Kind.VOCAB, "eng", "cat")
        Rel.objects.create(sender=node, receiver=eng, label=Rel.Label.TRANSLATION)
        SituationRelation.objects.create(situation=self.situation, node=node, relevance=3)

        exercise = generate_exercise_for_situation(self.situation)
        self.assertEqual(exercise.kind, "FlashcardVocab")
        self.assertIn("## chat", exercise.front)
        self.assertIn("### cat", exercise.back)
        self.assertIn("dict", exercise.credits)

    def test_sentence_without_translation_excluded_from_pool(self):
        sentence = make_node(Node.Kind.SENTENCE, "fra", "Le chat dort.")
        SituationRelation.objects.create(situation=self.situation, node=sentence, relevance=5)

        with self.assertRaises(NoExercisableContent):
            generate_exercise_for_situation(self.situation)

    def test_sentence_exercise_generated_with_parts(self):
        sentence = make_node(Node.Kind.SENTENCE, "fra", "Le chat dort.")
        eng_sentence = make_node(Node.Kind.SENTENCE, "eng", "The cat sleeps.")
        Rel.objects.create(sender=sentence, receiver=eng_sentence, label=Rel.Label.TRANSLATION)

        part = make_node(Node.Kind.VOCAB, "fra", "chat")
        eng_part = make_node(Node.Kind.VOCAB, "eng", "cat")
        Rel.objects.create(sender=part, receiver=sentence, label=Rel.Label.PART_OF)
        Rel.objects.create(sender=part, receiver=eng_part, label=Rel.Label.TRANSLATION)

        SituationRelation.objects.create(situation=self.situation, node=sentence, relevance=5)

        exercise = generate_exercise_for_situation(self.situation)
        self.assertEqual(exercise.kind, "FlashcardSentence")
        self.assertIn("#### Le chat dort.", exercise.front)
        self.assertIn("### The cat sleeps.", exercise.back)
        self.assertIn("**chat**\ncat", exercise.back)

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from learning.models import Node, Rel, Situation, SituationRelation
from learning.models.validators import validate_iso639_3


class NodeModelTests(TestCase):
    def test_unique_kind_language_content(self):
        Node.objects.create(kind=Node.Kind.VOCAB, language="fra", content="chat")
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Node.objects.create(kind=Node.Kind.VOCAB, language="fra", content="chat")

    def test_default_state_is_needs_checking(self):
        node = Node.objects.create(kind=Node.Kind.VOCAB, language="fra", content="chien")
        self.assertEqual(node.state, Node.State.NEEDS_CHECKING)

    def test_invalid_language_rejected(self):
        with self.assertRaises(ValidationError):
            validate_iso639_3("xx")

    def test_valid_language_accepted(self):
        validate_iso639_3("fra")  # should not raise


class RelModelTests(TestCase):
    def test_unique_sender_receiver_label(self):
        a = Node.objects.create(kind=Node.Kind.VOCAB, language="fra", content="chat")
        b = Node.objects.create(kind=Node.Kind.VOCAB, language="eng", content="cat")
        Rel.objects.create(sender=a, receiver=b, label=Rel.Label.TRANSLATION)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Rel.objects.create(sender=a, receiver=b, label=Rel.Label.TRANSLATION)

    def test_state_choices_are_separate_from_node(self):
        self.assertEqual(
            {c[0] for c in Rel.State.choices}, {c[0] for c in Node.State.choices}
        )
        self.assertIsNot(Rel.State, Node.State)


class SituationRelationModelTests(TestCase):
    def test_relevance_out_of_range_rejected_by_full_clean(self):
        situation = Situation.objects.create(language="fra", description="Test situation")
        node = Node.objects.create(kind=Node.Kind.VOCAB, language="fra", content="chat")
        rel = SituationRelation(situation=situation, node=node, relevance=6)
        with self.assertRaises(ValidationError):
            rel.full_clean()

    def test_unique_situation_node(self):
        situation = Situation.objects.create(language="fra", description="Test situation")
        node = Node.objects.create(kind=Node.Kind.VOCAB, language="fra", content="chat")
        SituationRelation.objects.create(situation=situation, node=node, relevance=3)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                SituationRelation.objects.create(situation=situation, node=node, relevance=4)

import random
from dataclasses import dataclass

from django.db.models import Q

from learning.models import Node, Rel, Situation

from .exceptions import NoExercisableContent

ENG = "eng"


@dataclass
class Exercise:
    kind: str
    front: str
    back: str
    credits: str
    node_id: int


def _translation_rels(node: Node):
    return Rel.objects.filter(
        Q(sender=node) | Q(receiver=node), label=Rel.Label.TRANSLATION
    ).select_related("sender", "receiver")


def get_translations(node: Node, target_language: str = ENG) -> list[tuple[Node, Rel]]:
    """(other_node, rel) pairs where the other side is in target_language & the same kind.

    TRANSLATION rels are treated as bidirectional since translation is inherently
    symmetric and the spec doesn't specify a sender/receiver direction for it.
    """
    pairs = []
    for rel in _translation_rels(node):
        other = rel.receiver if rel.sender_id == node.id else rel.sender
        if other.language == target_language and other.kind == node.kind:
            pairs.append((other, rel))
    return pairs


def get_examples(vocab_node: Node) -> list[tuple[Node, Rel]]:
    """(example_sentence, rel) pairs: sender is an EXAMPLE of vocab_node, same language."""
    rels = (
        Rel.objects.filter(
            receiver=vocab_node,
            label=Rel.Label.EXAMPLE,
            sender__language=vocab_node.language,
        )
        .select_related("sender")
        .order_by("id")
    )
    return [(rel.sender, rel) for rel in rels]


def get_parts(sentence_node: Node) -> list[tuple[Node, Rel]]:
    """(part_node, rel) pairs: sender is PART_OF sentence_node, in creation order."""
    rels = (
        Rel.objects.filter(receiver=sentence_node, label=Rel.Label.PART_OF)
        .select_related("sender")
        .order_by("id")
    )
    return [(rel.sender, rel) for rel in rels]


def _render_translation_block(node: Node, rel: Rel) -> str:
    text = f"### {node.content}\n"
    text += f"*{rel.note}*\n\n" if rel.note else "\n"
    return text


def _render_example_block(example_node: Node, translation_node: Node) -> str:
    return f"**{example_node.content}**\n{translation_node.content}\n\n"


def _collect_credits(*credits: str | None) -> str:
    return "; ".join(c.strip() for c in credits if c and c.strip())


def build_vocab_exercise(node: Node) -> Exercise:
    front = f"What does this mean?\n\n## {node.content}"

    translations = get_translations(node)
    random.shuffle(translations)
    translations = translations[:3]

    examples = get_examples(node)
    random.shuffle(examples)
    usable_examples: list[tuple[Node, Node]] = []
    for example_node, _example_rel in examples:
        example_translations = get_translations(example_node)
        if not example_translations:
            continue  # spec: do not return sentences without a translation
        translation_node, _ = random.choice(example_translations)
        usable_examples.append((example_node, translation_node))
        if len(usable_examples) == 2:
            break

    back = "".join(_render_translation_block(n, r) for n, r in translations)
    back += "".join(
        _render_example_block(example, translation)
        for example, translation in usable_examples
    )

    credits = [node.credit]
    for translation_node, translation_rel in translations:
        credits += [translation_node.credit, translation_rel.credit]
    for example_node, translation_node in usable_examples:
        credits += [example_node.credit, translation_node.credit]

    return Exercise(
        kind="FlashcardVocab",
        front=front,
        back=back,
        credits=_collect_credits(*credits),
        node_id=node.id,
    )


def build_sentence_exercise(node: Node) -> Exercise:
    front = f"What does this mean?\n\n#### {node.content}"

    translations = get_translations(node)
    if not translations:
        raise NoExercisableContent(f"Node {node.id} has no {ENG} translation.")
    translation_node, translation_rel = random.choice(translations)

    parts = get_parts(node)
    usable_parts: list[tuple[Node, Node]] = []
    for part_node, _part_rel in parts:
        part_translations = get_translations(part_node)
        if not part_translations:
            continue
        part_translation_node, _ = random.choice(part_translations)
        usable_parts.append((part_node, part_translation_node))

    back = _render_translation_block(translation_node, translation_rel)
    back += "".join(
        _render_example_block(part, translation) for part, translation in usable_parts
    )

    credits = [node.credit, translation_node.credit, translation_rel.credit]
    for part_node, part_translation_node in usable_parts:
        credits += [part_node.credit, part_translation_node.credit]

    return Exercise(
        kind="FlashcardSentence",
        front=front,
        back=back,
        credits=_collect_credits(*credits),
        node_id=node.id,
    )


def _eligible_node_ids(situation: Situation) -> list[int]:
    # Node/Rel `state` (TRUSTED/NEEDS_CHECKING) is intentionally NOT filtered here —
    # spec doesn't call for it in exercise generation.
    # TODO(v2): consider .filter(state=Node.State.TRUSTED) once a content review
    # workflow exists.
    candidates = Node.objects.filter(
        situation_relations__situation=situation,
        situation_relations__relevance__gte=2,
    ).distinct()

    ids = []
    for node in candidates.only("id", "kind", "language"):
        if node.kind == Node.Kind.SENTENCE and not get_translations(node):
            continue  # unusable: can't build a FlashcardSentence without a translation
        ids.append(node.id)
    return ids


def generate_exercise_for_situation(situation: Situation) -> Exercise:
    ids = _eligible_node_ids(situation)
    if not ids:
        raise NoExercisableContent(
            f"Situation {situation.id} has no exercisable content."
        )
    node = Node.objects.get(pk=random.choice(ids))
    if node.kind == Node.Kind.VOCAB:
        return build_vocab_exercise(node)
    return build_sentence_exercise(node)


def _build_exercise(node: Node) -> Exercise:
    if node.kind == Node.Kind.VOCAB:
        return build_vocab_exercise(node)
    return build_sentence_exercise(node)


def generate_exercise_pool(
    situations: list[Situation],
) -> list[tuple[Exercise, set[int]]]:
    """One Exercise per unique eligible Node across all given situations, paired
    with the ids of every situation it's eligible under (a node can be relevant to
    more than one situation)."""
    situation_ids_by_node: dict[int, set[int]] = {}
    for situation in situations:
        for node_id in _eligible_node_ids(situation):
            situation_ids_by_node.setdefault(node_id, set()).add(situation.id)

    nodes = Node.objects.in_bulk(situation_ids_by_node.keys())
    return [
        (_build_exercise(nodes[node_id]), situation_ids)
        for node_id, situation_ids in situation_ids_by_node.items()
    ]

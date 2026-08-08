from dataclasses import dataclass

from django.db import transaction

from learning.models import Node, Rel, Situation, SituationRelation

from . import generation
from .merge import merge_field

ENG = "eng"
DIRECT_RELEVANCE = 3
ADJACENT_RELEVANCE = 2


@dataclass
class AddContentResult:
    situation_id: int
    node_id: int | None
    generation_error: str | None = None

    def as_dict(self) -> dict:
        return {
            "situation_id": self.situation_id,
            "node_id": self.node_id,
            "generation_error": self.generation_error,
        }


def _get_or_create_node(kind: str, language: str, content: str, state: str = Node.State.NEEDS_CHECKING):
    return Node.objects.get_or_create(
        kind=kind, language=language, content=content, defaults={"state": state}
    )


def _link_translation(sender: Node, receiver: Node, note: str, state: str) -> Rel:
    rel, created = Rel.objects.get_or_create(
        sender=sender,
        receiver=receiver,
        label=Rel.Label.TRANSLATION,
        defaults={"note": note, "state": state},
    )
    if not created and note:
        merged_note = merge_field(rel.note, note)
        if merged_note != rel.note:
            rel.note = merged_note
            rel.save(update_fields=["note"])
    return rel


def _link_part_example(word_node: Node, sentence_node: Node, state: str) -> None:
    Rel.objects.get_or_create(
        sender=word_node, receiver=sentence_node, label=Rel.Label.PART_OF, defaults={"state": state}
    )
    Rel.objects.get_or_create(
        sender=sentence_node, receiver=word_node, label=Rel.Label.EXAMPLE, defaults={"state": state}
    )


def _link_situation(situation: Situation, node: Node, relevance: int) -> None:
    SituationRelation.objects.get_or_create(
        situation=situation, node=node, defaults={"relevance": relevance}
    )


@transaction.atomic
def _create_base(
    kind: str, language: str, situation_description: str, content: str, translations: list[dict]
) -> tuple[Situation, Node | None, list[tuple[Node, str]]]:
    situation, _ = Situation.objects.get_or_create(
        language=language,
        description=situation_description.strip()
        or f"General {generation.language_display_name(language)}",
    )

    main_node = None
    if content.strip():
        main_node, _ = _get_or_create_node(kind, language, content.strip())

    translation_nodes: list[tuple[Node, str]] = []
    for row in translations:
        row_content = row.get("content", "").strip()
        if not row_content:
            continue
        translation_node, _ = _get_or_create_node(kind, ENG, row_content)
        translation_nodes.append((translation_node, row.get("note", "").strip()))

    if main_node is not None:
        for translation_node, note in translation_nodes:
            _link_translation(main_node, translation_node, note, Rel.State.NEEDS_CHECKING)
        _link_situation(situation, main_node, DIRECT_RELEVANCE)

    return situation, main_node, translation_nodes


def _split_sentence(
    *, api_key: str, language: str, situation: Situation, sentence_node: Node, translation_text: str
) -> None:
    parts = generation.extract_vocab(
        api_key=api_key,
        sentence=sentence_node.content,
        translation=translation_text,
        language=language,
    )
    for part in parts:
        word_node, _ = _get_or_create_node(
            Node.Kind.VOCAB, language, part["word"], state=Node.State.AUTO_GENERATED
        )
        _link_part_example(word_node, sentence_node, Rel.State.AUTO_GENERATED)
        _link_situation(situation, word_node, ADJACENT_RELEVANCE)
        if part["translation"]:
            eng_node, _ = _get_or_create_node(
                Node.Kind.VOCAB, ENG, part["translation"], state=Node.State.AUTO_GENERATED
            )
            _link_translation(word_node, eng_node, part["note"], Rel.State.AUTO_GENERATED)


def _add_examples(
    *, api_key: str, language: str, situation: Situation, word_node: Node, translation_text: str
) -> None:
    examples = generation.generate_examples(
        api_key=api_key,
        word=word_node.content,
        translation=translation_text,
        language=language,
    )
    for example in examples:
        sentence_node, _ = _get_or_create_node(
            Node.Kind.SENTENCE, language, example["sentence"], state=Node.State.AUTO_GENERATED
        )
        _link_part_example(word_node, sentence_node, Rel.State.AUTO_GENERATED)
        _link_situation(situation, sentence_node, ADJACENT_RELEVANCE)
        if example["translation"]:
            eng_node, _ = _get_or_create_node(
                Node.Kind.SENTENCE, ENG, example["translation"], state=Node.State.AUTO_GENERATED
            )
            _link_translation(sentence_node, eng_node, example["note"], Rel.State.AUTO_GENERATED)


def _generate(
    *,
    api_key: str,
    kind: str,
    language: str,
    situation: Situation,
    main_node: Node | None,
    translation_nodes: list[tuple[Node, str]],
) -> Node | None:
    if main_node is None:
        if not translation_nodes:
            return None
        seed_translation_node, _ = translation_nodes[0]
        result = generation.translate_missing(
            api_key=api_key,
            kind=kind,
            source_language=ENG,
            target_language=language,
            text=seed_translation_node.content,
        )
        if not result:
            return None
        main_node, _ = _get_or_create_node(
            kind, language, result["content"], state=Node.State.AUTO_GENERATED
        )
        for translation_node, note in translation_nodes:
            _link_translation(main_node, translation_node, note, Rel.State.AUTO_GENERATED)
        _link_situation(situation, main_node, DIRECT_RELEVANCE)

    if not translation_nodes:
        result = generation.translate_missing(
            api_key=api_key,
            kind=kind,
            source_language=language,
            target_language=ENG,
            text=main_node.content,
        )
        if result:
            translation_node, _ = _get_or_create_node(
                kind, ENG, result["content"], state=Node.State.AUTO_GENERATED
            )
            _link_translation(main_node, translation_node, result["note"], Rel.State.AUTO_GENERATED)
            translation_nodes = [(translation_node, result["note"])]

    translation_text = translation_nodes[0][0].content if translation_nodes else ""

    if kind == Node.Kind.SENTENCE:
        _split_sentence(
            api_key=api_key,
            language=language,
            situation=situation,
            sentence_node=main_node,
            translation_text=translation_text,
        )
    elif kind == Node.Kind.VOCAB and translation_text:
        _add_examples(
            api_key=api_key,
            language=language,
            situation=situation,
            word_node=main_node,
            translation_text=translation_text,
        )

    return main_node


def add_content(
    *,
    kind: str,
    language: str,
    situation_description: str,
    content: str,
    translations: list[dict],
    api_key: str,
) -> AddContentResult:
    situation, main_node, translation_nodes = _create_base(
        kind, language, situation_description, content, translations
    )

    generation_error = None
    api_key = (api_key or "").strip()
    if api_key:
        try:
            main_node = (
                _generate(
                    api_key=api_key,
                    kind=kind,
                    language=language,
                    situation=situation,
                    main_node=main_node,
                    translation_nodes=translation_nodes,
                )
                or main_node
            )
        except Exception as exc:  # AI augmentation must never lose the user's saved data
            generation_error = str(exc)

    return AddContentResult(
        situation_id=situation.id,
        node_id=main_node.id if main_node else None,
        generation_error=generation_error,
    )

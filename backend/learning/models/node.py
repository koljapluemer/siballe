from django.db import models

from .validators import validate_iso639_3


class Node(models.Model):
    """A single piece of learning content: vocab, a sentence, etc."""

    class Kind(models.TextChoices):
        VOCAB = "VOCAB", "Vocabulary"
        SENTENCE = "SENTENCE", "Sentence"

    class State(models.TextChoices):
        TRUSTED = "TRUSTED", "Trusted"
        NEEDS_CHECKING = "NEEDS_CHECKING", "Needs checking"
        AUTO_GENERATED = "AUTO_GENERATED", "Auto-generated"

    kind = models.CharField(max_length=16, choices=Kind.choices)
    language = models.CharField(max_length=3, validators=[validate_iso639_3])
    content = models.TextField()
    credit = models.TextField(blank=True, default="")
    state = models.CharField(
        max_length=16, choices=State.choices, default=State.NEEDS_CHECKING
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["kind", "language", "content"],
                name="unique_node_kind_language_content",
            ),
        ]

    def __str__(self) -> str:
        return f"[{self.kind}:{self.language}] {self.content[:40]}"

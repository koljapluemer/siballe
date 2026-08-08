from django.db import models

from .node import Node


class Rel(models.Model):
    """A directed relationship between two Nodes."""

    class Label(models.TextChoices):
        EXAMPLE = "EXAMPLE", "Example"
        PART_OF = "PART_OF", "Part of"
        TRANSLATION = "TRANSLATION", "Translation"

    class State(models.TextChoices):
        TRUSTED = "TRUSTED", "Trusted"
        NEEDS_CHECKING = "NEEDS_CHECKING", "Needs checking"
        AUTO_GENERATED = "AUTO_GENERATED", "Auto-generated"

    sender = models.ForeignKey(
        Node, on_delete=models.CASCADE, related_name="outgoing_rels"
    )
    receiver = models.ForeignKey(
        Node, on_delete=models.CASCADE, related_name="incoming_rels"
    )
    label = models.CharField(max_length=16, choices=Label.choices)
    note = models.TextField(blank=True, default="")
    credit = models.TextField(blank=True, default="")
    state = models.CharField(
        max_length=16, choices=State.choices, default=State.NEEDS_CHECKING
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["sender", "receiver", "label"],
                name="unique_rel_sender_receiver_label",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.sender_id} -{self.label}-> {self.receiver_id}"

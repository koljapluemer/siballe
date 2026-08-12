from django.db import models

from .node import Node
from .user import User


class ExerciseProgress(models.Model):
    """A user's FSRS review state for one exercise (keyed by its source Node).

    `card_data` is an opaque payload straight from the client's fsrs Card — the
    server never interprets FSRS internals, it only stores and relays them between
    a user's devices. `due` is denormalized out of `card_data` purely for admin
    visibility. `client_updated_at` is the last-write-wins comparator: it's the
    client's local review time, not a server-side auto_now, since sync must compare
    against when the review actually happened, not when it happened to sync.
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="exercise_progress"
    )
    node = models.ForeignKey(
        Node, on_delete=models.CASCADE, related_name="exercise_progress"
    )
    card_data = models.JSONField()
    due = models.DateTimeField()
    client_updated_at = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "node"], name="unique_user_node_progress"
            ),
        ]

    def __str__(self) -> str:
        return f"{self.user_id}:{self.node_id} due {self.due:%Y-%m-%d}"

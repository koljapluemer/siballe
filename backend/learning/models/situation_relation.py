from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .node import Node
from .situation import Situation


class SituationRelation(models.Model):
    situation = models.ForeignKey(
        Situation, on_delete=models.CASCADE, related_name="situation_relations"
    )
    node = models.ForeignKey(
        Node, on_delete=models.CASCADE, related_name="situation_relations"
    )
    relevance = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["situation", "node"], name="unique_situation_relation"
            ),
        ]

    def __str__(self) -> str:
        return f"{self.situation_id} <-{self.relevance}-> {self.node_id}"

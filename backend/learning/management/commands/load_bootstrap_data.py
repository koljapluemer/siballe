import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from learning.models import Node, Rel, Situation, SituationRelation

DEFAULT_FIXTURE = (
    Path(__file__).resolve().parent.parent.parent
    / "fixtures"
    / "bootstrap"
    / "fra_smalltalk.json"
)

# node field -> (Rel label, direction) where direction says which side the
# *current* node plays: "sender" or "receiver". The other side is the referenced key.
RELATION_FIELDS = {
    "translations": (Rel.Label.TRANSLATION, "sender"),
    "examples": (Rel.Label.EXAMPLE, "receiver"),  # sender = example sentence
    "parts": (Rel.Label.PART_OF, "receiver"),  # sender = the part
}


class Command(BaseCommand):
    help = "Idempotently load bootstrap Node/Rel/Situation data from a bespoke JSON fixture."

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=Path,
            default=DEFAULT_FIXTURE,
            help="Path to a bootstrap JSON fixture (default: bundled fra_smalltalk.json).",
        )

    def handle(self, *args, **options):
        path: Path = options["file"]
        if not path.exists():
            raise CommandError(f"Fixture file not found: {path}")

        data = json.loads(path.read_text())

        nodes_by_key = self._load_nodes(data.get("nodes", []))
        rel_count = self._load_relations(data.get("nodes", []), nodes_by_key)
        situation_count, relation_count = self._load_situations(
            data.get("situations", []), nodes_by_key
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Loaded {len(nodes_by_key)} nodes, {rel_count} rels, "
                f"{situation_count} situations, {relation_count} situation relations "
                f"from {path.name}"
            )
        )

    def _load_nodes(self, node_entries: list[dict]) -> dict[str, Node]:
        nodes_by_key = {}
        for entry in node_entries:
            node, _ = Node.objects.update_or_create(
                kind=entry["kind"],
                language=entry["language"],
                content=entry["content"],
                defaults={
                    "credit": entry.get("credit", ""),
                    "state": entry.get("state", Node.State.NEEDS_CHECKING),
                },
            )
            nodes_by_key[entry["key"]] = node
        return nodes_by_key

    def _load_relations(
        self, node_entries: list[dict], nodes_by_key: dict[str, Node]
    ) -> int:
        count = 0
        for entry in node_entries:
            node = nodes_by_key[entry["key"]]
            for field, (label, current_side) in RELATION_FIELDS.items():
                for rel_entry in entry.get(field, []):
                    other = nodes_by_key[rel_entry["key"]]
                    sender, receiver = (
                        (node, other) if current_side == "sender" else (other, node)
                    )
                    Rel.objects.get_or_create(
                        sender=sender,
                        receiver=receiver,
                        label=label,
                        defaults={
                            "note": rel_entry.get("note", ""),
                            "credit": rel_entry.get("credit", ""),
                            "state": rel_entry.get("state", Rel.State.TRUSTED),
                        },
                    )
                    count += 1
        return count

    def _load_situations(
        self, situation_entries: list[dict], nodes_by_key: dict[str, Node]
    ) -> tuple[int, int]:
        situation_count = 0
        relation_count = 0
        for entry in situation_entries:
            situation, _ = Situation.objects.update_or_create(
                description=entry["description"],
                defaults={"language": entry["language"]},
            )
            situation_count += 1
            for rel_entry in entry.get("relations", []):
                SituationRelation.objects.update_or_create(
                    situation=situation,
                    node=nodes_by_key[rel_entry["node"]],
                    defaults={"relevance": rel_entry["relevance"]},
                )
                relation_count += 1
        return situation_count, relation_count

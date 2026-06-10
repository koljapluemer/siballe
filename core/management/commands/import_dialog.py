import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from core.models import (
    Dialog, DialogLine, DialogUtterance,
    Language, Sentence, Situation, SituationalUtterance, SpeechAct,
)


class Command(BaseCommand):
    help = "Import a dialog from a JSON file (skips if dialog already exists)."

    def add_arguments(self, parser):
        parser.add_argument("file", nargs="+", type=Path, help="Path(s) to dialog JSON file(s)")

    def handle(self, *args, **options):
        for path in options["file"]:
            try:
                self._import(path)
            except Exception as exc:
                raise CommandError(f"{path}: {exc}") from exc

    def _import(self, path: Path):
        data = json.loads(path.read_text())

        language = Language.objects.get(iso3=data["language"])

        situation, _ = Situation.objects.get_or_create(
            description=data["situation"],
            language=language,
        )

        if Dialog.objects.filter(name=data["name"], situation=situation).exists():
            self.stdout.write(f"skip  {path.name} — dialog already exists")
            return

        dialog = Dialog.objects.create(
            situation=situation,
            name=data["name"],
            learner_role=data.get("learner_role", ""),
            other_role=data.get("other_role", ""),
        )

        raw = data["utterances"]
        nodes: dict[str, DialogUtterance] = {}

        # First pass: create utterance nodes, their lines, and situational utterances.
        for i, entry in enumerate(raw):
            file_id = entry.get("id", str(i))
            speech_act, _ = SpeechAct.objects.get_or_create(description=entry["speech_act"])

            node = DialogUtterance.objects.create(
                dialog=dialog,
                speaker=entry["speaker"],
                speech_act=speech_act,
            )
            nodes[file_id] = node

            lines = _resolve_lines(entry)
            for order, (content, context) in enumerate(lines):
                sentence, _ = Sentence.objects.get_or_create(
                    content=content,
                    language=language,
                )
                DialogLine.objects.create(
                    utterance=node,
                    sentence=sentence,
                    context=context,
                    order=order,
                )
                SituationalUtterance.objects.update_or_create(
                    situation=situation,
                    speech_act=speech_act,
                    sentence=sentence,
                    defaults={"context": context},
                )

        # Second pass: wire previous_utterances.
        for i, entry in enumerate(raw):
            file_id = entry.get("id", str(i))
            node = nodes[file_id]

            if "after" in entry:
                after = entry["after"]
                predecessors = [after] if isinstance(after, str) else after
                node.previous_utterances.set(nodes[p] for p in predecessors)
            elif i > 0:
                prev_id = raw[i - 1].get("id", str(i - 1))
                node.previous_utterances.set([nodes[prev_id]])

        start_id = raw[0].get("id", "0")
        dialog.start_utterance = nodes[start_id]
        dialog.save()

        self.stdout.write(f"import {path.name} — {len(nodes)} utterance(s)")


def _resolve_lines(entry: dict) -> list[tuple[str, str]]:
    """Return (content, context) pairs from either 'lines' or 'text'."""
    if "lines" in entry:
        return [(line["content"], line.get("context", "")) for line in entry["lines"]]
    if "text" in entry:
        return [(entry["text"], entry.get("context", ""))]
    raise ValueError(f"utterance '{entry.get('id', '?')}' has neither 'text' nor 'lines'")

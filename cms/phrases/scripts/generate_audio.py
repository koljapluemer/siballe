"""Generate ElevenLabs TTS audio for every target-language phrase in
public/data/phrases/<iso3>/*.json.

Run via: uv run python phrases/scripts/generate_audio.py

Each phrase file nests target-language phrases as keys of an "expressions"
object, at any depth. For every phrase found, writes an mp3 to a sibling
audio/ folder (public/data/phrases/<iso3>/audio/), named after a slug of
the phrase text. Phrases whose audio file already exists are skipped, so
reruns only fill in new phrases.

Batch counterpart to the CMS app's per-phrase "Generate audio" button -
see ../audio.py for the filename convention and generation details, which
this script reuses.
"""

import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from audio import audio_path, fetch_voices, generate_audio_bytes, iso3_to_iso1  # noqa: E402
from data_io import phrases_dir  # noqa: E402


def find_phrases(node: object) -> set[str]:
    phrases: set[str] = set()
    if isinstance(node, dict):
        expressions = node.get("expressions")
        if isinstance(expressions, dict):
            phrases.update(expressions.keys())
        for value in node.values():
            phrases.update(find_phrases(value))
    elif isinstance(node, list):
        for item in node:
            phrases.update(find_phrases(item))
    return phrases


def process_language(lang_dir: Path) -> None:
    phrases: set[str] = set()
    for json_file in lang_dir.glob("*.json"):
        phrases.update(find_phrases(json.loads(json_file.read_text())))
    if not phrases:
        return

    pending = [p for p in phrases if not audio_path(lang_dir.name, p).exists()]
    skipped = len(phrases) - len(pending)
    if not pending:
        print(f"{lang_dir.name}: {skipped} phrase(s) already have audio, nothing to do")
        return

    voices = fetch_voices(iso3_to_iso1(lang_dir.name))
    if not voices:
        print(f"{lang_dir.name}: no ElevenLabs voices available, skipping")
        return

    for phrase in pending:
        voice = random.choice(voices)
        audio = generate_audio_bytes(phrase, voice["voice_id"])
        path = audio_path(lang_dir.name, phrase)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(audio)
        print(f"{lang_dir.name}: generated '{phrase}' with voice '{voice['name']}'")

    print(f"{lang_dir.name}: generated {len(pending)}, skipped {skipped} already-present")


def main() -> None:
    for lang_dir in sorted(p for p in phrases_dir().iterdir() if p.is_dir()):
        process_language(lang_dir)


if __name__ == "__main__":
    main()

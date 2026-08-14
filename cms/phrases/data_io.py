"""Load/save the phrases content directly under public/data/phrases/<iso3>/.

Unlike world_map, there's no separate CMS source-of-truth + export step:
these JSON files ARE the frontend-facing files, so load_*/save_* read and
write them in place.

Per language (public/data/phrases/<iso3>/):
- index.json: situation slug -> display name (e.g.
  {"arriving-as-a-tourist-in-albania": "Arriving as a tourist in Albania"})
- <slug>.json: that situation's content, a dict of communication goal
  (e.g. "Excuse me") -> {"expressions": {target-language phrase: {"note":
  optional str}}}
- audio/: mp3s for target-language phrases, named by audio.audio_filename
  (see that module) - a plain slug of the phrase text, shared across every
  situation in the language, since the same phrase may appear under
  multiple goals/situations.
"""

import json
import re
from pathlib import Path
from typing import TypedDict


class ExpressionEntry(TypedDict, total=False):
    note: str


class GoalEntry(TypedDict):
    expressions: dict[str, ExpressionEntry]


SituationContent = dict[str, GoalEntry]
LanguageIndex = dict[str, str]


def find_repo_root() -> Path:
    current = Path(__file__).resolve()
    for candidate in current.parents:
        if (candidate / "package.json").exists():
            return candidate
    raise FileNotFoundError("no package.json found above cms/phrases")


def phrases_dir() -> Path:
    return find_repo_root() / "public" / "data" / "phrases"


def language_dir(iso3: str) -> Path:
    return phrases_dir() / iso3


def index_path(iso3: str) -> Path:
    return language_dir(iso3) / "index.json"


def situation_path(iso3: str, slug: str) -> Path:
    return language_dir(iso3) / f"{slug}.json"


def audio_dir(iso3: str) -> Path:
    return language_dir(iso3) / "audio"


def list_languages() -> list[str]:
    if not phrases_dir().exists():
        return []
    return sorted(p.name for p in phrases_dir().iterdir() if p.is_dir() and (p / "index.json").exists())


def create_language(iso3: str) -> None:
    audio_dir(iso3).mkdir(parents=True, exist_ok=True)
    if not index_path(iso3).exists():
        save_index(iso3, {})


def load_index(iso3: str) -> LanguageIndex:
    path = index_path(iso3)
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def save_index(iso3: str, index: LanguageIndex) -> None:
    path = index_path(iso3)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n")


def load_situation(iso3: str, slug: str) -> SituationContent:
    path = situation_path(iso3, slug)
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def save_situation(iso3: str, slug: str, content: SituationContent) -> None:
    path = situation_path(iso3, slug)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(content, ensure_ascii=False, indent=2) + "\n")


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "situation"


def unique_slug(base_slug: str, existing: set[str]) -> str:
    if base_slug not in existing:
        return base_slug
    n = 2
    while f"{base_slug}-{n}" in existing:
        n += 1
    return f"{base_slug}-{n}"


def create_situation(iso3: str, name: str) -> str:
    index = load_index(iso3)
    slug = unique_slug(slugify(name), set(index.keys()))
    index[slug] = name
    save_index(iso3, index)
    save_situation(iso3, slug, {})
    return slug


def rename_situation(iso3: str, slug: str, new_name: str) -> None:
    index = load_index(iso3)
    index[slug] = new_name
    save_index(iso3, index)


def delete_situation(iso3: str, slug: str) -> None:
    index = load_index(iso3)
    index.pop(slug, None)
    save_index(iso3, index)
    path = situation_path(iso3, slug)
    if path.exists():
        path.unlink()


def rename_key(d: dict, old_key: str, new_key: str) -> dict:
    """Rename a dict key, preserving insertion order (goal/expression order is meaningful content order)."""
    return {new_key if k == old_key else k: v for k, v in d.items()}

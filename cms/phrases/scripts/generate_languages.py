"""Write public/data/phrases/languages.json: iso3 -> English language name,
for every language that has at least one situation.

Run via: uv run python phrases/scripts/generate_languages.py
"""

import json
import sys
from pathlib import Path

import pycountry

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from data_io import list_languages, load_index, phrases_dir  # noqa: E402


def iso3_to_name(iso3: str) -> str:
    language = pycountry.languages.get(alpha_3=iso3)
    return language.name if language else iso3


def main() -> None:
    languages = {iso3: iso3_to_name(iso3) for iso3 in list_languages() if load_index(iso3)}
    path = phrases_dir() / "languages.json"
    path.write_text(json.dumps(languages, ensure_ascii=False, indent=2) + "\n")
    print(f"wrote {len(languages)} language(s) to {path}")


if __name__ == "__main__":
    main()

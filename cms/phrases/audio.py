"""ElevenLabs TTS generation for phrase audio.

Shared between the CMS app (single-phrase, on-demand generation for
whatever's missing) and scripts/generate_audio.py (batch-fills every
missing phrase across all languages). Audio files live in each language's
audio/ folder (see data_io.audio_dir), named after a slug of the phrase
text (audio_filename below), so the same phrase always resolves to the
same file regardless of which situation/goal it appears under. Collisions
aren't a concern for this app's phrase volume, so no uniqueness suffix.

Requires ELEVENLABS_API_KEY in a .env file at the repo root.
"""

import os
import random
import re
from pathlib import Path

import pycountry
import requests
from dotenv import load_dotenv

from data_io import audio_dir, find_repo_root

API_BASE = "https://api.elevenlabs.io"
MODEL_ID = "eleven_multilingual_v2"

load_dotenv(find_repo_root() / ".env")
API_KEY = os.environ.get("ELEVENLABS_API_KEY")
HEADERS = {"xi-api-key": API_KEY} if API_KEY else {}


def iso3_to_iso1(iso3: str) -> str | None:
    language = pycountry.languages.get(alpha_3=iso3)
    return getattr(language, "alpha_2", None) if language else None


def audio_filename(phrase: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", phrase.lower()).strip("-") or "phrase"
    return f"{slug}.mp3"


def audio_path(iso3: str, phrase: str) -> Path:
    return audio_dir(iso3) / audio_filename(phrase)


def has_audio(iso3: str, phrase: str) -> bool:
    return audio_path(iso3, phrase).exists()


def fetch_voices(iso1: str | None) -> list[dict]:
    params = {"page_size": 100}
    if iso1:
        params["language"] = iso1
    response = requests.get(f"{API_BASE}/v2/voices", headers=HEADERS, params=params)
    response.raise_for_status()
    voices = response.json()["voices"]
    if voices:
        return voices
    if iso1:
        return fetch_voices(None)
    return voices


def generate_audio_bytes(phrase: str, voice_id: str) -> bytes:
    response = requests.post(
        f"{API_BASE}/v1/text-to-speech/{voice_id}",
        headers={**HEADERS, "Content-Type": "application/json"},
        json={"text": phrase, "model_id": MODEL_ID},
    )
    response.raise_for_status()
    return response.content


def generate_missing_audio(iso3: str, phrase: str) -> Path:
    """Generate and save audio for a single phrase, for the CMS's
    per-phrase "Generate audio" button. Picks a random voice labeled for
    the language, falling back to any voice if none are labeled.
    """
    if not API_KEY:
        raise RuntimeError("ELEVENLABS_API_KEY is not set (add it to .env at the repo root)")
    voices = fetch_voices(iso3_to_iso1(iso3))
    if not voices:
        raise RuntimeError("no ElevenLabs voices available")
    voice = random.choice(voices)
    audio = generate_audio_bytes(phrase, voice["voice_id"])
    path = audio_path(iso3, phrase)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(audio)
    return path

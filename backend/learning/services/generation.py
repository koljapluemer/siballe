import json
import re

import pycountry
from django.conf import settings
from openai import OpenAI


def language_display_name(code: str) -> str:
    language = pycountry.languages.get(alpha_3=code)
    return language.name if language else code


def _ask(api_key: str, prompt: str) -> str:
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content or ""


def _extract_json(text: str, opening: str, closing: str):
    match = re.search(re.escape(opening) + r"[\s\S]*" + re.escape(closing), text)
    if not match:
        return None
    try:
        return json.loads(match.group(0))
    except (json.JSONDecodeError, ValueError):
        return None


def _str_field(row: dict, key: str) -> str:
    value = row.get(key, "")
    return value if isinstance(value, str) else ""


def translate_missing(
    *, api_key: str, kind: str, source_language: str, target_language: str, text: str
) -> dict | None:
    """Translate `text` from source_language into target_language.

    Returns {"content": ..., "note": ...} or None if generation failed.
    """
    item_word = "sentence" if kind == "SENTENCE" else "word/phrase"
    prompt = "\n".join(
        [
            f"Text: {text}",
            f"Source language: {language_display_name(source_language)}",
            f"Target language: {language_display_name(target_language)}",
            "",
            f"Translate the {item_word} above from the source language into the target language.",
            'Keep "content" to the plain translation - don\'t add parenthetical',
            "annotations (context notes, register, grammar notes, etc.) inside that field. If the",
            'translation genuinely needs that extra context, put it in an optional "note" field instead.',
            "Return ONLY a JSON object, no other text, in this exact format:",
            '{"content": "...", "note": "..."}',
        ]
    )
    parsed = _extract_json(_ask(api_key, prompt), "{", "}")
    if not isinstance(parsed, dict):
        return None
    content = _str_field(parsed, "content").strip()
    if not content:
        return None
    return {"content": content, "note": _str_field(parsed, "note").strip()}


def extract_vocab(*, api_key: str, sentence: str, translation: str, language: str) -> list[dict]:
    """Split a target-language sentence into vocab words, each with an eng translation."""
    prompt = "\n".join(
        [
            f"Sentence: {sentence}",
            f"Translation: {translation}",
            f"Language: {language_display_name(language)}",
            "",
            "Extract each vocabulary word from the sentence above, with its translation.",
            'Keep "word" and "translation" to the bare word/phrase - don\'t add parenthetical',
            "annotations (gender, register, grammar notes, etc.) inside those fields. If a word",
            'genuinely needs that extra context, put it in an optional "note" field instead.',
            "Return ONLY a JSON array, no other text, in this exact format:",
            '[{"word": "...", "translation": "...", "note": "..."}]',
        ]
    )
    parsed = _extract_json(_ask(api_key, prompt), "[", "]")
    if not isinstance(parsed, list):
        return []
    rows = []
    for row in parsed:
        if not isinstance(row, dict):
            continue
        word = _str_field(row, "word").strip()
        if not word:
            continue
        rows.append(
            {
                "word": word,
                "translation": _str_field(row, "translation").strip(),
                "note": _str_field(row, "note").strip(),
            }
        )
    return rows


def generate_examples(*, api_key: str, word: str, translation: str, language: str) -> list[dict]:
    """Generate example sentences (with eng translations) using `word`."""
    prompt = "\n".join(
        [
            f"Word: {word}",
            f"Translation: {translation}",
            f"Language: {language_display_name(language)}",
            "",
            "Give 3 example sentences in the word's language that use this word, each with its translation.",
            'Keep "sentence" and "translation" to the plain text - don\'t add parenthetical',
            "annotations (context notes, alternate readings, etc.) inside those fields. If a",
            'sentence genuinely needs that extra context, put it in an optional "note" field instead.',
            "Return ONLY a JSON array, no other text, in this exact format:",
            '[{"sentence": "...", "translation": "...", "note": "..."}]',
        ]
    )
    parsed = _extract_json(_ask(api_key, prompt), "[", "]")
    if not isinstance(parsed, list):
        return []
    rows = []
    for row in parsed:
        if not isinstance(row, dict):
            continue
        sentence = _str_field(row, "sentence").strip()
        if not sentence:
            continue
        rows.append(
            {
                "sentence": sentence,
                "translation": _str_field(row, "translation").strip(),
                "note": _str_field(row, "note").strip(),
            }
        )
    return rows

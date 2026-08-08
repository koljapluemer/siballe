import pycountry
from django.core.exceptions import ValidationError


def validate_iso639_3(value: str) -> None:
    if not pycountry.languages.get(alpha_3=value):
        raise ValidationError(f"{value!r} is not a valid ISO 639-3 language code.")

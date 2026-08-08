from django.db import models

from .validators import validate_iso639_3


class Situation(models.Model):
    language = models.CharField(max_length=3, validators=[validate_iso639_3])
    description = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"[{self.language}] {self.description}"

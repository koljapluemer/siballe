from django.db import models

from .building_block import language_code_validator


class Sentence(models.Model):
    content = models.TextField()
    language_code = models.CharField(max_length=3, validators=[language_code_validator])
    usage = models.TextField()

    def __str__(self):
        return f"[{self.language_code}] {self.content[:50]}"

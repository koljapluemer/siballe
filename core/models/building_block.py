from django.core.validators import RegexValidator
from django.db import models

language_code_validator = RegexValidator(
    r'^[a-zA-Z]{3}$',
    'Must be exactly 3 alphabetic characters.',
)


class BuildingBlock(models.Model):
    content = models.TextField()
    language_code = models.CharField(max_length=3, validators=[language_code_validator])
    usage = models.TextField()

    def __str__(self):
        return f"[{self.language_code}] {self.content[:50]}"

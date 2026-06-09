from django.db import models


class Sentence(models.Model):
    content = models.TextField()
    language = models.ForeignKey('Language', on_delete=models.PROTECT, related_name='sentences')

    def __str__(self):
        return f"[{self.language_id}] {self.content[:50]}"

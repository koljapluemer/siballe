from django.db import models


class BuildingBlock(models.Model):
    content = models.TextField()
    language = models.ForeignKey('Language', on_delete=models.PROTECT, related_name='building_blocks')
    usage = models.TextField()

    sentences = models.ManyToManyField('Sentence', blank=True, related_name='building_blocks')

    def __str__(self):
        return f"[{self.language_id}] {self.content[:50]}"

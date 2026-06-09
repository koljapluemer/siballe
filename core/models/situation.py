from django.db import models


class Situation(models.Model):
    description = models.TextField()
    language = models.ForeignKey('Language', null=True, on_delete=models.PROTECT, related_name='situations')

    def __str__(self):
        return self.description[:60]

from django.db import models


class Language(models.Model):
    iso3 = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.iso3})"

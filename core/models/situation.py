from django.db import models


class Situation(models.Model):
    description = models.TextField()

    def __str__(self):
        return self.description[:60]

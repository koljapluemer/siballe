from django.db import models


class DialogNode(models.Model):
    dialog = models.ForeignKey('Dialog', on_delete=models.CASCADE, related_name='nodes')
    speaker = models.TextField()

    def __str__(self):
        return f"{self.dialog.name} / {self.speaker}"

from django.db import models


class DialogLine(models.Model):
    utterance = models.ForeignKey('DialogUtterance', on_delete=models.CASCADE, related_name='lines')
    sentence = models.ForeignKey('Sentence', on_delete=models.CASCADE, related_name='dialog_lines')
    context = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return str(self.sentence)

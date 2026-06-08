from django.db import models


class SpeechAct(models.Model):
    description = models.TextField()
    situation = models.ForeignKey('Situation', on_delete=models.CASCADE, related_name='speech_acts')
    sentences = models.ManyToManyField('Sentence', blank=True, related_name='speech_acts')

    def __str__(self):
        return self.description[:60]

from django.db import models


class SituationalUtterance(models.Model):
    situation = models.ForeignKey('Situation', on_delete=models.CASCADE, related_name='utterances')
    speech_act = models.ForeignKey('SpeechAct', on_delete=models.CASCADE, related_name='utterances')
    sentence = models.ForeignKey('Sentence', on_delete=models.CASCADE, related_name='utterances')
    context = models.TextField()

    def __str__(self):
        return f"{self.speech_act} / {self.sentence}"

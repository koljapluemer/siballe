from django.db import models


class DialogUtterance(models.Model):
    dialog = models.ForeignKey('Dialog', on_delete=models.CASCADE, related_name='utterances')
    speaker = models.TextField()
    speech_act = models.ForeignKey('SpeechAct', on_delete=models.CASCADE, related_name='dialog_utterances')
    previous_utterance = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='next_utterances',
    )

    def __str__(self):
        return str(self.speech_act)

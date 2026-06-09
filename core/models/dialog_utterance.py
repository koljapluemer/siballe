from django.db import models


class DialogUtterance(models.Model):
    node = models.ForeignKey('DialogNode', on_delete=models.CASCADE, related_name='utterances')
    speech_act = models.ForeignKey('SpeechAct', on_delete=models.CASCADE, related_name='dialog_utterances')
    next_node = models.ForeignKey(
        'DialogNode', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='incoming_utterances',
    )

    def __str__(self):
        return str(self.speech_act)

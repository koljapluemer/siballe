from django.db import models


class Dialog(models.Model):
    situation = models.ForeignKey('Situation', on_delete=models.CASCADE, related_name='dialogs')
    name = models.TextField()
    learner_role = models.TextField(blank=True)
    other_role = models.TextField(blank=True)
    start_utterance = models.ForeignKey(
        'DialogUtterance', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+',
    )

    def __str__(self):
        return self.name[:60]

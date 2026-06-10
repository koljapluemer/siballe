from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_dialogutterance_previous_utterances'),
    ]

    operations = [
        migrations.AddField(
            model_name='dialog',
            name='learner_role',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='dialog',
            name='other_role',
            field=models.TextField(blank=True),
        ),
        migrations.RemoveField(
            model_name='dialog',
            name='speakers',
        ),
    ]

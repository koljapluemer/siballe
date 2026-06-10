from django.db import migrations, models


def migrate_forward(apps, schema_editor):
    DialogUtterance = apps.get_model('core', 'DialogUtterance')
    for u in DialogUtterance.objects.filter(previous_utterance__isnull=False):
        u.previous_utterances.add(u.previous_utterance_id)


def migrate_backward(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_merge_dialognode_into_dialogutterance'),
    ]

    operations = [
        migrations.AddField(
            model_name='dialogutterance',
            name='previous_utterances',
            field=models.ManyToManyField(
                blank=True,
                related_name='next_utterances',
                symmetrical=False,
                to='core.dialogutterance',
            ),
        ),
        migrations.RunPython(migrate_forward, migrate_backward),
        migrations.RemoveField(
            model_name='dialogutterance',
            name='previous_utterance',
        ),
    ]

from django.db import migrations, models
import django.db.models.deletion


def migrate_forward(apps, schema_editor):
    DialogNode = apps.get_model('core', 'DialogNode')
    DialogUtterance = apps.get_model('core', 'DialogUtterance')
    Dialog = apps.get_model('core', 'Dialog')

    # Step 1: copy dialog + speaker from each utterance's node
    utterances = list(DialogUtterance.objects.select_related('node__dialog').all())
    for u in utterances:
        u.dialog_id = u.node.dialog_id
        u.speaker = u.node.speaker
    DialogUtterance.objects.bulk_update(utterances, ['dialog_id', 'speaker'])

    # Step 2: for each node, find its predecessor utterance (the one whose next_node was this node)
    # and set previous_utterance on all utterances belonging to that node
    for node in DialogNode.objects.prefetch_related('utterances', 'incoming_utterances').all():
        pred = node.incoming_utterances.order_by('pk').first()
        if pred:
            node.utterances.update(previous_utterance=pred)
        # utterances at nodes with no predecessor keep previous_utterance=None (start-level)

    # Step 3: migrate Dialog.start_utterance from Dialog.start_node
    dialogs = list(Dialog.objects.filter(start_node__isnull=False))
    for d in dialogs:
        first = DialogUtterance.objects.filter(node_id=d.start_node_id).order_by('pk').first()
        d.start_utterance_id = first.pk if first else None
    Dialog.objects.bulk_update(dialogs, ['start_utterance_id'])


def migrate_backward(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_dialog_dialognode_dialog_start_node_dialogutterance_and_more'),
    ]

    operations = [
        # Phase 1: add new fields (nullable/blank to allow data migration)
        migrations.AddField(
            model_name='dialogutterance',
            name='dialog',
            field=models.ForeignKey(
                null=True, blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='utterances',
                to='core.dialog',
            ),
        ),
        migrations.AddField(
            model_name='dialogutterance',
            name='speaker',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dialogutterance',
            name='previous_utterance',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='next_utterances',
                to='core.dialogutterance',
            ),
        ),
        migrations.AddField(
            model_name='dialog',
            name='start_utterance',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='+',
                to='core.dialogutterance',
            ),
        ),

        # Phase 2: data migration
        migrations.RunPython(migrate_forward, migrate_backward),

        # Phase 3: make dialog non-nullable, remove old fields and DialogNode table
        migrations.AlterField(
            model_name='dialogutterance',
            name='dialog',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='utterances',
                to='core.dialog',
            ),
        ),
        migrations.RemoveField(
            model_name='dialogutterance',
            name='node',
        ),
        migrations.RemoveField(
            model_name='dialogutterance',
            name='next_node',
        ),
        migrations.RemoveField(
            model_name='dialog',
            name='start_node',
        ),
        migrations.DeleteModel(
            name='DialogNode',
        ),
    ]

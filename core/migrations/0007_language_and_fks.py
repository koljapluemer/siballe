from django.db import migrations, models
import django.db.models.deletion


def populate_languages(apps, schema_editor):
    Language = apps.get_model('core', 'Language')
    BuildingBlock = apps.get_model('core', 'BuildingBlock')
    Sentence = apps.get_model('core', 'Sentence')

    codes = set()
    codes.update(BuildingBlock.objects.values_list('language_code', flat=True))
    codes.update(Sentence.objects.values_list('language_code', flat=True))

    for code in codes:
        if code:
            Language.objects.get_or_create(iso3=code, defaults={'name': code.upper()})

    for bb in BuildingBlock.objects.all():
        if bb.language_code:
            bb.language_id = bb.language_code
            bb.save(update_fields=['language_id'])

    for s in Sentence.objects.all():
        if s.language_code:
            s.language_id = s.language_code
            s.save(update_fields=['language_id'])


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_situationalutterance_context'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('iso3', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='buildingblock',
            name='language',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='building_blocks',
                to='core.language',
            ),
        ),
        migrations.AddField(
            model_name='sentence',
            name='language',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='sentences',
                to='core.language',
            ),
        ),
        migrations.RunPython(populate_languages, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='buildingblock',
            name='language',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='building_blocks',
                to='core.language',
            ),
        ),
        migrations.AlterField(
            model_name='sentence',
            name='language',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='sentences',
                to='core.language',
            ),
        ),
        migrations.RemoveField(
            model_name='buildingblock',
            name='language_code',
        ),
        migrations.RemoveField(
            model_name='sentence',
            name='language_code',
        ),
        migrations.AddField(
            model_name='situation',
            name='language',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='situations',
                to='core.language',
            ),
        ),
    ]

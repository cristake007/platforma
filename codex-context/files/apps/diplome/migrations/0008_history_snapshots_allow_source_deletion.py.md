# apps/diplome/migrations/0008_history_snapshots_allow_source_deletion.py

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `apps/diplome/migrations/0008_history_snapshots_allow_source_deletion.py`
- App: `diplome`
- App guide: `codex-context/apps/diplome.md`
- Role: `migration`
- Size: 3923 bytes
- Source SHA-256: `084ea8cd1c4749948331e91f65694d92ff12ea37cbfad122a7b45d19631d85d2`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
import django.db.models.deletion
from django.db import migrations, models


def populate_history_snapshots(apps, schema_editor):
    DiplomaGenerationBatch = apps.get_model("diplome", "DiplomaGenerationBatch")
    GeneratedDiploma = apps.get_model("diplome", "GeneratedDiploma")

    for batch in DiplomaGenerationBatch.objects.select_related(
        "participant_list",
        "template",
    ).iterator(chunk_size=200):
        DiplomaGenerationBatch.objects.filter(pk=batch.pk).update(
            participant_list_name=batch.participant_list.name,
            template_name=batch.template.name,
        )

    for generated in GeneratedDiploma.objects.select_related(
        "participant_list",
        "template",
    ).iterator(chunk_size=200):
        GeneratedDiploma.objects.filter(pk=generated.pk).update(
            participant_list_name=generated.participant_list.name,
            template_name=generated.template.name,
        )


class Migration(migrations.Migration):
    dependencies = [
        ("diplome", "0007_diploma_generation_batch"),
    ]

    operations = [
        migrations.AddField(
            model_name="diplomagenerationbatch",
            name="participant_list_name",
            field=models.CharField(default="", max_length=160),
        ),
        migrations.AddField(
            model_name="diplomagenerationbatch",
            name="template_name",
            field=models.CharField(default="", max_length=160),
        ),
        migrations.AddField(
            model_name="generateddiploma",
            name="participant_list_name",
            field=models.CharField(default="", max_length=160),
        ),
        migrations.AddField(
            model_name="generateddiploma",
            name="template_name",
            field=models.CharField(default="", max_length=160),
        ),
        migrations.RunPython(
            populate_history_snapshots,
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name="diplomagenerationbatch",
            name="participant_list",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="diploma_generation_batches",
                to="diplome.participantlist",
            ),
        ),
        migrations.AlterField(
            model_name="diplomagenerationbatch",
            name="template",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="diploma_generation_batches",
                to="diplome.diplomatemplate",
            ),
        ),
        migrations.AlterField(
            model_name="generateddiploma",
            name="participant",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="generated_diplomas",
                to="diplome.participant",
            ),
        ),
        migrations.AlterField(
            model_name="generateddiploma",
            name="participant_list",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="generated_diplomas",
                to="diplome.participantlist",
            ),
        ),
        migrations.AlterField(
            model_name="generateddiploma",
            name="template",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="generated_diplomas",
                to="diplome.diplomatemplate",
            ),
        ),
    ]
```

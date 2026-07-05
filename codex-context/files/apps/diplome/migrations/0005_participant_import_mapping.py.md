# apps/diplome/migrations/0005_participant_import_mapping.py

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `apps/diplome/migrations/0005_participant_import_mapping.py`
- App: `diplome`
- App guide: `codex-context/apps/diplome.md`
- Role: `migration`
- Size: 903 bytes
- Source SHA-256: `7851f1bcb39312ecb80b883d31b2df0e98c6e2ebced00e363d3025e9d6b40bbf`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("diplome", "0004_participant_list_import"),
    ]

    operations = [
        migrations.AddField(
            model_name="participantimportdraft",
            name="source_columns_json",
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name="participantimportdraft",
            name="source_rows_json",
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name="participantimportdraft",
            name="column_mapping_json",
            field=models.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name="participantimportdraft",
            name="mapping_confirmed",
            field=models.BooleanField(default=False),
        ),
    ]
```

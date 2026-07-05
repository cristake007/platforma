# apps/diplome/migrations/0009_participantimportdraft_source_sheets_json.py

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `apps/diplome/migrations/0009_participantimportdraft_source_sheets_json.py`
- App: `diplome`
- App guide: `codex-context/apps/diplome.md`
- Role: `migration`
- Size: 382 bytes
- Source SHA-256: `f43e469df782c24331f9e53467f20e0d63ce307dc71e63efb642c3e4a92039b2`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("diplome", "0008_history_snapshots_allow_source_deletion"),
    ]

    operations = [
        migrations.AddField(
            model_name="participantimportdraft",
            name="source_sheets_json",
            field=models.JSONField(default=list),
        ),
    ]
```

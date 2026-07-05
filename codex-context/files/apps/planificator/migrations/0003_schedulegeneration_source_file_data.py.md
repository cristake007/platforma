# apps/planificator/migrations/0003_schedulegeneration_source_file_data.py

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `apps/planificator/migrations/0003_schedulegeneration_source_file_data.py`
- App: `planificator`
- App guide: `codex-context/apps/planificator.md`
- Role: `migration`
- Size: 404 bytes
- Source SHA-256: `4d12ae1fbd4df553474306d4f4dc679834d2979a16d2f07875e2296395b4b6ec`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("planificator", "0002_schedulegeneration_appsetting_user_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="schedulegeneration",
            name="source_file_data",
            field=models.BinaryField(default=bytes, editable=False),
        ),
    ]
```

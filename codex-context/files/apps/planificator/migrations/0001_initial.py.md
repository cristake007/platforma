# apps/planificator/migrations/0001_initial.py

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `apps/planificator/migrations/0001_initial.py`
- App: `planificator`
- App guide: `codex-context/apps/planificator.md`
- Role: `migration`
- Size: 746 bytes
- Source SHA-256: `a58b4c200eb1421e62e42871ac87c92ec8cccbd059085b4884d246f522865822`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AppSetting",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("scope", models.CharField(max_length=100, unique=True)),
                ("payload", models.JSONField(default=dict)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "permissions": [
                    ("use_course_planning", "Can use schedule generator"),
                ],
            },
        ),
    ]
```

# apps/planificator/migrations/0004_alter_appsetting_options.py

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `apps/planificator/migrations/0004_alter_appsetting_options.py`
- App: `planificator`
- App guide: `codex-context/apps/planificator.md`
- Role: `migration`
- Size: 512 bytes
- Source SHA-256: `8f7dbdcf4b1c74abd61443aae8752ba36451945a9b6291d8c69deae27b1cb97b`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("planificator", "0003_schedulegeneration_source_file_data"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="appsetting",
            options={
                "permissions": [
                    ("use_course_planning", "Can use schedule generator"),
                    ("use_word_matcher", "Can use Word date matcher"),
                ],
            },
        ),
    ]
```

# apps/planificator/migrations/0005_alter_appsetting_options.py

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `apps/planificator/migrations/0005_alter_appsetting_options.py`
- App: `planificator`
- App guide: `codex-context/apps/planificator.md`
- Role: `migration`
- Size: 563 bytes
- Source SHA-256: `268811b4331ae3ad9b365e5154da710c0797b635f40c00bc7dc3c502a3e3ab37`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("planificator", "0004_alter_appsetting_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="appsetting",
            options={
                "permissions": [
                    ("use_course_planning", "Can use schedule generator"),
                    ("use_word_matcher", "Can use Word date matcher"),
                    ("use_xml_export", "Can use XML export"),
                ],
            },
        ),
    ]
```

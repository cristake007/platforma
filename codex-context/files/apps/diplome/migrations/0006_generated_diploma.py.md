# apps/diplome/migrations/0006_generated_diploma.py

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `apps/diplome/migrations/0006_generated_diploma.py`
- App: `diplome`
- App guide: `codex-context/apps/diplome.md`
- Role: `migration`
- Size: 3388 bytes
- Source SHA-256: `5f8fbecdbf0f15d47b8d1db97230262e285aa8c33fc7094dc42274bb712f5aa4`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models

import apps.diplome.models


class Migration(migrations.Migration):
    dependencies = [
        ("diplome", "0005_participant_import_mapping"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="GeneratedDiploma",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("certificate_number", models.CharField(max_length=100)),
                ("participant_name", models.CharField(max_length=200)),
                (
                    "pdf_file",
                    models.FileField(
                        max_length=500,
                        upload_to=apps.diplome.models.generated_diploma_upload_to,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="generated_diplomas",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "participant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="generated_diplomas",
                        to="diplome.participant",
                    ),
                ),
                (
                    "participant_list",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="generated_diplomas",
                        to="diplome.participantlist",
                    ),
                ),
                (
                    "template",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="generated_diplomas",
                        to="diplome.diplomatemplate",
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at",),
                "indexes": [
                    models.Index(
                        fields=["owner", "-created_at"],
                        name="dipl_gen_owner_created",
                    ),
                    models.Index(
                        fields=["participant_list", "created_at"],
                        name="dipl_gen_list_created",
                    ),
                    models.Index(
                        fields=["participant", "created_at"],
                        name="dipl_gen_part_created",
                    ),
                    models.Index(
                        fields=["template", "created_at"],
                        name="dipl_gen_tmpl_created",
                    ),
                ],
            },
        ),
    ]
```

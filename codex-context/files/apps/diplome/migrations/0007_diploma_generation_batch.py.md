# apps/diplome/migrations/0007_diploma_generation_batch.py

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `apps/diplome/migrations/0007_diploma_generation_batch.py`
- App: `diplome`
- App guide: `codex-context/apps/diplome.md`
- Role: `migration`
- Size: 4691 bytes
- Source SHA-256: `250664043eb0ad042441d3b53e2b18680d003c5a8e1658b967b85db6d3de301b`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("diplome", "0006_generated_diploma"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="DiplomaGenerationBatch",
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
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "În așteptare"),
                            ("running", "În curs"),
                            ("completed", "Finalizat"),
                            ("completed_with_errors", "Finalizat cu erori"),
                            ("failed", "Eșuat"),
                        ],
                        default="pending",
                        max_length=24,
                    ),
                ),
                ("total_count", models.PositiveIntegerField(default=0)),
                ("success_count", models.PositiveIntegerField(default=0)),
                ("failed_count", models.PositiveIntegerField(default=0)),
                ("output_folder", models.CharField(max_length=500)),
                ("error_summary", models.JSONField(blank=True, default=list)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("started_at", models.DateTimeField(blank=True, null=True)),
                ("completed_at", models.DateTimeField(blank=True, null=True)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="diploma_generation_batches",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "participant_list",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="diploma_generation_batches",
                        to="diplome.participantlist",
                    ),
                ),
                (
                    "template",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="diploma_generation_batches",
                        to="diplome.diplomatemplate",
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at",),
                "indexes": [
                    models.Index(fields=["owner", "-created_at"], name="dipl_batch_owner_created"),
                    models.Index(fields=["participant_list", "-created_at"], name="dipl_batch_list_created"),
                    models.Index(fields=["template", "-created_at"], name="dipl_batch_tmpl_created"),
                    models.Index(fields=["owner", "status", "-created_at"], name="dipl_batch_owner_st_created"),
                ],
            },
        ),
        migrations.AddField(
            model_name="generateddiploma",
            name="batch",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="generated_diplomas",
                to="diplome.diplomagenerationbatch",
            ),
        ),
        migrations.RemoveIndex(
            model_name="generateddiploma",
            name="dipl_gen_list_created",
        ),
        migrations.RemoveIndex(
            model_name="generateddiploma",
            name="dipl_gen_part_created",
        ),
        migrations.AddIndex(
            model_name="generateddiploma",
            index=models.Index(fields=["batch", "participant_name"], name="dipl_gen_batch_name"),
        ),
        migrations.AddIndex(
            model_name="generateddiploma",
            index=models.Index(fields=["participant_list", "participant_name"], name="dipl_gen_list_name"),
        ),
        migrations.AddIndex(
            model_name="generateddiploma",
            index=models.Index(fields=["participant", "-created_at"], name="dipl_gen_part_created"),
        ),
    ]
```

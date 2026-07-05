# apps/diplome/migrations/0004_participant_list_import.py

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `apps/diplome/migrations/0004_participant_list_import.py`
- App: `diplome`
- App guide: `codex-context/apps/diplome.md`
- Role: `migration`
- Size: 3988 bytes
- Source SHA-256: `937645fccb40a92cc0c8c7c9a757f3719ff026296954f7cd72e89492b4851d4d`

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
        ("diplome", "0003_diplomatemplate_category_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ParticipantImportDraft",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("list_name", models.CharField(max_length=160)),
                ("description", models.TextField(blank=True)),
                ("course_name", models.CharField(blank=True, max_length=200)),
                ("source_file_name", models.CharField(max_length=255)),
                ("valid_rows_json", models.JSONField(default=list)),
                ("invalid_rows_json", models.JSONField(default=list)),
                ("warnings_json", models.JSONField(default=list)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("expires_at", models.DateTimeField(db_index=True)),
                ("owner", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="participant_import_drafts", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ("-created_at",),
                "indexes": [models.Index(fields=["owner", "expires_at"], name="dipl_pdraft_owner_exp")],
            },
        ),
        migrations.CreateModel(
            name="ParticipantList",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=160)),
                ("description", models.TextField(blank=True)),
                ("course_name", models.CharField(blank=True, max_length=200)),
                ("source_file_name", models.CharField(max_length=255)),
                ("participant_count", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("owner", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="participant_lists", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ("-updated_at", "name"),
                "indexes": [models.Index(fields=["owner", "-updated_at"], name="dipl_plist_owner_upd")],
            },
        ),
        migrations.CreateModel(
            name="Participant",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("full_name", models.CharField(max_length=200)),
                ("date_of_birth", models.DateField()),
                ("place_of_birth", models.CharField(max_length=200)),
                ("certificate_number", models.CharField(max_length=100)),
                ("source_row", models.PositiveIntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("owner", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="diploma_participants", to=settings.AUTH_USER_MODEL)),
                ("participant_list", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="participants", to="diplome.participantlist")),
            ],
            options={
                "ordering": ("source_row", "full_name"),
                "indexes": [
                    models.Index(fields=["participant_list", "source_row"], name="dipl_part_list_row"),
                    models.Index(fields=["owner", "certificate_number"], name="dipl_part_owner_cert"),
                ],
            },
        ),
    ]
```

# apps/tasks/migrations/0001_initial.py

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `apps/tasks/migrations/0001_initial.py`
- App: `tasks`
- App guide: `codex-context/apps/tasks.md`
- Role: `migration`
- Size: 6537 bytes
- Source SHA-256: `5591d55059734f0beda2238afdcf426fbe35d531379f812ce55154f85a96fa17`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
# Generated for the collaborative tasks application.

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
from django.db.models import F, Q


class Migration(migrations.Migration):
    initial = True

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="TaskBoard",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=120)),
                ("is_archived", models.BooleanField(db_index=True, default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("owner", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="owned_task_boards", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ("name",)},
        ),
        migrations.CreateModel(
            name="BoardMembership",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("board", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="memberships", to="tasks.taskboard")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="task_board_memberships", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ("user__first_name", "user__last_name", "user__username")},
        ),
        migrations.AddField(
            model_name="taskboard",
            name="members",
            field=models.ManyToManyField(related_name="task_boards", through="tasks.BoardMembership", to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name="TaskStage",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=80)),
                ("position", models.PositiveIntegerField(default=0)),
                ("tone", models.CharField(choices=[("neutral", "Neutru"), ("info", "Informativ"), ("warning", "Avertizare"), ("error", "Eroare"), ("success", "Succes")], default="neutral", max_length=12)),
                ("is_terminal", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("board", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="stages", to="tasks.taskboard")),
            ],
            options={"ordering": ("position", "created_at")},
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField(blank=True)),
                ("priority", models.CharField(choices=[("low", "Scăzută"), ("medium", "Medie"), ("high", "Ridicată")], db_index=True, default="medium", max_length=10)),
                ("start_at", models.DateTimeField(blank=True, null=True)),
                ("due_at", models.DateTimeField(db_index=True)),
                ("rank", models.PositiveIntegerField(default=0)),
                ("completed_at", models.DateTimeField(blank=True, null=True)),
                ("archived_at", models.DateTimeField(blank=True, db_index=True, null=True)),
                ("origin_app", models.CharField(blank=True, max_length=100)),
                ("origin_type", models.CharField(blank=True, max_length=100)),
                ("origin_object_id", models.CharField(blank=True, max_length=255)),
                ("origin_label", models.CharField(blank=True, max_length=200)),
                ("origin_url", models.CharField(blank=True, max_length=500)),
                ("version", models.PositiveIntegerField(default=1)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("assignee", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="assigned_tasks", to=settings.AUTH_USER_MODEL)),
                ("board", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="tasks", to="tasks.taskboard")),
                ("creator", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="created_tasks", to=settings.AUTH_USER_MODEL)),
                ("stage", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="tasks", to="tasks.taskstage")),
            ],
            options={"ordering": ("stage__position", "rank", "due_at")},
        ),
        migrations.AddConstraint(
            model_name="taskboard",
            constraint=models.UniqueConstraint(fields=("owner", "name"), name="tasks_unique_board_owner_name"),
        ),
        migrations.AddConstraint(
            model_name="boardmembership",
            constraint=models.UniqueConstraint(fields=("board", "user"), name="tasks_unique_board_member"),
        ),
        migrations.AddConstraint(
            model_name="taskstage",
            constraint=models.UniqueConstraint(fields=("board", "name"), name="tasks_unique_stage_board_name"),
        ),
        migrations.AddIndex(
            model_name="taskstage",
            index=models.Index(fields=["board", "position"], name="tasks_stage_board_pos"),
        ),
        migrations.AddConstraint(
            model_name="task",
            constraint=models.CheckConstraint(condition=Q(("start_at__isnull", True), ("due_at__gt", F("start_at")), _connector="OR"), name="tasks_due_after_start"),
        ),
        migrations.AddIndex(model_name="task", index=models.Index(fields=["board", "stage", "rank"], name="tasks_board_stage_rank")),
        migrations.AddIndex(model_name="task", index=models.Index(fields=["assignee", "archived_at", "due_at"], name="tasks_assignee_due")),
        migrations.AddIndex(model_name="task", index=models.Index(fields=["creator", "archived_at", "due_at"], name="tasks_creator_due")),
    ]
```

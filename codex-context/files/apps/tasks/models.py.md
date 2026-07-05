# apps/tasks/models.py

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `apps/tasks/models.py`
- App: `tasks`
- App guide: `codex-context/apps/tasks.md`
- Role: `backend`
- Size: 6222 bytes
- Source SHA-256: `ad5146a89a5083a9a962d92973c696ffdb9965a45fa1651d0d4987ded28594e1`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q


class TaskBoard(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="owned_task_boards",
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="BoardMembership",
        related_name="task_boards",
    )
    is_archived = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)
        constraints = [
            models.UniqueConstraint(
                fields=("owner", "name"),
                name="tasks_unique_board_owner_name",
            ),
        ]

    def __str__(self):
        return self.name


class BoardMembership(models.Model):
    board = models.ForeignKey(TaskBoard, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="task_board_memberships",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("user__first_name", "user__last_name", "user__username")
        constraints = [
            models.UniqueConstraint(
                fields=("board", "user"),
                name="tasks_unique_board_member",
            ),
        ]

    def __str__(self):
        return f"{self.user} — {self.board}"


class TaskStage(models.Model):
    class Tone(models.TextChoices):
        NEUTRAL = "neutral", "Neutru"
        INFO = "info", "Informativ"
        WARNING = "warning", "Avertizare"
        ERROR = "error", "Eroare"
        SUCCESS = "success", "Succes"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    board = models.ForeignKey(TaskBoard, on_delete=models.CASCADE, related_name="stages")
    name = models.CharField(max_length=80)
    position = models.PositiveIntegerField(default=0)
    tone = models.CharField(max_length=12, choices=Tone.choices, default=Tone.NEUTRAL)
    is_terminal = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("position", "created_at")
        constraints = [
            models.UniqueConstraint(
                fields=("board", "name"),
                name="tasks_unique_stage_board_name",
            ),
        ]
        indexes = [models.Index(fields=("board", "position"), name="tasks_stage_board_pos")]

    def __str__(self):
        return f"{self.board}: {self.name}"


class Task(models.Model):
    class Priority(models.TextChoices):
        LOW = "low", "Scăzută"
        MEDIUM = "medium", "Medie"
        HIGH = "high", "Ridicată"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    board = models.ForeignKey(TaskBoard, on_delete=models.CASCADE, related_name="tasks")
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_tasks",
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="assigned_tasks",
    )
    stage = models.ForeignKey(TaskStage, on_delete=models.PROTECT, related_name="tasks")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
        db_index=True,
    )
    start_at = models.DateTimeField(blank=True, null=True)
    due_at = models.DateTimeField(db_index=True)
    rank = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(blank=True, null=True)
    archived_at = models.DateTimeField(blank=True, null=True, db_index=True)
    origin_app = models.CharField(max_length=100, blank=True)
    origin_type = models.CharField(max_length=100, blank=True)
    origin_object_id = models.CharField(max_length=255, blank=True)
    origin_label = models.CharField(max_length=200, blank=True)
    origin_url = models.CharField(max_length=500, blank=True)
    version = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("stage__position", "rank", "due_at")
        constraints = [
            models.CheckConstraint(
                condition=Q(start_at__isnull=True) | Q(due_at__gt=F("start_at")),
                name="tasks_due_after_start",
            ),
        ]
        indexes = [
            models.Index(fields=("board", "stage", "rank"), name="tasks_board_stage_rank"),
            models.Index(fields=("assignee", "archived_at", "due_at"), name="tasks_assignee_due"),
            models.Index(fields=("creator", "archived_at", "due_at"), name="tasks_creator_due"),
        ]

    def clean(self):
        errors = {}
        if self.stage_id and self.board_id and self.stage.board_id != self.board_id:
            errors["stage"] = "Etapa trebuie să aparțină board-ului selectat."
        if self.start_at and self.due_at and self.due_at <= self.start_at:
            errors["due_at"] = "Termenul trebuie să fie după data de început."
        if self.assignee_id and self.board_id:
            is_member = BoardMembership.objects.filter(
                board_id=self.board_id,
                user_id=self.assignee_id,
                user__is_active=True,
            ).exists()
            if not is_member:
                errors["assignee"] = "Responsabilul trebuie să fie membru activ al board-ului."
        if errors:
            raise ValidationError(errors)

    @property
    def is_archived(self):
        return self.archived_at is not None

    def __str__(self):
        return self.title
```

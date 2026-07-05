# apps/tasks/admin.py

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `apps/tasks/admin.py`
- App: `tasks`
- App guide: `codex-context/apps/tasks.md`
- Role: `backend`
- Size: 927 bytes
- Source SHA-256: `f24c27bf08c340644a3595e7a9c8cd6343a2846a54c67fe230cc9e2cecaee8cc`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from django.contrib import admin

from .models import BoardMembership, Task, TaskBoard, TaskStage


class BoardMembershipInline(admin.TabularInline):
    model = BoardMembership
    extra = 0


class TaskStageInline(admin.TabularInline):
    model = TaskStage
    extra = 0


@admin.register(TaskBoard)
class TaskBoardAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "is_archived", "updated_at")
    list_filter = ("is_archived",)
    search_fields = ("name", "owner__username")
    inlines = (BoardMembershipInline, TaskStageInline)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "board", "assignee", "stage", "priority", "due_at", "archived_at")
    list_filter = ("priority", "stage__is_terminal", "archived_at")
    search_fields = ("title", "description", "assignee__username", "creator__username")
    list_select_related = ("board", "assignee", "creator", "stage")
```

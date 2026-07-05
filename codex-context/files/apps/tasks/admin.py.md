# Source snapshot

## `apps/tasks/admin.py`

Size: 927 B

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

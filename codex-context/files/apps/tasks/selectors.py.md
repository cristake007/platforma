# apps/tasks/selectors.py

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `apps/tasks/selectors.py`
- App: `tasks`
- App guide: `codex-context/apps/tasks.md`
- Role: `backend`
- Size: 2520 bytes
- Source SHA-256: `41cbee0d8692a12fd39cec337d2b5b1e39f383273f7bb6003e00affe94c94d33`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from django.db.models import Q, QuerySet
from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import BoardMembership, Task, TaskBoard


def accessible_boards(*, user, include_archived: bool = False) -> QuerySet[TaskBoard]:
    queryset = TaskBoard.objects.select_related("owner")
    if not include_archived:
        queryset = queryset.filter(is_archived=False)
    if user.is_staff:
        return queryset.order_by("name").distinct()
    return queryset.filter(Q(owner=user) | Q(memberships__user=user)).order_by("name").distinct()


def get_accessible_board(*, user, board_id, include_archived: bool = False) -> TaskBoard:
    return get_object_or_404(
        accessible_boards(user=user, include_archived=include_archived),
        pk=board_id,
    )


def user_can_manage_board(*, user, board: TaskBoard) -> bool:
    return bool(user.is_staff or board.owner_id == user.pk)


def require_board_manager(*, user, board: TaskBoard) -> None:
    if not user_can_manage_board(user=user, board=board):
        raise Http404("Board indisponibil.")


def visible_tasks(*, user, include_archived: bool = False) -> QuerySet[Task]:
    queryset = Task.objects.select_related("board", "board__owner", "stage", "creator", "assignee")
    if not include_archived:
        queryset = queryset.filter(archived_at__isnull=True, board__is_archived=False)
    if user.is_staff:
        return queryset
    return queryset.filter(
        Q(creator=user) | Q(assignee=user) | Q(board__owner=user)
    ).distinct()


def visible_board_tasks(*, user, board: TaskBoard, include_archived: bool = False) -> QuerySet[Task]:
    return visible_tasks(user=user, include_archived=include_archived).filter(board=board)


def get_visible_task(*, user, task_id, include_archived: bool = False) -> Task:
    return get_object_or_404(
        visible_tasks(user=user, include_archived=include_archived),
        pk=task_id,
    )


def board_members(*, board: TaskBoard, active_only: bool = True):
    queryset = BoardMembership.objects.filter(board=board).select_related("user")
    if active_only:
        queryset = queryset.filter(user__is_active=True)
    return queryset.order_by("user__first_name", "user__last_name", "user__username")


def user_can_edit_task(*, user, task: Task) -> bool:
    return bool(user.is_staff or task.creator_id == user.pk)


def user_can_move_task(*, user, task: Task) -> bool:
    return bool(user.is_staff or task.creator_id == user.pk or task.assignee_id == user.pk)
```

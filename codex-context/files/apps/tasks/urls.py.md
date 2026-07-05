# apps/tasks/urls.py

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `apps/tasks/urls.py`
- App: `tasks`
- App guide: `codex-context/apps/tasks.md`
- Role: `backend`
- Size: 1811 bytes
- Source SHA-256: `1d2c915b8a9c1918fccdc98be171dc1b109b9d8af9d34d6f7124acf0e4cacf9a`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from django.urls import path

from . import views


app_name = "tasks"

urlpatterns = [
    path("", views.TaskHubView.as_view(), name="index"),
    path("boards/new/", views.BoardCreateView.as_view(), name="board_create"),
    path("boards/<uuid:board_id>/", views.BoardKanbanView.as_view(), name="board_kanban"),
    path("boards/<uuid:board_id>/list/", views.BoardListView.as_view(), name="board_list"),
    path("boards/<uuid:board_id>/settings/", views.BoardSettingsView.as_view(), name="board_settings"),
    path("boards/<uuid:board_id>/archive/", views.BoardArchiveView.as_view(), name="board_archive"),
    path("boards/<uuid:board_id>/members/add/", views.MemberAddView.as_view(), name="member_add"),
    path("boards/<uuid:board_id>/members/<int:user_id>/remove/", views.MemberRemoveView.as_view(), name="member_remove"),
    path("boards/<uuid:board_id>/transfer/", views.OwnershipTransferView.as_view(), name="ownership_transfer"),
    path("boards/<uuid:board_id>/stages/add/", views.StageCreateView.as_view(), name="stage_create"),
    path("stages/<uuid:stage_id>/edit/", views.StageUpdateView.as_view(), name="stage_update"),
    path("stages/<uuid:stage_id>/move/", views.StagePositionView.as_view(), name="stage_position"),
    path("stages/<uuid:stage_id>/delete/", views.StageDeleteView.as_view(), name="stage_delete"),
    path("boards/<uuid:board_id>/tasks/new/", views.TaskCreateView.as_view(), name="task_create"),
    path("tasks/<uuid:task_id>/edit/", views.TaskEditView.as_view(), name="task_edit"),
    path("tasks/<uuid:task_id>/move/", views.TaskMoveView.as_view(), name="task_move"),
    path("tasks/<uuid:task_id>/archive/", views.TaskArchiveView.as_view(), name="task_archive"),
    path("boards/<uuid:board_id>/state/", views.BoardStateView.as_view(), name="board_state"),
]
```

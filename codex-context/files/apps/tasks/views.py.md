# apps/tasks/views.py

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `apps/tasks/views.py`
- App: `tasks`
- App guide: `codex-context/apps/tasks.md`
- Role: `backend`
- Size: 20095 bytes
- Source SHA-256: `5ec8e508c62012b3c4d0fe0eab9aab3634c0068288008c6a25be4c774cb2dd6f`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
import hashlib
import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Q
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View

from .forms import (
    BoardForm,
    MemberAddForm,
    OwnershipTransferForm,
    StageDeleteForm,
    StageForm,
    TaskForm,
    TaskMoveForm,
)
from .models import Task, TaskStage
from .selectors import (
    accessible_boards,
    board_members,
    get_accessible_board,
    get_visible_task,
    require_board_manager,
    user_can_edit_task,
    user_can_manage_board,
    user_can_move_task,
    visible_board_tasks,
    visible_tasks,
)
from .services import (
    add_board_member,
    create_board,
    create_stage,
    create_task,
    delete_stage,
    move_stage_position,
    move_task,
    remove_board_member,
    set_board_archived,
    set_task_archived,
    transfer_board_ownership,
    update_stage,
    update_task,
)


def _error_text(exc: ValidationError) -> str:
    if hasattr(exc, "message_dict"):
        return " ".join(message for values in exc.message_dict.values() for message in values)
    return " ".join(exc.messages)


def _decorate_tasks(tasks, user):
    for task in tasks:
        task.can_edit = user_can_edit_task(user=user, task=task)
        task.can_move = user_can_move_task(user=user, task=task)
    return tasks


def _filtered_tasks(request, queryset):
    board_id = request.GET.get("board", "").strip()
    relation = request.GET.get("relation", "").strip()
    stage_id = request.GET.get("stage", "").strip()
    priority = request.GET.get("priority", "").strip()
    search = request.GET.get("q", "").strip()
    if board_id:
        queryset = queryset.filter(board_id=board_id)
    if relation == "created":
        queryset = queryset.filter(creator=request.user)
    elif relation == "assigned":
        queryset = queryset.filter(assignee=request.user)
    elif relation == "mine" and request.user.is_staff:
        queryset = queryset.filter(Q(creator=request.user) | Q(assignee=request.user))
    if stage_id:
        queryset = queryset.filter(stage_id=stage_id)
    if priority in Task.Priority.values:
        queryset = queryset.filter(priority=priority)
    if search:
        queryset = queryset.filter(
            Q(title__icontains=search)
            | Q(description__icontains=search)
            | Q(origin_label__icontains=search)
        )
    ordering = request.GET.get("sort")
    return queryset.order_by("-due_at" if ordering == "due_desc" else "due_at", "title")


class TaskHubView(LoginRequiredMixin, View):
    template_name = "tasks/hub.html"

    def get(self, request):
        boards = list(accessible_boards(user=request.user))
        queryset = _filtered_tasks(request, visible_tasks(user=request.user))
        paginator = Paginator(queryset, 25)
        page = paginator.get_page(request.GET.get("page"))
        _decorate_tasks(page.object_list, request.user)
        stage_options = TaskStage.objects.filter(board__in=boards).order_by("board__name", "position")
        return render(
            request,
            self.template_name,
            {
                "boards": boards,
                "page": page,
                "stage_options": stage_options,
                "priority_choices": Task.Priority.choices,
                "filters": request.GET,
                "first_board": boards[0] if boards else None,
            },
        )


class BoardCreateView(LoginRequiredMixin, View):
    template_name = "tasks/board_form.html"

    def get(self, request):
        return render(request, self.template_name, {"form": BoardForm()})

    def post(self, request):
        form = BoardForm(request.POST)
        if form.is_valid():
            try:
                board = create_board(actor=request.user, name=form.cleaned_data["name"])
            except IntegrityError:
                form.add_error("name", "Ai deja un board cu acest nume.")
            else:
                messages.success(request, "Board-ul a fost creat.")
                return redirect("tasks:board_kanban", board_id=board.pk)
        return render(request, self.template_name, {"form": form}, status=400)


def _board_context(*, request, board, task_form=None):
    stages = list(board.stages.order_by("position", "created_at"))
    task_queryset = visible_board_tasks(user=request.user, board=board)
    assignee_id = request.GET.get("assignee", "").strip()
    priority = request.GET.get("priority", "").strip()
    search = request.GET.get("q", "").strip()
    if assignee_id:
        task_queryset = task_queryset.filter(assignee_id=assignee_id)
    if priority in Task.Priority.values:
        task_queryset = task_queryset.filter(priority=priority)
    if search:
        task_queryset = task_queryset.filter(Q(title__icontains=search) | Q(description__icontains=search))
    tasks = list(task_queryset.order_by("stage__position", "rank", "due_at"))
    _decorate_tasks(tasks, request.user)
    grouped = {stage.pk: [] for stage in stages}
    for task in tasks:
        grouped.setdefault(task.stage_id, []).append(task)
    for stage in stages:
        stage.visible_tasks = grouped.get(stage.pk, [])
    members = list(board_members(board=board))
    return {
        "board": board,
        "boards": accessible_boards(user=request.user),
        "stages": stages,
        "members": members,
        "task_form": task_form or TaskForm(board=board, actor=request.user),
        "can_manage_board": user_can_manage_board(user=request.user, board=board),
        "state_url": reverse("tasks:board_state", kwargs={"board_id": board.pk}),
        "priority_choices": Task.Priority.choices,
        "filters": request.GET,
    }


class BoardKanbanView(LoginRequiredMixin, View):
    template_name = "tasks/board_kanban.html"

    def get(self, request, board_id):
        board = get_accessible_board(user=request.user, board_id=board_id)
        return render(request, self.template_name, _board_context(request=request, board=board))


class BoardListView(LoginRequiredMixin, View):
    template_name = "tasks/board_list.html"

    def get(self, request, board_id):
        board = get_accessible_board(user=request.user, board_id=board_id)
        queryset = _filtered_tasks(request, visible_board_tasks(user=request.user, board=board))
        page = Paginator(queryset, 25).get_page(request.GET.get("page"))
        _decorate_tasks(page.object_list, request.user)
        context = _board_context(request=request, board=board)
        context.update({"page": page, "priority_choices": Task.Priority.choices, "filters": request.GET})
        return render(request, self.template_name, context)


class TaskCreateView(LoginRequiredMixin, View):
    template_name = "tasks/task_form.html"

    def get(self, request, board_id):
        board = get_accessible_board(user=request.user, board_id=board_id)
        return render(request, self.template_name, {"board": board, "form": TaskForm(board=board, actor=request.user)})

    def post(self, request, board_id):
        board = get_accessible_board(user=request.user, board_id=board_id)
        form = TaskForm(request.POST, board=board, actor=request.user)
        if form.is_valid():
            try:
                create_task(actor=request.user, board=board, **form.cleaned_data)
            except ValidationError as exc:
                form.add_error(None, _error_text(exc))
            else:
                messages.success(request, "Task-ul a fost creat.")
                return redirect("tasks:board_kanban", board_id=board.pk)
        return render(request, self.template_name, {"board": board, "form": form}, status=400)


class TaskEditView(LoginRequiredMixin, View):
    template_name = "tasks/task_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.task = get_visible_task(user=request.user, task_id=kwargs["task_id"])
        if not user_can_edit_task(user=request.user, task=self.task):
            raise Http404("Task indisponibil.")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, task_id):
        form = TaskForm(instance=self.task, board=self.task.board, actor=request.user)
        return render(request, self.template_name, {"board": self.task.board, "task": self.task, "form": form})

    def post(self, request, task_id):
        form = TaskForm(request.POST, instance=self.task, board=self.task.board, actor=request.user)
        if form.is_valid():
            try:
                update_task(actor=request.user, task=self.task, **form.cleaned_data)
            except ValidationError as exc:
                form.add_error(None, _error_text(exc))
            else:
                messages.success(request, "Task-ul a fost actualizat.")
                return redirect("tasks:board_kanban", board_id=self.task.board_id)
        return render(request, self.template_name, {"board": self.task.board, "task": self.task, "form": form}, status=400)


class TaskMoveView(LoginRequiredMixin, View):
    def post(self, request, task_id):
        task = get_visible_task(user=request.user, task_id=task_id)
        form = TaskMoveForm(request.POST, board=task.board)
        if not form.is_valid():
            return JsonResponse({"success": False, "errors": form.errors.get_json_data()}, status=400)
        try:
            task = move_task(
                actor=request.user,
                task=task,
                target_stage=form.cleaned_data["stage"],
                target_index=form.cleaned_data["target_index"],
                expected_version=form.cleaned_data["expected_version"],
            )
        except ValidationError as exc:
            is_stale = any(getattr(error, "code", None) == "stale" for error in exc.error_list)
            status = 409 if is_stale else 400
            if request.headers.get("Accept") == "application/json":
                return JsonResponse({"success": False, "error": _error_text(exc)}, status=status)
            messages.error(request, _error_text(exc))
            return redirect("tasks:board_kanban", board_id=task.board_id)
        if request.headers.get("Accept") == "application/json":
            return JsonResponse(
                {
                    "success": True,
                    "task": {
                        "id": str(task.pk),
                        "stageId": str(task.stage_id),
                        "rank": task.rank,
                        "version": task.version,
                        "completedAt": task.completed_at.isoformat() if task.completed_at else None,
                    },
                }
            )
        messages.success(request, "Etapa task-ului a fost actualizată.")
        return redirect("tasks:board_kanban", board_id=task.board_id)


class TaskArchiveView(LoginRequiredMixin, View):
    def post(self, request, task_id):
        task = get_visible_task(user=request.user, task_id=task_id, include_archived=True)
        archived = request.POST.get("archived", "1") != "0"
        try:
            set_task_archived(actor=request.user, task=task, archived=archived)
        except ValidationError as exc:
            raise Http404(_error_text(exc)) from exc
        messages.success(request, "Task arhivat." if archived else "Task restaurat.")
        return redirect(request.POST.get("next") or reverse("tasks:board_kanban", kwargs={"board_id": task.board_id}))


class BoardSettingsView(LoginRequiredMixin, View):
    template_name = "tasks/board_settings.html"

    def get(self, request, board_id):
        board = get_accessible_board(user=request.user, board_id=board_id, include_archived=True)
        require_board_manager(user=request.user, board=board)
        stages = list(board.stages.order_by("position"))
        stage_rows = [
            {
                "stage": stage,
                "form": StageForm(instance=stage, prefix=f"stage-{stage.pk}"),
                "delete_form": StageDeleteForm(stage=stage, prefix=f"delete-{stage.pk}"),
            }
            for stage in stages
        ]
        archived_tasks = visible_board_tasks(user=request.user, board=board, include_archived=True).filter(archived_at__isnull=False)
        return render(
            request,
            self.template_name,
            {
                "board": board,
                "members": board_members(board=board, active_only=False),
                "member_form": MemberAddForm(board=board),
                "transfer_form": OwnershipTransferForm(board=board),
                "stage_form": StageForm(prefix="new-stage"),
                "stage_rows": stage_rows,
                "archived_tasks": archived_tasks,
            },
        )


class MemberAddView(LoginRequiredMixin, View):
    def post(self, request, board_id):
        board = get_accessible_board(user=request.user, board_id=board_id, include_archived=True)
        require_board_manager(user=request.user, board=board)
        form = MemberAddForm(request.POST, board=board)
        if form.is_valid():
            add_board_member(actor=request.user, board=board, user=form.cleaned_data["user"])
            messages.success(request, "Membru adăugat.")
        else:
            messages.error(request, "Selectează un utilizator activ care nu este deja membru.")
        return redirect("tasks:board_settings", board_id=board.pk)


class MemberRemoveView(LoginRequiredMixin, View):
    def post(self, request, board_id, user_id):
        board = get_accessible_board(user=request.user, board_id=board_id, include_archived=True)
        require_board_manager(user=request.user, board=board)
        membership = get_object_or_404(board.memberships.select_related("user"), user_id=user_id)
        try:
            remove_board_member(actor=request.user, board=board, user=membership.user)
        except ValidationError as exc:
            messages.error(request, _error_text(exc))
        else:
            messages.success(request, "Membru eliminat.")
        return redirect("tasks:board_settings", board_id=board.pk)


class OwnershipTransferView(LoginRequiredMixin, View):
    def post(self, request, board_id):
        board = get_accessible_board(user=request.user, board_id=board_id, include_archived=True)
        require_board_manager(user=request.user, board=board)
        form = OwnershipTransferForm(request.POST, board=board)
        if form.is_valid():
            transfer_board_ownership(actor=request.user, board=board, new_owner=form.cleaned_data["new_owner"])
            messages.success(request, "Proprietatea board-ului a fost transferată.")
        else:
            messages.error(request, "Alege un membru activ.")
        return redirect("tasks:board_settings", board_id=board.pk)


class BoardArchiveView(LoginRequiredMixin, View):
    def post(self, request, board_id):
        board = get_accessible_board(user=request.user, board_id=board_id, include_archived=True)
        require_board_manager(user=request.user, board=board)
        archived = request.POST.get("archived", "1") != "0"
        set_board_archived(actor=request.user, board=board, archived=archived)
        messages.success(request, "Board arhivat." if archived else "Board restaurat.")
        return redirect("tasks:board_settings", board_id=board.pk) if archived else redirect("tasks:board_kanban", board_id=board.pk)


class StageCreateView(LoginRequiredMixin, View):
    def post(self, request, board_id):
        board = get_accessible_board(user=request.user, board_id=board_id, include_archived=True)
        require_board_manager(user=request.user, board=board)
        form = StageForm(request.POST)
        if form.is_valid():
            try:
                create_stage(actor=request.user, board=board, **form.cleaned_data)
            except (ValidationError, IntegrityError) as exc:
                messages.error(request, _error_text(exc) if isinstance(exc, ValidationError) else "Există deja o etapă cu acest nume.")
            else:
                messages.success(request, "Etapă adăugată.")
        else:
            messages.error(request, "Verifică datele etapei.")
        return redirect("tasks:board_settings", board_id=board.pk)


class StageUpdateView(LoginRequiredMixin, View):
    def post(self, request, stage_id):
        stage = get_object_or_404(TaskStage.objects.select_related("board"), pk=stage_id)
        get_accessible_board(user=request.user, board_id=stage.board_id, include_archived=True)
        require_board_manager(user=request.user, board=stage.board)
        form = StageForm(request.POST, instance=stage)
        if form.is_valid():
            try:
                update_stage(actor=request.user, stage=stage, **form.cleaned_data)
            except (ValidationError, IntegrityError) as exc:
                messages.error(request, _error_text(exc) if isinstance(exc, ValidationError) else "Există deja o etapă cu acest nume.")
            else:
                messages.success(request, "Etapă actualizată.")
        else:
            messages.error(request, "Verifică datele etapei.")
        return redirect("tasks:board_settings", board_id=stage.board_id)


class StagePositionView(LoginRequiredMixin, View):
    def post(self, request, stage_id):
        stage = get_object_or_404(TaskStage.objects.select_related("board"), pk=stage_id)
        get_accessible_board(user=request.user, board_id=stage.board_id, include_archived=True)
        require_board_manager(user=request.user, board=stage.board)
        direction = -1 if request.POST.get("direction") == "up" else 1
        move_stage_position(actor=request.user, stage=stage, direction=direction)
        return redirect("tasks:board_settings", board_id=stage.board_id)


class StageDeleteView(LoginRequiredMixin, View):
    def post(self, request, stage_id):
        stage = get_object_or_404(TaskStage.objects.select_related("board"), pk=stage_id)
        get_accessible_board(user=request.user, board_id=stage.board_id, include_archived=True)
        require_board_manager(user=request.user, board=stage.board)
        form = StageDeleteForm(request.POST, stage=stage)
        if form.is_valid():
            try:
                delete_stage(actor=request.user, stage=stage, replacement=form.cleaned_data["replacement_stage"])
            except ValidationError as exc:
                messages.error(request, _error_text(exc))
            else:
                messages.success(request, "Etapa a fost eliminată, iar task-urile au fost mutate.")
        else:
            messages.error(request, "Alege o etapă validă de înlocuire.")
        return redirect("tasks:board_settings", board_id=stage.board_id)


class BoardStateView(LoginRequiredMixin, View):
    def get(self, request, board_id):
        board = get_accessible_board(user=request.user, board_id=board_id)
        tasks = list(visible_board_tasks(user=request.user, board=board).order_by("stage__position", "rank", "pk"))
        payload = [
            {
                "id": str(task.pk),
                "stageId": str(task.stage_id),
                "rank": task.rank,
                "version": task.version,
                "title": task.title,
                "assignee": task.assignee.get_full_name() or task.assignee.get_username(),
                "priority": task.priority,
                "startAt": task.start_at.isoformat() if task.start_at else None,
                "createdAt": task.created_at.isoformat(),
                "dueAt": task.due_at.isoformat(),
                "completedAt": task.completed_at.isoformat() if task.completed_at else None,
            }
            for task in tasks
        ]
        signature = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
        return JsonResponse({"signature": signature, "tasks": payload})
```

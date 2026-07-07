# Django app: tasks

Migrations are excluded by default. Tests are included unless `--no-tests` is used.

## `apps/tasks/__init__.py`

Size: 1 B

```python

```

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

## `apps/tasks/AGENTS.md`

Size: 1.9 KB

````markdown
# Tasks App Instructions

## Scope

This app owns collaborative boards, memberships, stages, task persistence, task-list and Kanban views, deadline timers, and the reusable cross-app task-creation contract.

## Read before editing

- Root `AGENTS.md`.
- `coding-standards.md`.
- `frontend.md` for UI/template work.
- This file.
- Only the files for the selected workflow.

Use `codex-context/apps/tasks.md` only when a path is unknown.

## Architecture

- Keep request validation in `forms.py`.
- Keep reusable invariants in `validators.py`.
- Keep writes in `services.py`.
- Keep permission-filtered reads in `selectors.py`.
- All pages and endpoints require authentication.
- Ordinary members see tasks they created or received.
- Board owners and staff see all tasks on the relevant board.
- Creators and staff edit/archive tasks.
- Creators, assignees, and staff may move tasks.
- PostgreSQL is authoritative.
- JavaScript enhances timers, polling, dialogs, and drag-and-drop only.
- Use POST with CSRF for every state change.
- Return 404 for inaccessible boards and tasks.

## Reuse and UI standards

- Reuse existing board, task, stage, member, message, and action patterns.
- Extend `layouts/base.html` and use shared semantic theme tokens.
- Keep task lists horizontally usable on narrow screens.
- Preserve native form fallback for task stage changes.
- Board settings must use compact structured rows, not decorative rounded cards.
- Kanban stage dragging and ordering must show obvious active, drop, moved, disabled, and destructive states.
- Destructive stage/task actions should use consistent bin/trash icon treatment with accessible labels.
- Do not hide replacement or destructive behavior behind vague controls.

## Focused checks

```powershell
python manage.py test apps.tasks
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py tailwind build
```
````

## `apps/tasks/apps.py`

Size: 148 B

```python
from django.apps import AppConfig


class TasksConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.tasks"

```

## `apps/tasks/forms.py`

Size: 6.2 KB

```python
from django import forms
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import BoardMembership, Task, TaskBoard, TaskStage


INPUT_CLASS = "input input-bordered input-sm w-full"
SELECT_CLASS = "select select-bordered select-sm w-full"
TEXTAREA_CLASS = "textarea textarea-bordered min-h-24 w-full"


class BoardForm(forms.ModelForm):
    class Meta:
        model = TaskBoard
        fields = ("name",)
        labels = {"name": "Nume board"}
        widgets = {"name": forms.TextInput(attrs={"class": INPUT_CLASS, "autofocus": True})}


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("title", "description", "assignee", "stage", "priority", "start_at", "due_at")
        labels = {
            "title": "Titlu",
            "description": "Descriere",
            "assignee": "Responsabil",
            "stage": "Etapă",
            "priority": "Prioritate",
            "start_at": "Începe la",
            "due_at": "Termen",
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": INPUT_CLASS, "autocomplete": "off"}),
            "description": forms.Textarea(attrs={"class": TEXTAREA_CLASS, "rows": 4}),
            "assignee": forms.Select(attrs={"class": SELECT_CLASS}),
            "stage": forms.Select(attrs={"class": SELECT_CLASS}),
            "priority": forms.Select(attrs={"class": SELECT_CLASS}),
            "start_at": forms.DateTimeInput(attrs={"class": INPUT_CLASS, "type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
            "due_at": forms.DateTimeInput(attrs={"class": INPUT_CLASS, "type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        }

    def __init__(self, *args, board: TaskBoard, actor, **kwargs):
        super().__init__(*args, **kwargs)
        self.board = board
        self.actor = actor
        self.fields["assignee"].queryset = get_user_model().objects.filter(
            task_board_memberships__board=board,
            is_active=True,
        ).distinct().order_by("first_name", "last_name", "username")
        self.fields["stage"].queryset = board.stages.order_by("position")
        self.fields["assignee"].label_from_instance = lambda user: user.get_full_name() or user.get_username()
        self.fields["stage"].label_from_instance = lambda stage: stage.name
        self.fields["start_at"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["due_at"].input_formats = ("%Y-%m-%dT%H:%M",)
        if not self.is_bound and self.instance._state.adding:
            self.initial["assignee"] = actor.pk if self.fields["assignee"].queryset.filter(pk=actor.pk).exists() else None
            self.initial["stage"] = board.stages.filter(is_terminal=False).order_by("position").first()

    def clean(self):
        cleaned = super().clean()
        due_at = cleaned.get("due_at")
        start_at = cleaned.get("start_at")
        baseline = start_at or (
            self.instance.created_at
            if not self.instance._state.adding and self.instance.created_at
            else timezone.now()
        )
        if due_at and due_at <= baseline:
            self.add_error("due_at", "Termenul trebuie să fie după începutul task-ului.")
        stage = cleaned.get("stage")
        assignee = cleaned.get("assignee")
        if stage and stage.board_id != self.board.pk:
            self.add_error("stage", "Etapa nu aparține acestui board.")
        if assignee and not BoardMembership.objects.filter(board=self.board, user=assignee, user__is_active=True).exists():
            self.add_error("assignee", "Responsabilul trebuie să fie membru activ.")
        return cleaned


class MemberAddForm(forms.Form):
    user = forms.ModelChoiceField(label="Utilizator", queryset=get_user_model().objects.none())

    def __init__(self, *args, board: TaskBoard, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user"].queryset = get_user_model().objects.filter(is_active=True).exclude(
            task_board_memberships__board=board
        ).order_by("first_name", "last_name", "username")
        self.fields["user"].widget.attrs["class"] = SELECT_CLASS
        self.fields["user"].label_from_instance = lambda user: user.get_full_name() or user.get_username()


class OwnershipTransferForm(forms.Form):
    new_owner = forms.ModelChoiceField(label="Proprietar nou", queryset=get_user_model().objects.none())

    def __init__(self, *args, board: TaskBoard, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_owner"].queryset = get_user_model().objects.filter(
            task_board_memberships__board=board,
            is_active=True,
        ).exclude(pk=board.owner_id).order_by("first_name", "last_name", "username")
        self.fields["new_owner"].widget.attrs["class"] = SELECT_CLASS
        self.fields["new_owner"].label_from_instance = lambda user: user.get_full_name() or user.get_username()


class StageForm(forms.ModelForm):
    class Meta:
        model = TaskStage
        fields = ("name", "tone", "is_terminal")
        labels = {"name": "Nume", "tone": "Ton semantic", "is_terminal": "Etapă finală"}
        widgets = {
            "name": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "tone": forms.Select(attrs={"class": SELECT_CLASS}),
            "is_terminal": forms.CheckboxInput(attrs={"class": "checkbox checkbox-primary checkbox-sm"}),
        }


class StageDeleteForm(forms.Form):
    replacement_stage = forms.ModelChoiceField(label="Mută task-urile în", queryset=TaskStage.objects.none())

    def __init__(self, *args, stage: TaskStage, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["replacement_stage"].queryset = stage.board.stages.exclude(pk=stage.pk).order_by("position")
        self.fields["replacement_stage"].widget.attrs["class"] = SELECT_CLASS
        self.fields["replacement_stage"].label_from_instance = lambda item: item.name


class TaskMoveForm(forms.Form):
    stage = forms.ModelChoiceField(queryset=TaskStage.objects.none())
    target_index = forms.IntegerField(min_value=0)
    expected_version = forms.IntegerField(min_value=1)

    def __init__(self, *args, board: TaskBoard, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["stage"].queryset = board.stages.order_by("position")
```

## `apps/tasks/IMPLEMENTATION_PLAN.md`

Size: 6.6 KB

````markdown
# Collaborative Tasks App — Phased Implementation Plan

## Plan Storage

This plan is stored at `apps/tasks/IMPLEMENTATION_PLAN.md` alongside the application it governs.

Approved design references:

- Kanban: `C:/Users/Cristi Popa/.codex/generated_images/019f320b-e61f-7ca0-b13b-43e7bc570701/exec-c2a81d2e-9a74-4d00-b232-9b38035a456c.png`
- List: `C:/Users/Cristi Popa/.codex/generated_images/019f320b-e61f-7ca0-b13b-43e7bc570701/exec-ee827e62-a37a-4c4e-b0ad-ed1ccd53d9eb.png`

## Phase 1 — Application Scaffold

- Create the Django `apps.tasks` package, app configuration, namespaced URLs, templates, static directories, tests, and app-specific `AGENTS.md`.
- Register the app in settings and mount it at `/tasks/`.
- Activate the existing sidebar “Task-uri” item.
- Add the app templates and scripts to Tailwind `@source`.
- Require authentication on every task-app page.

Verification gate:

- `python manage.py check`
- Sidebar link resolves and anonymous access redirects to login.

## Phase 2 — Persistence and Domain Rules

Add an initial migration containing:

- `TaskBoard`: UUID, name, owner, archive state, timestamps.
- `BoardMembership`: unique board/user membership.
- `TaskStage`: board, name, ordered position, semantic tone, terminal flag.
- `Task`: UUID, board, creator, assignee, stage, title, description, low/medium/high priority, optional start time, required due time, manual rank, completion/archive timestamps, origin metadata, timestamps.

Enforce:

- Board names unique per owner and stage names unique per board.
- Board creator automatically becomes owner and member.
- Assignments limited to active board members.
- Due time must follow `start_at`, or creation time when no start is supplied.
- Every board retains at least one terminal and one non-terminal stage.
- New boards receive `De făcut`, `În lucru`, `Blocat`, and terminal `Finalizat`.
- Entering a terminal stage records `completed_at`; leaving it reopens the task.
- Archive tasks and boards instead of deleting them.

Verification gate:

- Model and validation tests.
- `python manage.py makemigrations --check --dry-run`

## Phase 3 — Services, Selectors, and Authorization

- Put all writes and transactional workflows in `services.py`.
- Put visibility-filtered reads in `selectors.py`.
- Put request validation in `forms.py` and reusable invariants in `validators.py`.
- Ordinary members see tasks they created or received.
- Board owners and staff see every task in the relevant board.
- Creators and staff edit, reassign, archive, or restore tasks.
- Assignees may move visible tasks between stages.
- Board owners and staff manage membership and stages.
- Block member removal while active tasks remain assigned to that member.
- Require ownership transfer before removing the board owner.
- Stage deletion requires a replacement stage and transactionally moves existing tasks.

Expose the reusable integration interface:

```python
create_task(
    *,
    actor,
    board,
    assignee,
    title,
    due_at,
    description="",
    priority="medium",
    start_at=None,
    stage=None,
    origin=None,
)
```

Use a nullable `TaskOrigin(app, type, object_id, label, url)` structure. Validate origin URLs as safe application links. Emit assignment and reassignment events after commit for future notification listeners, without adding notification UI or delivery.

Verification gate:

- Authorization, cross-user 404, membership, stage-transition, archive, and integration-service tests.

## Phase 4 — Board Management

- Add board creation and settings pages.
- Support member addition/removal, ownership transfer, archive/restore, and active-user assignment choices.
- Support custom stage creation, renaming, semantic tone, terminal status, reordering, and deletion with a required replacement.
- Restrict settings controls to the board owner and staff.
- Keep PostgreSQL and server validation authoritative.

Verification gate:

- Board lifecycle, membership, ownership, stage invariants, and automatic task-move tests.

## Phase 5 — Personal Hub and List View

Implement “Task-urile mele” using the approved list concept:

- Aggregate tasks created by or assigned to the user.
- Allow staff to switch to all visible tasks.
- Add board, relationship, stage, priority, search, and deadline-order filters.
- Add pagination and responsive horizontal table scrolling.
- Provide board selection and direct Kanban navigation.
- Add server-validated task create/edit forms, progressively enhanced with daisyUI dialogs.
- Show origin links when source metadata exists.

Verification gate:

- Filter, pagination, visibility, invalid-form, archive, back-navigation, and narrow-screen tests.

## Phase 6 — Kanban, Ordering, and Live Behaviour

Implement the approved Kanban concept:

- Board-specific Kanban and list tabs.
- Persist same-stage ordering and cross-stage movement.
- Provide accessible drag-and-drop plus a keyboard/non-JavaScript stage-change fallback.
- POST moves with target stage, target index, and expected task version.
- Lock affected rows, reindex both stages, and return `409` for stale changes.
- Add a permission-filtered board-state JSON endpoint.
- Poll approximately every 30 seconds and reconcile the complete visible board snapshot.

Live timer behaviour:

- Use `start_at` or `created_at` as the baseline.
- Success through 50% elapsed, warning from 50–80%, and error after 80% or overdue.
- Update displayed countdowns every second from server-provided ISO timestamps.
- Terminal tasks display `Finalizat` and stop urgency updates.
- JavaScript never owns validation or persistence.

Verification gate:

- Movement, ordering, concurrency, polling visibility, reopening, timer thresholds, keyboard operation, and CSRF tests.

## Phase 7 — Final QA and Context Generation

Run:

- `python manage.py test apps.tasks`
- `python manage.py check`
- `python manage.py makemigrations --check --dry-run`
- `python manage.py tailwind build`

Use the Browser plugin to verify desktop and narrow-screen behaviour, falling back to Playwright only if unavailable. Compare the rendered Kanban and list views against the approved concepts, including layout, typography, semantic colors, timer states, filtering, dialogs, drag behaviour, and scrolling.

Finally run:

```powershell
.\generate_codex_context.bat
```

Review the generated task context and report files changed, migration details, checks run, visual QA, and remaining manual checks.

## Deferred Scope

- Comments, attachments, labels, recurring tasks, and activity history.
- In-app or email notification delivery.
- WebSockets.
- Concrete “Adaugă ca task” buttons in existing applications.
- Permanent deletion.
````

## `apps/tasks/models.py`

Size: 6.1 KB

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

## `apps/tasks/selectors.py`

Size: 2.5 KB

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

## `apps/tasks/services.py`

Size: 12.4 KB

```python
from dataclasses import dataclass

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Max
from django.utils import timezone

from .models import BoardMembership, Task, TaskBoard, TaskStage
from .selectors import user_can_edit_task, user_can_manage_board, user_can_move_task
from .signals import task_assigned, task_reassigned
from .validators import validate_origin_url, validate_stage_balance


DEFAULT_STAGES = (
    ("De făcut", TaskStage.Tone.INFO, False),
    ("În lucru", TaskStage.Tone.INFO, False),
    ("Blocat", TaskStage.Tone.ERROR, False),
    ("Finalizat", TaskStage.Tone.SUCCESS, True),
)


def _next_integer(value) -> int:
    return 0 if value is None else value + 1


@dataclass(frozen=True)
class TaskOrigin:
    app: str
    type: str
    object_id: str
    label: str = ""
    url: str = ""


def _require_board_manager(*, actor, board: TaskBoard) -> None:
    if not user_can_manage_board(user=actor, board=board):
        raise ValidationError("Nu poți administra acest board.")


def _require_board_member(*, board: TaskBoard, user) -> None:
    if not user.is_active or not BoardMembership.objects.filter(board=board, user=user).exists():
        raise ValidationError("Responsabilul trebuie să fie membru activ al board-ului.")


@transaction.atomic
def create_board(*, actor, name: str) -> TaskBoard:
    board = TaskBoard.objects.create(owner=actor, name=name.strip())
    BoardMembership.objects.create(board=board, user=actor)
    TaskStage.objects.bulk_create(
        [
            TaskStage(board=board, name=stage_name, tone=tone, is_terminal=terminal, position=index)
            for index, (stage_name, tone, terminal) in enumerate(DEFAULT_STAGES)
        ]
    )
    return board


@transaction.atomic
def add_board_member(*, actor, board: TaskBoard, user) -> BoardMembership:
    _require_board_manager(actor=actor, board=board)
    if not user.is_active:
        raise ValidationError("Poți adăuga doar utilizatori activi.")
    membership, _ = BoardMembership.objects.get_or_create(board=board, user=user)
    return membership


@transaction.atomic
def remove_board_member(*, actor, board: TaskBoard, user) -> None:
    _require_board_manager(actor=actor, board=board)
    if board.owner_id == user.pk:
        raise ValidationError("Transferă proprietatea înainte de a elimina proprietarul.")
    has_active_tasks = Task.objects.filter(
        board=board,
        assignee=user,
        archived_at__isnull=True,
        stage__is_terminal=False,
    ).exists()
    if has_active_tasks:
        raise ValidationError("Reatribuie task-urile active înainte de a elimina membrul.")
    BoardMembership.objects.filter(board=board, user=user).delete()


@transaction.atomic
def transfer_board_ownership(*, actor, board: TaskBoard, new_owner) -> TaskBoard:
    _require_board_manager(actor=actor, board=board)
    _require_board_member(board=board, user=new_owner)
    board.owner = new_owner
    board.save(update_fields=("owner", "updated_at"))
    return board


@transaction.atomic
def set_board_archived(*, actor, board: TaskBoard, archived: bool) -> TaskBoard:
    _require_board_manager(actor=actor, board=board)
    board.is_archived = archived
    board.save(update_fields=("is_archived", "updated_at"))
    return board


@transaction.atomic
def create_stage(*, actor, board: TaskBoard, name: str, tone: str, is_terminal: bool) -> TaskStage:
    _require_board_manager(actor=actor, board=board)
    position = _next_integer(board.stages.aggregate(value=Max("position"))["value"])
    return TaskStage.objects.create(
        board=board,
        name=name.strip(),
        tone=tone,
        is_terminal=is_terminal,
        position=position,
    )


@transaction.atomic
def update_stage(*, actor, stage: TaskStage, name: str, tone: str, is_terminal: bool) -> TaskStage:
    _require_board_manager(actor=actor, board=stage.board)
    stages = list(stage.board.stages.exclude(pk=stage.pk))
    terminal_count = sum(item.is_terminal for item in stages) + int(is_terminal)
    validate_stage_balance(
        terminal_count=terminal_count,
        non_terminal_count=len(stages) + 1 - terminal_count,
    )
    became_terminal = not stage.is_terminal and is_terminal
    became_active = stage.is_terminal and not is_terminal
    stage.name = name.strip()
    stage.tone = tone
    stage.is_terminal = is_terminal
    stage.save(update_fields=("name", "tone", "is_terminal", "updated_at"))
    if became_terminal:
        Task.objects.filter(stage=stage, completed_at__isnull=True).update(
            completed_at=timezone.now(),
            updated_at=timezone.now(),
        )
    elif became_active:
        Task.objects.filter(stage=stage).update(completed_at=None, updated_at=timezone.now())
    return stage


@transaction.atomic
def move_stage_position(*, actor, stage: TaskStage, direction: int) -> None:
    _require_board_manager(actor=actor, board=stage.board)
    ordered = list(stage.board.stages.select_for_update().order_by("position", "created_at"))
    current = ordered.index(stage)
    target = max(0, min(len(ordered) - 1, current + direction))
    if target == current:
        return
    ordered[current], ordered[target] = ordered[target], ordered[current]
    for position, item in enumerate(ordered):
        item.position = position
    TaskStage.objects.bulk_update(ordered, ("position",))


@transaction.atomic
def delete_stage(*, actor, stage: TaskStage, replacement: TaskStage) -> None:
    _require_board_manager(actor=actor, board=stage.board)
    if replacement.board_id != stage.board_id or replacement.pk == stage.pk:
        raise ValidationError("Alege o etapă de înlocuire din același board.")
    remaining = list(stage.board.stages.exclude(pk=stage.pk))
    validate_stage_balance(
        terminal_count=sum(item.is_terminal for item in remaining),
        non_terminal_count=sum(not item.is_terminal for item in remaining),
    )
    tasks = list(Task.objects.select_for_update().filter(stage=stage).order_by("rank", "created_at"))
    next_rank = _next_integer(Task.objects.filter(stage=replacement).aggregate(value=Max("rank"))["value"])
    now = timezone.now()
    for offset, task in enumerate(tasks):
        task.stage = replacement
        task.rank = next_rank + offset
        task.completed_at = now if replacement.is_terminal else None
        task.version += 1
        task.updated_at = now
    Task.objects.bulk_update(tasks, ("stage", "rank", "completed_at", "version", "updated_at"))
    stage.delete()
    ordered = list(stage.board.stages.order_by("position", "created_at"))
    for position, item in enumerate(ordered):
        item.position = position
    TaskStage.objects.bulk_update(ordered, ("position",))


def _origin_values(origin: TaskOrigin | None) -> dict:
    if origin is None:
        return {}
    validate_origin_url(origin.url)
    return {
        "origin_app": origin.app[:100],
        "origin_type": origin.type[:100],
        "origin_object_id": str(origin.object_id)[:255],
        "origin_label": origin.label[:200],
        "origin_url": origin.url[:500],
    }


@transaction.atomic
def create_task(
    *,
    actor,
    board: TaskBoard,
    assignee,
    title: str,
    due_at,
    description: str = "",
    priority: str = Task.Priority.MEDIUM,
    start_at=None,
    stage: TaskStage | None = None,
    origin: TaskOrigin | None = None,
) -> Task:
    if board.is_archived:
        raise ValidationError("Nu poți adăuga task-uri într-un board arhivat.")
    if not actor.is_staff and not BoardMembership.objects.filter(board=board, user=actor).exists():
        raise ValidationError("Trebuie să fii membru pentru a crea task-uri.")
    _require_board_member(board=board, user=assignee)
    stage = stage or board.stages.filter(is_terminal=False).order_by("position").first()
    if stage is None or stage.board_id != board.pk:
        raise ValidationError("Alege o etapă validă din board.")
    baseline = start_at or timezone.now()
    if due_at <= baseline:
        raise ValidationError({"due_at": "Termenul trebuie să fie după începutul task-ului."})
    rank = _next_integer(Task.objects.filter(stage=stage).aggregate(value=Max("rank"))["value"])
    task = Task.objects.create(
        board=board,
        creator=actor,
        assignee=assignee,
        stage=stage,
        title=title.strip(),
        description=description.strip(),
        priority=priority,
        start_at=start_at,
        due_at=due_at,
        rank=rank,
        completed_at=timezone.now() if stage.is_terminal else None,
        **_origin_values(origin),
    )
    transaction.on_commit(lambda: task_assigned.send(sender=Task, task=task, actor=actor))
    return task


@transaction.atomic
def update_task(
    *, actor, task: Task, assignee, title: str, due_at, description: str,
    priority: str, start_at, stage: TaskStage,
) -> Task:
    if not user_can_edit_task(user=actor, task=task):
        raise ValidationError("Nu poți edita acest task.")
    _require_board_member(board=task.board, user=assignee)
    if stage.board_id != task.board_id:
        raise ValidationError("Etapa trebuie să aparțină board-ului task-ului.")
    baseline = start_at or task.created_at
    if due_at <= baseline:
        raise ValidationError({"due_at": "Termenul trebuie să fie după începutul task-ului."})
    previous_assignee = task.assignee
    stage_changed = task.stage_id != stage.pk
    task.assignee = assignee
    task.title = title.strip()
    task.description = description.strip()
    task.priority = priority
    task.start_at = start_at
    task.due_at = due_at
    task.stage = stage
    if stage_changed:
        task.rank = _next_integer(Task.objects.filter(stage=stage).aggregate(value=Max("rank"))["value"])
    task.completed_at = timezone.now() if stage.is_terminal else None
    task.version += 1
    task.save()
    if previous_assignee.pk != assignee.pk:
        transaction.on_commit(
            lambda: task_reassigned.send(
                sender=Task,
                task=task,
                actor=actor,
                previous_assignee=previous_assignee,
            )
        )
    return task


@transaction.atomic
def move_task(*, actor, task: Task, target_stage: TaskStage, target_index: int, expected_version: int) -> Task:
    locked = Task.objects.select_for_update().select_related("board", "stage", "assignee", "creator").get(pk=task.pk)
    if not user_can_move_task(user=actor, task=locked):
        raise ValidationError("Nu poți muta acest task.")
    if locked.version != expected_version:
        raise ValidationError("Task-ul a fost modificat de alt utilizator.", code="stale")
    if target_stage.board_id != locked.board_id:
        raise ValidationError("Etapa țintă nu aparține board-ului task-ului.")
    source_stage_id = locked.stage_id
    affected = list(
        Task.objects.select_for_update()
        .filter(stage_id__in={source_stage_id, target_stage.pk}, archived_at__isnull=True)
        .order_by("rank", "created_at")
    )
    source_items = [item for item in affected if item.stage_id == source_stage_id and item.pk != locked.pk]
    target_items = source_items if source_stage_id == target_stage.pk else [
        item for item in affected if item.stage_id == target_stage.pk and item.pk != locked.pk
    ]
    target_index = max(0, min(target_index, len(target_items)))
    target_items.insert(target_index, locked)
    now = timezone.now()
    changed = []
    if source_stage_id != target_stage.pk:
        for rank, item in enumerate(source_items):
            if item.rank != rank:
                item.rank = rank
                changed.append(item)
    for rank, item in enumerate(target_items):
        if item.pk == locked.pk:
            item.stage = target_stage
            item.completed_at = now if target_stage.is_terminal else None
            item.version += 1
            item.updated_at = now
        if item.rank != rank or item.pk == locked.pk:
            item.rank = rank
            changed.append(item)
    unique_changed = list({item.pk: item for item in changed}.values())
    Task.objects.bulk_update(unique_changed, ("stage", "rank", "completed_at", "version", "updated_at"))
    locked.refresh_from_db()
    return locked


@transaction.atomic
def set_task_archived(*, actor, task: Task, archived: bool) -> Task:
    if not user_can_edit_task(user=actor, task=task):
        raise ValidationError("Nu poți arhiva acest task.")
    task.archived_at = timezone.now() if archived else None
    task.version += 1
    task.save(update_fields=("archived_at", "version", "updated_at"))
    return task
```

## `apps/tasks/signals.py`

Size: 90 B

```python
from django.dispatch import Signal


task_assigned = Signal()
task_reassigned = Signal()

```

## `apps/tasks/static/tasks/tasks.js`

Size: 11.3 KB

```javascript
(() => {
    const formatDuration = (milliseconds) => {
        const totalSeconds = Math.max(0, Math.floor(Math.abs(milliseconds) / 1000));
        const days = Math.floor(totalSeconds / 86400);
        const hours = Math.floor((totalSeconds % 86400) / 3600);
        const minutes = Math.floor((totalSeconds % 3600) / 60);
        const seconds = totalSeconds % 60;
        if (days > 0) return `${days}z ${String(hours).padStart(2, "0")}h`;
        if (hours > 0) return `${String(hours).padStart(2, "0")}h ${String(minutes).padStart(2, "0")}m`;
        return `${String(minutes).padStart(2, "0")}m ${String(seconds).padStart(2, "0")}s`;
    };

    const setTimerTone = (element, tone) => {
        element.classList.remove("border-success", "text-success", "border-warning", "text-warning", "border-error", "text-error", "border-info", "text-info", "border-base-300");
        if (tone === "success") element.classList.add("border-success", "text-success");
        else if (tone === "warning") element.classList.add("border-warning", "text-warning");
        else if (tone === "error") element.classList.add("border-error", "text-error");
        else element.classList.add("border-info", "text-info");
    };

    const updateTimers = () => {
        const now = Date.now();
        document.querySelectorAll("[data-task-timer]").forEach((element) => {
            const label = element.querySelector("[data-timer-label]");
            if (!label) return;
            if (element.dataset.completedAt) {
                label.textContent = "Finalizat";
                setTimerTone(element, "success");
                return;
            }
            const start = Date.parse(element.dataset.startAt);
            const due = Date.parse(element.dataset.dueAt);
            if (!Number.isFinite(start) || !Number.isFinite(due) || due <= start) {
                label.textContent = "Termen invalid";
                setTimerTone(element, "error");
                return;
            }
            if (now < start) {
                label.textContent = `Începe în ${formatDuration(start - now)}`;
                setTimerTone(element, "success");
                return;
            }
            const progress = (now - start) / (due - start);
            if (now >= due) {
                label.textContent = `Depășit cu ${formatDuration(now - due)}`;
                setTimerTone(element, "error");
            } else {
                label.textContent = `${formatDuration(due - now)} rămase`;
                setTimerTone(element, progress < 0.5 ? "success" : progress < 0.8 ? "warning" : "error");
            }
        });
    };

    let timerInterval = null;
    const initTimers = () => {
        updateTimers();
        if (!timerInterval && document.querySelector("[data-task-timer]")) {
            timerInterval = window.setInterval(updateTimers, 1000);
        }
    };

    const getDialog = () => document.getElementById("task-create-dialog");
    const getRoot = () => document.querySelector("[data-kanban-root]");
    const getCsrf = () => document.querySelector("[name=csrfmiddlewaretoken]")?.value || "";
    let draggedCard = null;
    let requestInFlight = false;
    let knownSignature = null;
    let pollInterval = null;

    const updateCounts = () => document.querySelectorAll("[data-stage-column]").forEach((column) => {
        const count = column.querySelectorAll(":scope [data-stage-cards] > [data-task-card]").length;
        const target = column.querySelector("[data-stage-count]");
        if (target) target.textContent = String(count);
        const emptyState = column.querySelector("[data-stage-empty]");
        if (emptyState) emptyState.classList.toggle("hidden", count > 0);
    });

    const setDropState = (container, active) => {
        container.classList.toggle("outline", active);
        container.classList.toggle("outline-2", active);
        container.classList.toggle("outline-primary", active);
        container.classList.toggle("outline-offset-2", active);
        container.classList.toggle("border-primary", active);
        container.classList.toggle("bg-primary/10", active);
    };

    const setDragContext = (active) => {
        const board = document.querySelector("[data-kanban-board]");
        if (board) board.toggleAttribute("data-kanban-dragging", active);
        document.querySelectorAll("[data-stage-drop-zone]").forEach((container) => {
            container.classList.toggle("border-dashed", active);
            container.classList.toggle("border-base-300", active);
            container.classList.toggle("bg-base-100", active);
            container.classList.toggle("opacity-90", active);
        });
    };

    const markMoved = (card) => {
        card.classList.add("ring-2", "ring-success", "bg-success/10");
        window.setTimeout(() => card.classList.remove("ring-2", "ring-success", "bg-success/10"), 900);
    };

    const setDragDisabled = (disabled) => {
        document.querySelectorAll("[data-task-card][draggable=true]").forEach((card) => {
            card.classList.toggle("opacity-60", disabled);
            card.toggleAttribute("aria-disabled", disabled);
        });
    };

    const updateMovedCardTimer = (card, taskPayload) => {
        const timer = card.querySelector("[data-task-timer]");
        if (!timer || !Object.prototype.hasOwnProperty.call(taskPayload, "completedAt")) return;
        if (taskPayload.completedAt) timer.dataset.completedAt = taskPayload.completedAt;
        else delete timer.dataset.completedAt;
        updateTimers();
    };

    const initDragDrop = () => {
        document.querySelectorAll("[data-task-card][draggable=true]:not([data-kanban-drag-bound])").forEach((card) => {
            card.dataset.kanbanDragBound = "true";
            card.addEventListener("dragstart", () => {
                if (requestInFlight) return;
                draggedCard = card;
                setDragContext(true);
                card.classList.add("opacity-70", "ring-2", "ring-primary", "cursor-grabbing");
            });
            card.addEventListener("dragend", () => {
                card.classList.remove("opacity-70", "ring-2", "ring-primary", "cursor-grabbing");
                document.querySelectorAll("[data-stage-cards]").forEach((container) => setDropState(container, false));
                setDragContext(false);
                draggedCard = null;
            });
        });

        document.querySelectorAll("[data-stage-cards]:not([data-kanban-drop-bound])").forEach((container) => {
            container.dataset.kanbanDropBound = "true";
            container.addEventListener("dragover", (event) => {
                event.preventDefault();
                if (draggedCard && !requestInFlight) setDropState(container, true);
            });
            container.addEventListener("dragleave", (event) => {
                if (!container.contains(event.relatedTarget)) setDropState(container, false);
            });
            container.addEventListener("drop", async (event) => {
                event.preventDefault();
                setDropState(container, false);
                if (!draggedCard || requestInFlight) return;
                const card = draggedCard;
                const stageColumn = container.closest("[data-stage-column]");
                if (!stageColumn) return;
                const cards = Array.from(container.querySelectorAll(":scope > [data-task-card]")).filter((item) => item !== card);
                const target = event.target.closest("[data-task-card]");
                const targetIndex = target && target !== card ? cards.indexOf(target) : cards.length;
                const oldParent = card.parentElement;
                const reference = cards[targetIndex] || container.querySelector("[data-open-task-dialog]");
                container.insertBefore(card, reference || null);
                updateCounts();
                requestInFlight = true;
                setDragDisabled(true);
                card.setAttribute("aria-busy", "true");
                try {
                    const response = await fetch(card.dataset.moveUrl, {
                        method: "POST",
                        headers: {"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded", "X-CSRFToken": getCsrf()},
                        body: new URLSearchParams({stage: stageColumn.dataset.stageId, target_index: String(targetIndex), expected_version: card.dataset.taskVersion}),
                    });
                    const payload = await response.json();
                    if (!response.ok) throw new Error(payload.error || "Mutarea nu a putut fi salvată.");
                    card.dataset.taskVersion = String(payload.task.version);
                    const fallbackVersion = card.querySelector("[name=expected_version]");
                    if (fallbackVersion) fallbackVersion.value = String(payload.task.version);
                    const fallbackStage = card.querySelector("[name=stage]");
                    if (fallbackStage) fallbackStage.value = payload.task.stageId;
                    updateMovedCardTimer(card, payload.task);
                    knownSignature = null;
                    markMoved(card);
                } catch (error) {
                    oldParent.insertBefore(card, oldParent.querySelector("[data-open-task-dialog]") || null);
                    updateCounts();
                    window.alert(error.message);
                } finally {
                    card.removeAttribute("aria-busy");
                    setDragDisabled(false);
                    requestInFlight = false;
                }
            });
        });
    };

    const pollState = async () => {
        const root = getRoot();
        const dialog = getDialog();
        if (!root || document.hidden || requestInFlight || dialog?.open) return;
        try {
            const response = await fetch(root.dataset.stateUrl, {headers: {"Accept": "application/json"}});
            if (!response.ok) return;
            const payload = await response.json();
            if (knownSignature === null) knownSignature = payload.signature;
            else if (knownSignature !== payload.signature) window.location.reload();
        } catch (_) {
            // A later poll retries; local task operations remain server-authoritative.
        }
    };

    const initPolling = () => {
        if (!pollInterval && getRoot()) {
            pollState();
            pollInterval = window.setInterval(pollState, 30000);
        }
    };

    const initKanban = ({resetSignature = false} = {}) => {
        initTimers();
        initDragDrop();
        if (resetSignature) knownSignature = null;
        initPolling();
    };

    document.addEventListener("change", (event) => {
        const select = event.target.closest("[data-board-switcher]");
        if (select) window.location.assign(select.value);
    });

    document.addEventListener("click", (event) => {
        const openButton = event.target.closest("[data-open-task-dialog]");
        if (openButton) getDialog()?.showModal();
        const closeButton = event.target.closest("[data-close-task-dialog]");
        if (closeButton) getDialog()?.close();
    });

    document.addEventListener("taskKanban:taskCreated", () => getDialog()?.close());
    document.addEventListener("htmx:afterSwap", () => initKanban({resetSignature: true}));
    document.addEventListener("htmx:oobAfterSwap", () => initKanban({resetSignature: true}));

    initKanban();
})();
```

## `apps/tasks/templates/tasks/board_form.html`

Size: 563 B

```html
{% extends "layouts/base.html" %}
{% block title %}Board nou | Task-uri{% endblock %}
{% block content %}
<section class="mx-auto max-w-xl space-y-5">
    <div>
        <p class="text-xs text-muted"><a href="{% url 'tasks:index' %}" class="hover:text-primary">Task-uri</a> / Board nou</p>
        <h1 class="ops-title mt-1 text-2xl font-bold">Creeaz&#259; un board</h1>
        <p class="mt-1 text-sm text-muted">Vei deveni proprietar &#537;i membru al board-ului.</p>
    </div>
    {% include "tasks/includes/board_form_panel.html" %}
</section>
{% endblock %}
```

## `apps/tasks/templates/tasks/board_kanban.html`

Size: 4.2 KB

```html
{% extends "layouts/base.html" %}
{% load static %}

{% block title %}{{ board.name }} | Task-uri{% endblock %}

{% block content %}
<section class="space-y-4" data-kanban-root data-state-url="{{ state_url }}">
    {% include "tasks/includes/kanban_messages.html" %}
    <div class="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div class="min-w-0">
            <p class="text-xs font-medium text-muted"><a href="{% url 'tasks:index' %}" class="hover:text-primary">Task-uri</a> / Board</p>
            <h1 class="ops-title mt-1 truncate text-2xl font-bold sm:text-[2rem]">{{ board.name }}</h1>
            <div class="mt-3 flex flex-wrap items-center gap-2">
                <label class="sr-only" for="board-switcher">Schimbă board-ul</label>
                <select id="board-switcher" class="select select-bordered select-sm" data-board-switcher>
                    {% for item in boards %}<option value="{% url 'tasks:board_kanban' item.pk %}"{% if item.pk == board.pk %} selected{% endif %}>{{ item.name }}</option>{% endfor %}
                </select>
                <div class="flex -space-x-2" aria-label="{{ members|length }} membri">
                    {% for membership in members|slice:':5' %}<span class="flex h-8 w-8 items-center justify-center rounded-full border-2 border-base-100 bg-base-200 text-[10px] font-bold" title="{{ membership.user.get_full_name|default:membership.user.username }}">{{ membership.user.username|slice:':2'|upper }}</span>{% endfor %}
                    {% if members|length > 5 %}<span class="flex h-8 w-8 items-center justify-center rounded-full border-2 border-base-100 bg-base-200 text-[10px] font-bold">+{{ members|length|add:'-5' }}</span>{% endif %}
                </div>
            </div>
        </div>
        <div class="flex flex-wrap gap-2">
            {% if can_manage_board %}<a href="{% url 'tasks:board_settings' board.pk %}" class="btn btn-outline btn-sm">Setări board</a>{% endif %}
            <button type="button" class="btn btn-primary btn-sm" data-open-task-dialog>+ Task nou</button>
        </div>
    </div>

    <nav class="flex gap-5 border-b border-base-300" aria-label="Vizualizare board">
        <span class="border-b-2 border-primary px-1 pb-2 text-sm font-semibold text-primary" aria-current="page">Kanban</span>
        <a href="{% url 'tasks:board_list' board.pk %}" class="px-1 pb-2 text-sm font-medium hover:text-primary">Listă</a>
    </nav>

    <form method="get" class="grid gap-3 border-b border-base-300 pb-4 sm:grid-cols-2 lg:grid-cols-4">
        <label class="fieldset"><span class="fieldset-legend">Responsabil</span><select name="assignee" class="select select-bordered select-sm w-full"><option value="">Orice responsabil</option>{% for membership in members %}<option value="{{ membership.user_id }}"{% if filters.assignee == membership.user_id|stringformat:'s' %} selected{% endif %}>{{ membership.user.get_full_name|default:membership.user.username }}</option>{% endfor %}</select></label>
        <label class="fieldset"><span class="fieldset-legend">Prioritate</span><select name="priority" class="select select-bordered select-sm w-full"><option value="">Orice prioritate</option>{% for value,label in priority_choices %}<option value="{{ value }}"{% if filters.priority == value %} selected{% endif %}>{{ label }}</option>{% endfor %}</select></label>
        <label class="fieldset"><span class="fieldset-legend">Caută</span><input type="search" name="q" value="{{ filters.q|default:'' }}" class="input input-bordered input-sm w-full" placeholder="Caută task-uri..."></label>
        <div class="flex items-end gap-2"><button class="btn btn-primary btn-sm flex-1">Filtrează</button><a href="{% url 'tasks:board_kanban' board.pk %}" class="btn btn-ghost btn-sm">Resetează</a></div>
    </form>

    {% include "tasks/includes/kanban_board.html" %}
</section>

<dialog id="task-create-dialog" class="modal">
    <div class="modal-box max-w-2xl rounded-box border border-base-300 bg-base-100 shadow-xl">
        {% include "tasks/includes/task_create_dialog_body.html" %}
    </div>
    <form method="dialog" class="modal-backdrop"><button>Închide</button></form>
</dialog>
{% endblock %}

{% block page_scripts %}<script src="{% static 'tasks/tasks.js' %}" defer></script>{% endblock %}
```

## `apps/tasks/templates/tasks/board_list.html`

Size: 2.6 KB

```html
{% extends "layouts/base.html" %}
{% load static %}

{% block title %}{{ board.name }} — Listă | Task-uri{% endblock %}

{% block content %}
<section class="space-y-4">
    {% include "tasks/includes/messages.html" %}
    <div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div>
            <p class="text-xs text-muted"><a href="{% url 'tasks:index' %}" class="hover:text-primary">Task-uri</a> / Board</p>
            <h1 class="ops-title mt-1 text-2xl font-bold sm:text-[2rem]">{{ board.name }}</h1>
        </div>
        <div class="flex gap-2">
            {% if can_manage_board %}<a href="{% url 'tasks:board_settings' board.pk %}" class="btn btn-outline btn-sm">Setări board</a>{% endif %}
            <a href="{% url 'tasks:task_create' board.pk %}" class="btn btn-primary btn-sm">Task nou</a>
        </div>
    </div>
    <nav class="flex gap-5 border-b border-base-300">
        <a href="{% url 'tasks:board_kanban' board.pk %}" class="px-1 pb-2 text-sm font-medium hover:text-primary">Kanban</a>
        <span class="border-b-2 border-primary px-1 pb-2 text-sm font-semibold text-primary">Listă</span>
    </nav>
    <form
        method="get"
        class="grid gap-3 border-b border-base-300 pb-4 sm:grid-cols-2 lg:grid-cols-5"
        hx-get="{% url 'tasks:board_list' board.pk %}"
        hx-target="#task-list-results"
        hx-swap="outerHTML"
        hx-push-url="true"
    >
        <label class="fieldset lg:col-span-2"><span class="fieldset-legend">Caută</span><input name="q" value="{{ filters.q|default:'' }}" class="input input-bordered input-sm w-full" placeholder="Caută task-uri..."></label>
        <label class="fieldset"><span class="fieldset-legend">Prioritate</span><select name="priority" class="select select-bordered select-sm w-full"><option value="">Toate</option>{% for value,label in priority_choices %}<option value="{{ value }}"{% if filters.priority == value %} selected{% endif %}>{{ label }}</option>{% endfor %}</select></label>
        <label class="fieldset"><span class="fieldset-legend">Sortare</span><select name="sort" class="select select-bordered select-sm w-full"><option value="due_asc">Termen crescător</option><option value="due_desc"{% if filters.sort == 'due_desc' %} selected{% endif %}>Termen descrescător</option></select></label>
        <div class="flex items-end"><button class="btn btn-primary btn-sm w-full">Aplică</button></div>
    </form>
    {% include "tasks/includes/board_task_list.html" %}
</section>
{% endblock %}

{% block page_scripts %}<script src="{% static 'tasks/tasks.js' %}" defer></script>{% endblock %}
```

## `apps/tasks/templates/tasks/board_settings.html`

Size: 203 B

```html
{% extends "layouts/base.html" %}
{% block title %}Set&#259;ri {{ board.name }} | Task-uri{% endblock %}
{% block content %}
    {% include "tasks/includes/board_settings_content.html" %}
{% endblock %}
```

## `apps/tasks/templates/tasks/hub.html`

Size: 4.8 KB

```html
{% extends "layouts/base.html" %}
{% load static %}

{% block title %}Task-urile mele | Platforma TUVTK{% endblock %}

{% block content %}
<section class="space-y-5">
    {% include "tasks/includes/messages.html" %}
    <div class="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
            <h1 class="ops-title text-2xl font-bold sm:text-[2rem]">Task-urile mele</h1>
            <p class="mt-1 text-sm text-muted">Task-uri create de tine sau atribuite ție.</p>
        </div>
        <div class="flex flex-wrap gap-2">
            <a href="{% url 'tasks:board_create' %}" class="btn btn-outline btn-primary btn-sm">Board nou</a>
            {% if first_board %}<a href="{% url 'tasks:task_create' first_board.pk %}" class="btn btn-primary btn-sm">Task nou</a>{% endif %}
        </div>
    </div>

    {% if boards %}
    <div class="flex gap-2 overflow-x-auto border-b border-base-300 pb-3" aria-label="Board-uri disponibile">
        {% for board in boards %}
            <a href="{% url 'tasks:board_kanban' board.pk %}" class="btn btn-outline btn-sm shrink-0">
                {{ board.name }}
                <span class="text-xs font-normal text-muted">Kanban →</span>
            </a>
        {% endfor %}
    </div>

    <nav class="flex gap-5 border-b border-base-300" aria-label="Vizualizare task-uri">
        <span class="border-b-2 border-primary px-1 pb-2 text-sm font-semibold text-primary" aria-current="page">Listă</span>
        {% if first_board %}<a href="{% url 'tasks:board_kanban' first_board.pk %}" class="px-1 pb-2 text-sm font-medium hover:text-primary">Kanban</a>{% endif %}
    </nav>

    <form
        method="get"
        class="grid gap-3 border-b border-base-300 pb-4 sm:grid-cols-2 lg:grid-cols-8"
        hx-get="{% url 'tasks:index' %}"
        hx-target="#task-list-results"
        hx-swap="outerHTML"
        hx-push-url="true"
    >
        <label class="fieldset"><span class="fieldset-legend">Board</span><select name="board" class="select select-bordered select-sm w-full"><option value="">Toate board-urile</option>{% for board in boards %}<option value="{{ board.pk }}"{% if filters.board == board.pk|stringformat:'s' %} selected{% endif %}>{{ board.name }}</option>{% endfor %}</select></label>
        <label class="fieldset lg:col-span-2"><span class="fieldset-legend">Caută</span><input name="q" value="{{ filters.q|default:'' }}" class="input input-bordered input-sm w-full" placeholder="Caută task-uri..."></label>
        <label class="fieldset"><span class="fieldset-legend">Relație</span><select name="relation" class="select select-bordered select-sm w-full"><option value="">Toate</option><option value="assigned"{% if filters.relation == 'assigned' %} selected{% endif %}>Atribuite mie</option><option value="created"{% if filters.relation == 'created' %} selected{% endif %}>Create de mine</option>{% if request.user.is_staff %}<option value="mine"{% if filters.relation == 'mine' %} selected{% endif %}>Doar ale mele</option>{% endif %}</select></label>
        <label class="fieldset"><span class="fieldset-legend">Prioritate</span><select name="priority" class="select select-bordered select-sm w-full"><option value="">Toate</option>{% for value,label in priority_choices %}<option value="{{ value }}"{% if filters.priority == value %} selected{% endif %}>{{ label }}</option>{% endfor %}</select></label>
        <label class="fieldset"><span class="fieldset-legend">Etapă</span><select name="stage" class="select select-bordered select-sm w-full"><option value="">Toate</option>{% for stage in stage_options %}<option value="{{ stage.pk }}"{% if filters.stage == stage.pk|stringformat:'s' %} selected{% endif %}>{{ stage.board.name }} · {{ stage.name }}</option>{% endfor %}</select></label>
        <label class="fieldset"><span class="fieldset-legend">Sortare</span><select name="sort" class="select select-bordered select-sm w-full"><option value="due_asc">Termen crescător</option><option value="due_desc"{% if filters.sort == 'due_desc' %} selected{% endif %}>Termen descrescător</option></select></label>
        <div class="flex items-end gap-2"><button class="btn btn-primary btn-sm flex-1">Filtrează</button><a href="{% url 'tasks:index' %}" class="btn btn-ghost btn-sm">Resetează</a></div>
    </form>

    {% include "tasks/includes/hub_task_list.html" %}
    {% else %}
    <div class="border border-dashed border-base-300 bg-base-100 px-6 py-14 text-center">
        <h2 class="text-lg font-semibold text-base-content">Creează primul board</h2>
        <p class="mt-2 text-sm text-muted">Board-urile grupează membri, etape și task-uri colaborative.</p>
        <a href="{% url 'tasks:board_create' %}" class="btn btn-primary btn-sm mt-5">Board nou</a>
    </div>
    {% endif %}
</section>
{% endblock %}

{% block page_scripts %}<script src="{% static 'tasks/tasks.js' %}" defer></script>{% endblock %}
```

## `apps/tasks/templates/tasks/includes/board_form_panel.html`

Size: 513 B

```html
<form
    id="board-form-panel"
    method="post"
    class="space-y-4 border border-base-300 bg-base-100 p-5"
    hx-post="{% url 'tasks:board_create' %}"
    hx-target="#board-form-panel"
    hx-swap="outerHTML"
>
    {% csrf_token %}
    {% include "tasks/includes/form_fields.html" %}
    <div class="flex justify-end gap-2">
        <a href="{% url 'tasks:index' %}" class="btn btn-ghost btn-sm">Anuleaz&#259;</a>
        <button class="btn btn-primary btn-sm">Creeaz&#259; board</button>
    </div>
</form>
```

## `apps/tasks/templates/tasks/includes/board_settings_content.html`

Size: 17.1 KB

```html
<section id="board-settings-content" class="space-y-6">
    {% include "tasks/includes/messages.html" %}
    <div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div>
            <p class="text-xs text-muted"><a href="{% url 'tasks:index' %}" class="hover:text-primary">Task-uri</a> / Set&#259;ri</p>
            <h1 class="ops-title mt-1 text-2xl font-bold">{{ board.name }}</h1>
            <p class="mt-1 text-sm text-muted">Membri, proprietate &#537;i flux Kanban.</p>
        </div>
        {% if not board.is_archived %}<a href="{% url 'tasks:board_kanban' board.pk %}" class="btn btn-outline btn-sm">&#206;napoi la Kanban</a>{% endif %}
    </div>

    <div class="grid gap-5 lg:grid-cols-2">
        <section class="border border-base-300 bg-base-100 p-5">
            <h2 class="font-semibold text-base-content">Membri</h2>
            <p class="mt-1 text-xs text-muted">Task-urile pot fi atribuite doar membrilor activi.</p>
            <div class="mt-4 divide-y divide-base-300">
                {% for membership in members %}
                    <div class="flex items-center justify-between gap-3 py-3">
                        <div>
                            <p class="text-sm font-medium">{{ membership.user.get_full_name|default:membership.user.username }}</p>
                            <p class="text-xs text-muted">{% if membership.user_id == board.owner_id %}Proprietar{% else %}Membru{% endif %}{% if not membership.user.is_active %} &middot; Inactiv{% endif %}</p>
                        </div>
                        {% if membership.user_id != board.owner_id %}
                            <form method="post" action="{% url 'tasks:member_remove' board.pk membership.user_id %}" hx-post="{% url 'tasks:member_remove' board.pk membership.user_id %}" hx-target="#board-settings-content" hx-swap="outerHTML">
                                {% csrf_token %}
                                <button class="btn btn-ghost btn-xs text-error">Elimin&#259;</button>
                            </form>
                        {% endif %}
                    </div>
                {% endfor %}
            </div>
            {% if member_form.fields.user.queryset.exists %}
                <form method="post" action="{% url 'tasks:member_add' board.pk %}" class="mt-4 flex items-end gap-2" hx-post="{% url 'tasks:member_add' board.pk %}" hx-target="#board-settings-content" hx-swap="outerHTML">
                    {% csrf_token %}
                    <fieldset class="fieldset flex-1">
                        <label class="fieldset-legend" for="{{ member_form.user.id_for_label }}">Adaug&#259; membru</label>
                        {{ member_form.user }}
                        {% if member_form.user.errors %}<p class="label whitespace-normal text-xs text-error" role="alert">{{ member_form.user.errors|join:", " }}</p>{% endif %}
                    </fieldset>
                    <button class="btn btn-primary btn-sm">Adaug&#259;</button>
                </form>
            {% endif %}
        </section>

        <section class="border border-base-300 bg-base-100 p-5">
            <h2 class="font-semibold">Proprietate &#537;i arhivare</h2>
            <p class="mt-1 text-xs text-muted">Proprietarul configureaz&#259; board-ul; staff-ul p&#259;streaz&#259; acces de administrare.</p>
            {% if transfer_form.fields.new_owner.queryset.exists %}
                <form method="post" action="{% url 'tasks:ownership_transfer' board.pk %}" class="mt-4 space-y-3" hx-post="{% url 'tasks:ownership_transfer' board.pk %}" hx-target="#board-settings-content" hx-swap="outerHTML">
                    {% csrf_token %}
                    <fieldset class="fieldset">
                        <label class="fieldset-legend" for="{{ transfer_form.new_owner.id_for_label }}">Transfer&#259; proprietatea</label>
                        {{ transfer_form.new_owner }}
                        {% if transfer_form.new_owner.errors %}<p class="label whitespace-normal text-xs text-error" role="alert">{{ transfer_form.new_owner.errors|join:", " }}</p>{% endif %}
                    </fieldset>
                    <button class="btn btn-outline btn-primary btn-sm">Transfer&#259;</button>
                </form>
            {% endif %}
            <form method="post" action="{% url 'tasks:board_archive' board.pk %}" class="mt-6 border-t border-base-300 pt-4" hx-post="{% url 'tasks:board_archive' board.pk %}" hx-target="#board-settings-content" hx-swap="outerHTML">
                {% csrf_token %}
                <input type="hidden" name="archived" value="{% if board.is_archived %}0{% else %}1{% endif %}">
                <button class="btn btn-outline {% if board.is_archived %}btn-success{% else %}btn-error{% endif %} btn-sm">{% if board.is_archived %}Restaureaz&#259; board-ul{% else %}Arhiveaz&#259; board-ul{% endif %}</button>
            </form>
        </section>
    </div>

    <section class="border border-base-300 bg-base-100">
        <div class="border-b border-base-300 px-5 py-4">
            <div class="flex flex-col gap-2 lg:flex-row lg:items-start lg:justify-between">
                <div>
                    <h2 class="font-semibold">Etape Kanban</h2>
                    <p class="mt-1 text-xs text-muted">Configureaz&#259; ordinea etapelor f&#259;r&#259; s&#259; schimbi task-urile direct.</p>
                </div>
                <p class="max-w-2xl text-xs text-muted">
                    Etapele finale marcheaz&#259; task-urile ca finalizate. Etapele &#537;terse trebuie s&#259; mute task-urile existente
                    &#238;ntr-o alt&#259; etap&#259; din acela&#537;i board.
                </p>
            </div>
        </div>

        <div class="overflow-x-auto">
            <div class="min-w-[960px]">
                <div class="grid grid-cols-[4.5rem_1fr_9rem_9rem_8rem_8rem] items-center gap-3 border-b border-base-300 bg-base-200/50 px-5 py-2 text-xs font-semibold uppercase text-muted">
                    <span>Pozi&#539;ie</span>
                    <span>Etap&#259;</span>
                    <span>Ton semantic</span>
                    <span>Tip</span>
                    <span>Mutare</span>
                    <span class="text-right">Ac&#539;iuni</span>
                </div>
                <div class="divide-y divide-base-300">
                    {% for row in stage_rows %}
                        <article class="bg-base-100" x-data="{ edit: {% if row.form.errors %}true{% else %}false{% endif %} }" @keydown.escape.window="edit = false">
                            <div class="grid grid-cols-[4.5rem_1fr_9rem_9rem_8rem_8rem] items-center gap-3 px-5 py-3">
                                <div class="flex items-center gap-2">
                                    <span class="inline-flex size-8 items-center justify-center border border-base-300 bg-base-200 text-sm font-semibold tabular-nums text-base-content">{{ forloop.counter }}</span>
                                </div>
                                <div class="min-w-0">
                                    <p class="truncate text-sm font-semibold text-base-content">{{ row.stage.name }}</p>
                                </div>
                                <div>
                                    <span class="badge badge-outline badge-sm {% if row.stage.tone == 'success' %}badge-success{% elif row.stage.tone == 'error' %}badge-error{% elif row.stage.tone == 'warning' %}badge-warning{% elif row.stage.tone == 'info' %}badge-info{% endif %}">{{ row.stage.get_tone_display }}</span>
                                </div>
                                <div>
                                    {% if row.stage.is_terminal %}
                                        <span class="badge badge-success badge-outline badge-sm">Etap&#259; final&#259;</span>
                                    {% else %}
                                        <span class="badge badge-ghost badge-sm">Activ&#259;</span>
                                    {% endif %}
                                </div>
                                <form method="post" action="{% url 'tasks:stage_position' row.stage.pk %}" class="join" hx-post="{% url 'tasks:stage_position' row.stage.pk %}" hx-target="#board-settings-content" hx-swap="outerHTML">
                                    {% csrf_token %}
                                    <button name="direction" value="up" class="btn btn-ghost btn-xs join-item" aria-label="Mut&#259; etapa &#238;n sus" title="Mut&#259; etapa &#238;n sus">&uarr;</button>
                                    <button name="direction" value="down" class="btn btn-ghost btn-xs join-item" aria-label="Mut&#259; etapa &#238;n jos" title="Mut&#259; etapa &#238;n jos">&darr;</button>
                                </form>
                                <div class="flex justify-end gap-1">
                                    <button type="button" class="btn btn-square btn-ghost btn-xs text-primary hover:bg-primary/10" aria-label="Editeaz&#259; etapa" title="Editeaz&#259; etapa" @click="edit = !edit">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="size-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="m16.862 3.487 3.651 3.651M4.5 19.5l4.228-.845a2 2 0 0 0 1.024-.547L20.513 7.347a1.75 1.75 0 0 0 0-2.474l-1.386-1.386a1.75 1.75 0 0 0-2.474 0L5.892 14.248a2 2 0 0 0-.547 1.024L4.5 19.5Z" />
                                        </svg>
                                    </button>
                                    <button type="button" class="btn btn-square btn-ghost btn-xs text-error hover:bg-error/10" aria-label="&#536;terge etapa" title="&#536;terge etapa" x-on:click="$refs.deleteStageDialog.showModal()">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="size-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M6.75 7.5h10.5m-8.5 0V18a1.5 1.5 0 0 0 1.5 1.5h3.5a1.5 1.5 0 0 0 1.5-1.5V7.5m-5.25 0V5.75A1.25 1.25 0 0 1 11.25 4.5h1.5A1.25 1.25 0 0 1 14 5.75V7.5" />
                                        </svg>
                                    </button>
                                </div>
                            </div>
                            <form method="post" action="{% url 'tasks:stage_update' row.stage.pk %}" class="border-t border-base-300 bg-base-200/20 px-5 py-4" hx-post="{% url 'tasks:stage_update' row.stage.pk %}" hx-target="#board-settings-content" hx-swap="outerHTML" x-show="edit" {% if not row.form.errors %}style="display: none;"{% endif %}>
                                {% csrf_token %}
                                <div class="grid items-end gap-3 md:grid-cols-[1.4fr_1fr_auto_auto]">
                                    <fieldset class="fieldset">
                                        <label class="fieldset-legend" for="{{ row.form.name.id_for_label }}">Nume</label>
                                        {{ row.form.name }}
                                        {% if row.form.name.errors %}<p class="label whitespace-normal text-xs text-error" role="alert">{{ row.form.name.errors|join:", " }}</p>{% endif %}
                                    </fieldset>
                                    <fieldset class="fieldset">
                                        <label class="fieldset-legend" for="{{ row.form.tone.id_for_label }}">Ton semantic</label>
                                        {{ row.form.tone }}
                                        {% if row.form.tone.errors %}<p class="label whitespace-normal text-xs text-error" role="alert">{{ row.form.tone.errors|join:", " }}</p>{% endif %}
                                    </fieldset>
                                    <label class="flex h-8 items-center gap-2 text-sm">{{ row.form.is_terminal }} Etap&#259; final&#259;</label>
                                    <button class="btn btn-outline btn-sm">Salveaz&#259;</button>
                                </div>
                            </form>
                            <dialog x-ref="deleteStageDialog" class="modal" aria-labelledby="delete-stage-{{ row.stage.pk }}-title" {% if row.delete_form.replacement_stage.errors %}open{% endif %}>
                                <div class="modal-box max-w-md rounded-box border border-error/40 bg-base-100 shadow-xl">
                                    <form method="dialog">
                                        <button class="btn btn-ghost btn-sm btn-circle absolute right-3 top-3" aria-label="&#206;nchide">x</button>
                                    </form>
                                    <form method="post" action="{% url 'tasks:stage_delete' row.stage.pk %}" class="space-y-4" hx-post="{% url 'tasks:stage_delete' row.stage.pk %}" hx-target="#board-settings-content" hx-swap="outerHTML">
                                        {% csrf_token %}
                                        <div>
                                            <h3 id="delete-stage-{{ row.stage.pk }}-title" class="text-base font-semibold text-error">&#536;terge etapa {{ row.stage.name }}</h3>
                                            <p class="mt-2 text-sm text-muted">Task-urile din aceast&#259; etap&#259; vor fi mutate &#238;n etapa aleas&#259; mai jos.</p>
                                        </div>
                                        <fieldset class="fieldset">
                                            <label class="fieldset-legend" for="{{ row.delete_form.replacement_stage.id_for_label }}">Mut&#259; task-urile &#238;n</label>
                                            {{ row.delete_form.replacement_stage }}
                                            {% if row.delete_form.replacement_stage.errors %}<p class="label whitespace-normal text-xs text-error" role="alert">{{ row.delete_form.replacement_stage.errors|join:", " }}</p>{% endif %}
                                        </fieldset>
                                        <div class="modal-action">
                                            <button type="button" class="btn btn-ghost btn-sm" x-on:click="$refs.deleteStageDialog.close()">Anuleaz&#259;</button>
                                            <button class="btn btn-error btn-sm">&#536;terge etapa</button>
                                        </div>
                                    </form>
                                </div>
                                <form method="dialog" class="modal-backdrop"><button>&#206;nchide</button></form>
                            </dialog>
                        </article>
                    {% endfor %}
                </div>
            </div>
        </div>

        <form method="post" action="{% url 'tasks:stage_create' board.pk %}" class="m-5 border border-dashed border-base-300 bg-base-200/30 p-3" hx-post="{% url 'tasks:stage_create' board.pk %}" hx-target="#board-settings-content" hx-swap="outerHTML">
            {% csrf_token %}
            <div class="grid items-end gap-3 md:grid-cols-[1.4fr_1fr_auto_auto]">
                <fieldset class="fieldset">
                    <label class="fieldset-legend" for="{{ stage_form.name.id_for_label }}">Adaug&#259; etap&#259;</label>
                    {{ stage_form.name }}
                    {% if stage_form.name.errors %}<p class="label whitespace-normal text-xs text-error" role="alert">{{ stage_form.name.errors|join:", " }}</p>{% endif %}
                </fieldset>
                <fieldset class="fieldset">
                    <label class="fieldset-legend" for="{{ stage_form.tone.id_for_label }}">Ton semantic</label>
                    {{ stage_form.tone }}
                    {% if stage_form.tone.errors %}<p class="label whitespace-normal text-xs text-error" role="alert">{{ stage_form.tone.errors|join:", " }}</p>{% endif %}
                </fieldset>
                <label class="flex h-8 items-center gap-2 text-sm">{{ stage_form.is_terminal }} Etap&#259; final&#259;</label>
                <button class="btn btn-outline btn-sm">Adaug&#259;</button>
            </div>
        </form>
    </section>

    {% if archived_tasks %}
        <section class="border border-base-300 bg-base-100 p-5">
            <h2 class="font-semibold">Task-uri arhivate</h2>
            <div class="mt-3 divide-y divide-base-300">
                {% for task in archived_tasks %}
                    <div class="flex items-center justify-between gap-3 py-3">
                        <span class="text-sm">{{ task.title }}</span>
                        <form method="post" action="{% url 'tasks:task_archive' task.pk %}" hx-post="{% url 'tasks:task_archive' task.pk %}" hx-target="#board-settings-content" hx-swap="outerHTML">
                            {% csrf_token %}
                            <input type="hidden" name="archived" value="0">
                            <input type="hidden" name="next" value="{% url 'tasks:board_settings' board.pk %}">
                            <button class="btn btn-ghost btn-xs text-success">Restaureaz&#259;</button>
                        </form>
                    </div>
                {% endfor %}
            </div>
        </section>
    {% endif %}
</section>
```

## `apps/tasks/templates/tasks/includes/board_task_list.html`

Size: 3.5 KB

```html
<div id="task-list-results" class="space-y-3">
    <div class="overflow-x-auto border border-base-300">
        <table class="table table-sm min-w-[900px]">
            <thead><tr><th>Task</th><th>Etapă</th><th>Prioritate</th><th>Responsabil</th><th>Termen</th><th>Timp rămas</th><th class="text-right">Acțiuni</th></tr></thead>
            <tbody>
            {% for task in page %}
                <tr class="hover:bg-base-200/60">
                    <td><p class="font-semibold">{{ task.title }}</p>{% if task.origin_url %}<a href="{{ task.origin_url }}" class="text-xs text-primary">{{ task.origin_label|default:'Deschide sursa' }} ↗</a>{% endif %}</td>
                    <td><span class="badge badge-outline badge-sm">{{ task.stage.name }}</span></td>
                    <td>{{ task.get_priority_display }}</td>
                    <td>{{ task.assignee.get_full_name|default:task.assignee.username }}</td>
                    <td class="whitespace-nowrap">{{ task.due_at|date:'d.m.Y H:i' }}</td>
                    <td>{% include "tasks/includes/timer.html" %}</td>
                    <td>
                        <div class="flex justify-end gap-1">
                            {% if task.can_edit %}
                                <a href="{% url 'tasks:task_edit' task.pk %}" class="btn btn-square btn-ghost btn-xs text-primary hover:bg-primary/10" aria-label="Editează task-ul" title="Editează task-ul">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="size-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="m16.862 3.487 3.651 3.651M4.5 19.5l4.228-.845a2 2 0 0 0 1.024-.547L20.513 7.347a1.75 1.75 0 0 0 0-2.474l-1.386-1.386a1.75 1.75 0 0 0-2.474 0L5.892 14.248a2 2 0 0 0-.547 1.024L4.5 19.5Z" /></svg>
                                </a>
                            {% endif %}
                        </div>
                    </td>
                </tr>
            {% empty %}
                <tr><td colspan="7" class="py-12 text-center text-muted">Nu există task-uri.</td></tr>
            {% endfor %}
            </tbody>
        </table>
    </div>
    {% if page.paginator.num_pages > 1 %}
    <div class="flex items-center justify-between text-sm text-muted">
        <span>Pagina {{ page.number }} din {{ page.paginator.num_pages }}</span>
        <div class="join">
            {% if page.has_previous %}
                <a
                    class="btn btn-sm join-item"
                    href="?{% if filters.urlencode %}{{ filters.urlencode }}&{% endif %}page={{ page.previous_page_number }}"
                    hx-get="?{% if filters.urlencode %}{{ filters.urlencode }}&{% endif %}page={{ page.previous_page_number }}"
                    hx-target="#task-list-results"
                    hx-swap="outerHTML"
                    hx-push-url="true"
                >‹</a>
            {% endif %}
            {% if page.has_next %}
                <a
                    class="btn btn-sm join-item"
                    href="?{% if filters.urlencode %}{{ filters.urlencode }}&{% endif %}page={{ page.next_page_number }}"
                    hx-get="?{% if filters.urlencode %}{{ filters.urlencode }}&{% endif %}page={{ page.next_page_number }}"
                    hx-target="#task-list-results"
                    hx-swap="outerHTML"
                    hx-push-url="true"
                >›</a>
            {% endif %}
        </div>
    </div>
    {% endif %}
</div>
```

## `apps/tasks/templates/tasks/includes/form_fields.html`

Size: 775 B

```html
{% if form.non_field_errors %}
    <div class="alert alert-error py-2 text-sm" role="alert">{{ form.non_field_errors|join:", " }}</div>
{% endif %}
{% for field in form %}
    <fieldset class="fieldset min-w-0 {% if field.name == 'description' %}sm:col-span-2{% endif %}">
        <label class="fieldset-legend" for="{{ field.id_for_label }}">{{ field.label }}{% if field.field.required %}<span class="text-error" aria-hidden="true"> *</span>{% endif %}</label>
        {{ field }}
        {% if field.help_text %}<p class="label whitespace-normal text-xs text-muted">{{ field.help_text }}</p>{% endif %}
        {% if field.errors %}<p class="label whitespace-normal text-xs text-error" role="alert">{{ field.errors|join:", " }}</p>{% endif %}
    </fieldset>
{% endfor %}

```

## `apps/tasks/templates/tasks/includes/hub_task_list.html`

Size: 4.8 KB

```html
<div id="task-list-results" class="space-y-3">
    <div class="overflow-x-auto border border-base-300 bg-base-100">
        <table class="table table-sm min-w-[980px]">
            <thead><tr><th>Task</th><th>Board</th><th>Etapă</th><th>Prioritate</th><th>Responsabil</th><th>Termen</th><th>Timp rămas</th><th class="text-right">Acțiuni</th></tr></thead>
            <tbody>
            {% for task in page %}
                <tr class="hover:bg-base-200/60">
                    <td><div class="max-w-64"><p class="font-semibold text-base-content">{{ task.title }}</p>{% if task.origin_url %}<a href="{{ task.origin_url }}" class="text-xs text-primary hover:underline">{{ task.origin_label|default:"Deschide sursa" }} ↗</a>{% endif %}</div></td>
                    <td><a href="{% url 'tasks:board_kanban' task.board_id %}" class="font-medium text-primary hover:underline">{{ task.board.name }}</a></td>
                    <td><span class="badge badge-outline badge-sm">{{ task.stage.name }}</span></td>
                    <td>{{ task.get_priority_display }}</td>
                    <td>{{ task.assignee.get_full_name|default:task.assignee.username }}</td>
                    <td class="whitespace-nowrap">{{ task.due_at|date:"d.m.Y H:i" }}</td>
                    <td class="whitespace-nowrap">{% include "tasks/includes/timer.html" %}</td>
                    <td>
                        <div class="flex justify-end gap-1">
                            {% if task.can_edit %}
                                <a
                                    href="{% url 'tasks:task_edit' task.pk %}"
                                    class="btn btn-square btn-ghost btn-xs text-primary hover:bg-primary/10"
                                    aria-label="Editează task-ul"
                                    title="Editează task-ul"
                                >
                                    <svg xmlns="http://www.w3.org/2000/svg" class="size-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="m16.862 3.487 3.651 3.651M4.5 19.5l4.228-.845a2 2 0 0 0 1.024-.547L20.513 7.347a1.75 1.75 0 0 0 0-2.474l-1.386-1.386a1.75 1.75 0 0 0-2.474 0L5.892 14.248a2 2 0 0 0-.547 1.024L4.5 19.5Z" />
                                    </svg>
                                </a>
                            {% endif %}
                            <a
                                href="{% url 'tasks:board_kanban' task.board_id %}"
                                class="btn btn-square btn-ghost btn-xs text-primary hover:bg-primary/10"
                                aria-label="Deschide board-ul în vizualizarea Kanban"
                                title="Deschide board-ul în vizualizarea Kanban"
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" class="size-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M4.75 5.25h5.5v13.5h-5.5V5.25Zm9 0h5.5v8.5h-5.5v-8.5Z" />
                                </svg>
                            </a>
                        </div>
                    </td>
                </tr>
            {% empty %}
                <tr><td colspan="8" class="py-12 text-center text-muted">Nu există task-uri pentru filtrele selectate.</td></tr>
            {% endfor %}
            </tbody>
        </table>
    </div>
    {% if page.paginator.num_pages > 1 %}
    <div class="flex items-center justify-between text-sm text-muted">
        <span>Pagina {{ page.number }} din {{ page.paginator.num_pages }}</span>
        <div class="join">
            {% if page.has_previous %}
                <a
                    class="btn btn-sm join-item"
                    href="?{% if filters.urlencode %}{{ filters.urlencode }}&{% endif %}page={{ page.previous_page_number }}"
                    hx-get="?{% if filters.urlencode %}{{ filters.urlencode }}&{% endif %}page={{ page.previous_page_number }}"
                    hx-target="#task-list-results"
                    hx-swap="outerHTML"
                    hx-push-url="true"
                >‹</a>
            {% endif %}
            {% if page.has_next %}
                <a
                    class="btn btn-sm join-item"
                    href="?{% if filters.urlencode %}{{ filters.urlencode }}&{% endif %}page={{ page.next_page_number }}"
                    hx-get="?{% if filters.urlencode %}{{ filters.urlencode }}&{% endif %}page={{ page.next_page_number }}"
                    hx-target="#task-list-results"
                    hx-swap="outerHTML"
                    hx-push-url="true"
                >›</a>
            {% endif %}
        </div>
    </div>
    {% endif %}
</div>
```

## `apps/tasks/templates/tasks/includes/kanban_board.html`

Size: 2.1 KB

```html
<div id="kanban-board-region" class="flex min-h-[34rem] gap-3 overflow-x-auto border-y border-base-300 bg-base-100 py-3" data-kanban-board{% if kanban_board_oob %} hx-swap-oob="true"{% endif %}>
    {% for stage in stages %}
        <section class="flex w-80 shrink-0 flex-col border border-base-300 bg-base-200/60 transition-colors {% if stage.tone == 'error' %}border-t-4 border-t-error{% elif stage.tone == 'success' %}border-t-4 border-t-success{% elif stage.tone == 'warning' %}border-t-4 border-t-warning{% elif stage.tone == 'info' %}border-t-4 border-t-primary{% else %}border-t-4 border-t-base-300{% endif %}" data-stage-column data-stage-id="{{ stage.pk }}">
            <header class="border-b border-base-300 bg-base-100 px-3 py-3">
                <div class="flex items-start justify-between gap-3">
                    <div class="min-w-0">
                        <h2 class="truncate text-sm font-semibold text-base-content">{{ stage.name }}</h2>
                        <p class="mt-0.5 text-[11px] font-medium uppercase tracking-wide text-muted">{% if stage.is_terminal %}Etapă finală{% else %}Etapă activă{% endif %}</p>
                    </div>
                    <span class="badge badge-sm border-base-300 bg-base-200 font-semibold" data-stage-count>{{ stage.visible_tasks|length }}</span>
                </div>
            </header>
            <div class="flex min-h-80 flex-1 flex-col gap-2 border border-transparent p-2 transition-colors" data-stage-cards data-stage-drop-zone>
                {% include "tasks/includes/kanban_empty_stage.html" %}
                {% for task in stage.visible_tasks %}
                    {% include "tasks/includes/kanban_card.html" %}
                {% endfor %}
                <button type="button" class="mt-auto min-h-10 border border-dashed border-base-300 bg-base-100 px-3 text-sm font-medium text-muted transition-colors hover:border-primary hover:text-primary focus-visible:outline focus-visible:outline-2 focus-visible:outline-primary" data-open-task-dialog>+ Adaugă task</button>
            </div>
        </section>
    {% endfor %}
</div>
```

## `apps/tasks/templates/tasks/includes/kanban_board_response.html`

Size: 101 B

```html
{% include "tasks/includes/kanban_board.html" %}
{% include "tasks/includes/kanban_messages.html" %}
```

## `apps/tasks/templates/tasks/includes/kanban_card.html`

Size: 4.9 KB

```html
<article class="group border border-base-300 bg-base-100 p-3 transition-colors focus-within:border-primary focus-within:outline focus-within:outline-2 focus-within:outline-primary {% if task.can_move %}cursor-grab hover:border-primary{% endif %} {% if task.priority == 'high' %}border-l-4 border-l-error{% elif task.priority == 'medium' %}border-l-4 border-l-warning{% else %}border-l-4 border-l-success{% endif %}" data-task-card data-task-id="{{ task.pk }}" data-task-version="{{ task.version }}" data-move-url="{% url 'tasks:task_move' task.pk %}" {% if task.can_move %}draggable="true" tabindex="0"{% endif %}>
    <div class="flex items-start justify-between gap-2">
        <div class="min-w-0">
            <div class="flex items-start gap-2">
                {% if task.can_move %}<span class="mt-0.5 cursor-grab text-muted group-hover:text-primary" aria-hidden="true" data-card-grip>::</span>{% endif %}
                <h3 class="text-sm font-semibold leading-5 text-base-content">{{ task.title }}</h3>
            </div>
        </div>
        {% if task.origin_url %}<a href="{{ task.origin_url }}" class="shrink-0 text-primary hover:underline focus-visible:outline focus-visible:outline-2 focus-visible:outline-primary" title="{{ task.origin_label|default:'Deschide sursa' }}">&#8599;</a>{% endif %}
    </div>
    {% if task.description %}<p class="mt-1 line-clamp-2 text-xs leading-5 text-muted">{{ task.description }}</p>{% endif %}
    <div class="mt-3 flex items-center gap-2 border-t border-base-300 pt-2 text-xs">
        <span class="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-base-200 font-bold text-base-content">{{ task.assignee.username|slice:':2'|upper }}</span>
        <span class="min-w-0 truncate font-medium text-base-content">{{ task.assignee.get_full_name|default:task.assignee.username }}</span>
    </div>
    <div class="mt-2 flex flex-wrap items-center gap-2 text-xs">
        <span class="badge badge-xs border-base-300 bg-base-100 font-semibold {% if task.priority == 'high' %}text-error{% elif task.priority == 'medium' %}text-warning{% else %}text-success{% endif %}">&#9873; {{ task.get_priority_display }}</span>
        {% include "tasks/includes/timer.html" %}
    </div>
    <div class="mt-3 flex items-center justify-between gap-2 border-t border-base-300 pt-2">
        <div class="flex items-center gap-1">
            {% if task.can_edit %}
                <a href="{% url 'tasks:task_edit' task.pk %}" class="btn btn-ghost btn-xs focus-visible:outline focus-visible:outline-2 focus-visible:outline-primary">Editeaz&#259;</a>
                {% url 'tasks:task_archive' task.pk as task_archive_url %}
                <form method="post" action="{{ task_archive_url }}{% if kanban_query %}?{{ kanban_query }}{% endif %}" hx-post="{{ task_archive_url }}{% if kanban_query %}?{{ kanban_query }}{% endif %}" hx-target="#kanban-board-region" hx-swap="outerHTML">
                    {% csrf_token %}
                    <input type="hidden" name="_kanban" value="1">
                    <input type="hidden" name="archived" value="1">
                    <input type="hidden" name="next" value="{{ kanban_path }}">
                    <button class="btn btn-outline btn-error btn-xs btn-square focus-visible:outline focus-visible:outline-2 focus-visible:outline-error" type="submit" aria-label="Arhivează task-ul {{ task.title }}" title="Arhivează task-ul" data-archive-action>
                        <svg aria-hidden="true" class="h-3.5 w-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M3 6h18"></path>
                            <path d="M8 6V4h8v2"></path>
                            <path d="M19 6l-1 14H6L5 6"></path>
                            <path d="M10 11v6"></path>
                            <path d="M14 11v6"></path>
                        </svg>
                    </button>
                </form>
            {% else %}
                <span></span>
            {% endif %}
        </div>
        {% if task.can_move %}
            <form method="post" action="{% url 'tasks:task_move' task.pk %}" class="flex items-center gap-1" data-stage-fallback-form>
                {% csrf_token %}
                <input type="hidden" name="target_index" value="99999">
                <input type="hidden" name="expected_version" value="{{ task.version }}">
                <label class="sr-only" for="stage-{{ task.pk }}">Mută în etapa</label>
                <select id="stage-{{ task.pk }}" name="stage" class="select select-bordered select-xs max-w-28 focus-visible:outline focus-visible:outline-2 focus-visible:outline-primary" onchange="this.form.submit()">
                    {% for target in stages %}<option value="{{ target.pk }}"{% if target.pk == task.stage_id %} selected{% endif %}>{{ target.name }}</option>{% endfor %}
                </select>
            </form>
        {% endif %}
    </div>
</article>
```

## `apps/tasks/templates/tasks/includes/kanban_create_response.html`

Size: 161 B

```html
{% include "tasks/includes/task_create_dialog_body.html" %}
{% include "tasks/includes/kanban_messages.html" %}
{% include "tasks/includes/kanban_board.html" %}
```

## `apps/tasks/templates/tasks/includes/kanban_empty_stage.html`

Size: 368 B

```html
<div class="{% if stage.visible_tasks %}hidden {% endif %}flex min-h-28 flex-col items-center justify-center border border-dashed border-base-300 bg-base-100 px-3 py-5 text-center text-xs text-muted" data-stage-empty>
    <span class="font-semibold text-base-content">Etapă liberă</span>
    <span class="mt-1">Trage un task aici sau adaugă unul nou.</span>
</div>
```

## `apps/tasks/templates/tasks/includes/kanban_messages.html`

Size: 132 B

```html
<div id="task-messages"{% if messages_oob %} hx-swap-oob="true"{% endif %}>
    {% include "tasks/includes/messages.html" %}
</div>
```

## `apps/tasks/templates/tasks/includes/messages.html`

Size: 316 B

```html
{% if messages %}
<div class="space-y-2" aria-live="polite">
    {% for message in messages %}
        <div class="alert py-2 text-sm {% if message.tags == 'error' %}alert-error{% elif message.tags == 'success' %}alert-success{% else %}alert-info{% endif %}">{{ message }}</div>
    {% endfor %}
</div>
{% endif %}

```

## `apps/tasks/templates/tasks/includes/task_create_dialog_body.html`

Size: 1.1 KB

```html
<div id="task-create-dialog-body">
    <form method="dialog"><button class="btn btn-ghost btn-sm btn-circle absolute right-3 top-3" aria-label="Închide">×</button></form>
    <h2 class="text-xl font-bold text-base-content">Task nou</h2>
    <p class="mt-1 text-sm text-muted">Adaugă un task în {{ board.name }}.</p>
    {% url 'tasks:task_create' board.pk as task_create_url %}
    <form method="post" action="{{ task_create_url }}{% if kanban_query %}?{{ kanban_query }}{% endif %}" class="mt-5 space-y-4" hx-post="{{ task_create_url }}{% if kanban_query %}?{{ kanban_query }}{% endif %}" hx-target="#task-create-dialog-body" hx-swap="outerHTML">
        {% csrf_token %}
        <input type="hidden" name="_kanban" value="1">
        <div class="grid gap-x-4 sm:grid-cols-2">{% include "tasks/includes/form_fields.html" with form=task_form %}</div>
        <div class="flex justify-end gap-2">
            <button type="button" class="btn btn-ghost btn-sm" data-close-task-dialog>Anulează</button>
            <button class="btn btn-primary btn-sm">Creează task</button>
        </div>
    </form>
</div>
```

## `apps/tasks/templates/tasks/includes/task_form_panel.html`

Size: 971 B

```html
<form
    id="task-form-panel"
    method="post"
    class="space-y-5 border border-base-300 bg-base-100 p-5"
    {% if not task %}
        hx-post="{% url 'tasks:task_create' board.pk %}"
        hx-target="#task-form-panel"
        hx-swap="outerHTML"
    {% endif %}
>
    {% csrf_token %}
    <div class="grid gap-x-4 sm:grid-cols-2">
        {% include "tasks/includes/form_fields.html" %}
    </div>
    <div class="flex flex-wrap justify-between gap-2">
        <div>
            {% if task %}
                <button type="submit" formaction="{% url 'tasks:task_archive' task.pk %}" name="archived" value="1" class="btn btn-outline btn-error btn-sm">Arhiveaz&#259;</button>
            {% endif %}
        </div>
        <div class="flex gap-2">
            <a href="{% url 'tasks:board_kanban' board.pk %}" class="btn btn-ghost btn-sm">Anuleaz&#259;</a>
            <button class="btn btn-primary btn-sm">Salveaz&#259;</button>
        </div>
    </div>
</form>
```

## `apps/tasks/templates/tasks/includes/timer.html`

Size: 573 B

```html
<span
    class="inline-flex items-center gap-1.5 rounded-field border border-base-300 px-2 py-1 text-xs font-semibold tabular-nums"
    data-task-timer
    data-start-at="{% if task.start_at %}{{ task.start_at|date:'c' }}{% else %}{{ task.created_at|date:'c' }}{% endif %}"
    data-due-at="{{ task.due_at|date:'c' }}"
    data-completed-at="{% if task.completed_at %}{{ task.completed_at|date:'c' }}{% endif %}"
>
    <span aria-hidden="true">◷</span>
    <span data-timer-label>{% if task.completed_at %}Finalizat{% else %}Se calculează…{% endif %}</span>
</span>

```

## `apps/tasks/templates/tasks/task_form.html`

Size: 588 B

```html
{% extends "layouts/base.html" %}
{% block title %}{% if task %}Editeaz&#259; {{ task.title }}{% else %}Task nou{% endif %} | Task-uri{% endblock %}
{% block content %}
<section class="mx-auto max-w-2xl space-y-5">
    <div>
        <p class="text-xs text-muted"><a href="{% url 'tasks:board_kanban' board.pk %}" class="hover:text-primary">{{ board.name }}</a> / Task</p>
        <h1 class="ops-title mt-1 text-2xl font-bold">{% if task %}Editeaz&#259; task-ul{% else %}Task nou{% endif %}</h1>
    </div>
    {% include "tasks/includes/task_form_panel.html" %}
</section>
{% endblock %}
```

## `apps/tasks/tests.py`

Size: 24.4 KB

```python
from datetime import timedelta
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import BoardMembership, Task, TaskStage
from .selectors import visible_board_tasks
from .services import (
    TaskOrigin,
    add_board_member,
    create_board,
    create_stage,
    create_task,
    delete_stage,
    move_task,
    remove_board_member,
    set_task_archived,
    update_stage,
)


class TasksAppTests(TestCase):
    def setUp(self):
        users = get_user_model().objects
        self.owner = users.create_user(username="owner", password="test-password", first_name="Oana", last_name="Pop")
        self.assignee = users.create_user(username="assignee", password="test-password", first_name="Ana", last_name="Ionescu")
        self.member = users.create_user(username="member", password="test-password")
        self.outsider = users.create_user(username="outsider", password="test-password")
        self.staff = users.create_user(username="staff", password="test-password", is_staff=True)
        self.board = create_board(actor=self.owner, name="Operațiuni interne")
        add_board_member(actor=self.owner, board=self.board, user=self.assignee)
        add_board_member(actor=self.owner, board=self.board, user=self.member)
        self.todo = self.board.stages.get(name="De făcut")
        self.doing = self.board.stages.get(name="În lucru")
        self.done = self.board.stages.get(name="Finalizat")
        self.task = create_task(
            actor=self.owner,
            board=self.board,
            assignee=self.assignee,
            title="Verifică documentele",
            description="Control operațional",
            priority=Task.Priority.HIGH,
            due_at=timezone.now() + timedelta(days=2),
        )
        self.client.force_login(self.owner)

    def test_anonymous_user_is_redirected(self):
        self.client.logout()
        response = self.client.get(reverse("tasks:index"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("login")))

    def test_sidebar_and_hub_are_integrated(self):
        response = self.client.get(reverse("tasks:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Task-urile mele")
        self.assertContains(response, 'aria-current="page"')
        self.assertContains(response, "Verifică documentele")

    def test_board_creation_seeds_owner_membership_and_stages(self):
        board = create_board(actor=self.assignee, name="Board personal")
        self.assertTrue(BoardMembership.objects.filter(board=board, user=self.assignee).exists())
        self.assertEqual(
            list(board.stages.values_list("name", flat=True)),
            ["De făcut", "În lucru", "Blocat", "Finalizat"],
        )
        self.assertEqual(board.stages.filter(is_terminal=True).count(), 1)

    def test_assignment_must_target_active_member(self):
        with self.assertRaises(ValidationError):
            create_task(
                actor=self.owner,
                board=self.board,
                assignee=self.outsider,
                title="Task invalid",
                due_at=timezone.now() + timedelta(days=1),
            )

    def test_due_time_must_follow_effective_start(self):
        start = timezone.now() + timedelta(days=2)
        with self.assertRaises(ValidationError):
            create_task(
                actor=self.owner,
                board=self.board,
                assignee=self.assignee,
                title="Termen invalid",
                start_at=start,
                due_at=start - timedelta(hours=1),
            )

    def test_create_task_post_uses_current_time_when_start_is_blank(self):
        due_at = timezone.localtime(timezone.now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M")
        response = self.client.post(
            reverse("tasks:task_create", args=[self.board.pk]),
            {
                "title": "Task creat din formular",
                "description": "",
                "assignee": self.assignee.pk,
                "stage": self.todo.pk,
                "priority": Task.Priority.MEDIUM,
                "start_at": "",
                "due_at": due_at,
            },
        )
        self.assertRedirects(response, reverse("tasks:board_kanban", args=[self.board.pk]))
        self.assertTrue(Task.objects.filter(board=self.board, title="Task creat din formular").exists())

    def test_safe_origin_metadata_is_persisted_and_external_url_rejected(self):
        linked = create_task(
            actor=self.owner,
            board=self.board,
            assignee=self.assignee,
            title="Task cu sursă",
            due_at=timezone.now() + timedelta(days=1),
            origin=TaskOrigin(app="diplome", type="template", object_id="1", label="Template", url="/diplome/templates/1/"),
        )
        self.assertEqual(linked.origin_app, "diplome")
        with self.assertRaises(ValidationError):
            create_task(
                actor=self.owner,
                board=self.board,
                assignee=self.assignee,
                title="Sursă externă",
                due_at=timezone.now() + timedelta(days=1),
                origin=TaskOrigin(app="x", type="x", object_id="1", url="https://example.com"),
            )

    def test_member_sees_received_task_but_not_unrelated_task(self):
        unrelated = create_task(
            actor=self.owner,
            board=self.board,
            assignee=self.member,
            title="Task pentru alt membru",
            due_at=timezone.now() + timedelta(days=1),
        )
        visible_ids = set(visible_board_tasks(user=self.assignee, board=self.board).values_list("pk", flat=True))
        self.assertIn(self.task.pk, visible_ids)
        self.assertNotIn(unrelated.pk, visible_ids)

    def test_board_owner_and_staff_see_every_board_task(self):
        other = create_task(
            actor=self.member,
            board=self.board,
            assignee=self.member,
            title="Task creat de membru",
            due_at=timezone.now() + timedelta(days=1),
        )
        self.assertTrue(visible_board_tasks(user=self.owner, board=self.board).filter(pk=other.pk).exists())
        self.assertTrue(visible_board_tasks(user=self.staff, board=self.board).filter(pk=other.pk).exists())

    def test_outsider_cannot_open_board_or_task(self):
        self.client.force_login(self.outsider)
        self.assertEqual(self.client.get(reverse("tasks:board_kanban", args=[self.board.pk])).status_code, 404)
        self.assertEqual(self.client.get(reverse("tasks:task_edit", args=[self.task.pk])).status_code, 404)

    def test_assignee_can_move_but_cannot_edit(self):
        self.client.force_login(self.assignee)
        self.assertEqual(self.client.get(reverse("tasks:task_edit", args=[self.task.pk])).status_code, 404)
        response = self.client.post(
            reverse("tasks:task_move", args=[self.task.pk]),
            {"stage": self.doing.pk, "target_index": 0, "expected_version": self.task.version},
            HTTP_ACCEPT="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(self.task.stage, self.doing)

    def test_move_rejects_stale_version(self):
        response = self.client.post(
            reverse("tasks:task_move", args=[self.task.pk]),
            {"stage": self.doing.pk, "target_index": 0, "expected_version": self.task.version + 1},
            HTTP_ACCEPT="application/json",
        )
        self.assertEqual(response.status_code, 409)
        self.task.refresh_from_db()
        self.assertEqual(self.task.stage, self.todo)

    def test_terminal_move_completes_and_active_move_reopens(self):
        task = move_task(
            actor=self.assignee,
            task=self.task,
            target_stage=self.done,
            target_index=0,
            expected_version=self.task.version,
        )
        self.assertIsNotNone(task.completed_at)
        task = move_task(
            actor=self.assignee,
            task=task,
            target_stage=self.doing,
            target_index=0,
            expected_version=task.version,
        )
        self.assertIsNone(task.completed_at)

    def test_move_json_reports_completed_state_for_timer_updates(self):
        response = self.client.post(
            reverse("tasks:task_move", args=[self.task.pk]),
            {"stage": self.done.pk, "target_index": 0, "expected_version": self.task.version},
            HTTP_ACCEPT="application/json",
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIsNotNone(payload["task"]["completedAt"])

        self.task.refresh_from_db()
        response = self.client.post(
            reverse("tasks:task_move", args=[self.task.pk]),
            {"stage": self.doing.pk, "target_index": 0, "expected_version": self.task.version},
            HTTP_ACCEPT="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.json()["task"]["completedAt"])

    def test_manual_order_is_persisted(self):
        second = create_task(
            actor=self.owner,
            board=self.board,
            assignee=self.assignee,
            title="Al doilea",
            due_at=timezone.now() + timedelta(days=3),
        )
        moved = move_task(
            actor=self.owner,
            task=second,
            target_stage=self.todo,
            target_index=0,
            expected_version=second.version,
        )
        self.task.refresh_from_db()
        self.assertEqual(moved.rank, 0)
        self.assertEqual(self.task.rank, 1)

    def test_member_removal_is_blocked_until_active_tasks_are_reassigned(self):
        with self.assertRaises(ValidationError):
            remove_board_member(actor=self.owner, board=self.board, user=self.assignee)
        self.task.stage = self.done
        self.task.completed_at = timezone.now()
        self.task.save()
        remove_board_member(actor=self.owner, board=self.board, user=self.assignee)
        self.assertFalse(BoardMembership.objects.filter(board=self.board, user=self.assignee).exists())

    def test_stage_deletion_moves_tasks_to_replacement(self):
        blocked = self.board.stages.get(name="Blocat")
        self.task.stage = blocked
        self.task.save()
        delete_stage(actor=self.owner, stage=blocked, replacement=self.doing)
        self.task.refresh_from_db()
        self.assertEqual(self.task.stage, self.doing)
        self.assertFalse(self.board.stages.filter(pk=blocked.pk).exists())

    def test_last_terminal_stage_cannot_be_made_active(self):
        with self.assertRaises(ValidationError):
            update_stage(
                actor=self.owner,
                stage=self.done,
                name=self.done.name,
                tone=self.done.tone,
                is_terminal=False,
            )

    def test_additional_terminal_stage_is_allowed(self):
        stage = create_stage(actor=self.owner, board=self.board, name="Anulat", tone=TaskStage.Tone.NEUTRAL, is_terminal=True)
        self.assertTrue(stage.is_terminal)

    def test_archive_and_restore_task(self):
        set_task_archived(actor=self.owner, task=self.task, archived=True)
        self.assertFalse(visible_board_tasks(user=self.owner, board=self.board).filter(pk=self.task.pk).exists())
        set_task_archived(actor=self.owner, task=self.task, archived=False)
        self.assertTrue(visible_board_tasks(user=self.owner, board=self.board).filter(pk=self.task.pk).exists())

    def test_board_state_returns_only_visible_tasks(self):
        hidden = create_task(
            actor=self.owner,
            board=self.board,
            assignee=self.member,
            title="Ascuns pentru responsabil",
            due_at=timezone.now() + timedelta(days=1),
        )
        self.client.force_login(self.assignee)
        response = self.client.get(reverse("tasks:board_state", args=[self.board.pk]))
        self.assertEqual(response.status_code, 200)
        returned = {item["id"] for item in response.json()["tasks"]}
        self.assertIn(str(self.task.pk), returned)
        self.assertNotIn(str(hidden.pk), returned)

    def test_hub_filters_by_relation_and_priority(self):
        response = self.client.get(reverse("tasks:index"), {"relation": "assigned", "priority": Task.Priority.HIGH})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Verifică documentele")
        self.client.force_login(self.assignee)
        response = self.client.get(reverse("tasks:index"), {"relation": "assigned", "priority": Task.Priority.HIGH})
        self.assertContains(response, "Verifică documentele")

    def test_hub_htmx_filter_returns_task_list_partial(self):
        response = self.client.get(
            reverse("tasks:index"),
            {"relation": "created", "priority": Task.Priority.HIGH},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="task-list-results"')
        self.assertContains(response, self.task.title)
        self.assertNotContains(response, "Task-urile mele")
        self.assertNotContains(response, "<form")

    def test_board_list_htmx_filter_returns_task_list_partial(self):
        low_priority_title = "Task low priority"
        create_task(
            actor=self.owner,
            board=self.board,
            assignee=self.owner,
            title=low_priority_title,
            priority=Task.Priority.LOW,
            due_at=timezone.now() + timedelta(days=1),
        )
        response = self.client.get(
            reverse("tasks:board_list", args=[self.board.pk]),
            {"priority": Task.Priority.HIGH},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="task-list-results"')
        self.assertContains(response, self.task.title)
        self.assertNotContains(response, low_priority_title)
        self.assertNotContains(response, self.board.name)
        self.assertNotContains(response, "<form")

    def test_board_create_htmx_invalid_returns_form_partial(self):
        response = self.client.post(
            reverse("tasks:board_create"),
            {"name": ""},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'id="board-form-panel"', status_code=400)
        self.assertNotContains(response, "Board nou", status_code=400)

    def test_task_create_htmx_success_uses_hx_redirect(self):
        due_at = timezone.localtime(timezone.now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M")
        response = self.client.post(
            reverse("tasks:task_create", args=[self.board.pk]),
            {
                "title": "Task creat prin HTMX",
                "description": "",
                "assignee": self.assignee.pk,
                "stage": self.todo.pk,
                "priority": Task.Priority.MEDIUM,
                "start_at": "",
                "due_at": due_at,
            },
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.headers["HX-Redirect"], reverse("tasks:board_kanban", args=[self.board.pk]))
        self.assertTrue(Task.objects.filter(board=self.board, title="Task creat prin HTMX").exists())

    def test_task_create_htmx_invalid_returns_form_partial(self):
        response = self.client.post(
            reverse("tasks:task_create", args=[self.board.pk]),
            {
                "title": "",
                "description": "",
                "assignee": self.assignee.pk,
                "stage": self.todo.pk,
                "priority": Task.Priority.MEDIUM,
                "start_at": "",
                "due_at": "",
            },
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'id="task-form-panel"', status_code=400)
        self.assertNotContains(response, "Task nou", status_code=400)

    def test_kanban_task_create_htmx_success_refreshes_board_and_messages(self):
        due_at = timezone.localtime(timezone.now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M")
        title = "Task creat din Kanban HTMX"
        response = self.client.post(
            reverse("tasks:task_create", args=[self.board.pk]),
            {
                "_kanban": "1",
                "title": title,
                "description": "",
                "assignee": self.assignee.pk,
                "stage": self.todo.pk,
                "priority": Task.Priority.MEDIUM,
                "start_at": "",
                "due_at": due_at,
            },
            HTTP_HX_REQUEST="true",
            HTTP_HX_TARGET="task-create-dialog-body",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["HX-Trigger"], "taskKanban:taskCreated")
        self.assertTrue(Task.objects.filter(board=self.board, title=title).exists())
        self.assertContains(response, 'id="task-create-dialog-body"')
        self.assertContains(response, 'id="task-messages" hx-swap-oob="true"')
        self.assertContains(response, 'id="kanban-board-region"')
        self.assertContains(response, 'hx-swap-oob="true"')
        self.assertContains(response, title)
        self.assertContains(response, "Task-ul a fost creat.")
        self.assertContains(response, "data-stage-column")
        self.assertContains(response, "data-stage-id")
        self.assertContains(response, "data-stage-drop-zone")
        self.assertContains(response, "data-stage-empty")
        self.assertContains(response, "data-task-card")
        self.assertContains(response, "data-task-id")
        self.assertContains(response, "data-task-version")
        self.assertContains(response, "data-move-url")
        self.assertContains(response, "data-card-grip")
        self.assertContains(response, "data-archive-action")
        self.assertContains(response, 'draggable="true"')
        self.assertContains(response, "data-stage-fallback-form")
        self.assertContains(response, "data-task-timer")
        self.assertNotContains(response, "<html")

    def test_kanban_task_create_htmx_invalid_stays_inside_dialog_body(self):
        response = self.client.post(
            reverse("tasks:task_create", args=[self.board.pk]),
            {
                "_kanban": "1",
                "title": "",
                "description": "",
                "assignee": self.assignee.pk,
                "stage": self.todo.pk,
                "priority": Task.Priority.MEDIUM,
                "start_at": "",
                "due_at": "",
            },
            HTTP_HX_REQUEST="true",
            HTTP_HX_TARGET="task-create-dialog-body",
        )
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'id="task-create-dialog-body"', status_code=400)
        self.assertContains(response, 'role="alert"', status_code=400)
        self.assertNotContains(response, 'id="kanban-board-region"', status_code=400)
        self.assertNotContains(response, "<html", status_code=400)

    def test_kanban_task_archive_htmx_refreshes_board_and_messages(self):
        response = self.client.post(
            reverse("tasks:task_archive", args=[self.task.pk]),
            {
                "_kanban": "1",
                "archived": "1",
                "next": reverse("tasks:board_kanban", args=[self.board.pk]),
            },
            HTTP_HX_REQUEST="true",
            HTTP_HX_TARGET="kanban-board-region",
        )
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertIsNotNone(self.task.archived_at)
        self.assertContains(response, 'id="kanban-board-region"')
        self.assertContains(response, 'id="task-messages" hx-swap-oob="true"')
        self.assertContains(response, "Task arhivat.")
        self.assertContains(response, "data-stage-column")
        self.assertNotContains(response, self.task.title)
        self.assertNotContains(response, "<html")

    def test_task_archive_native_fallback_redirects_to_kanban(self):
        response = self.client.post(
            reverse("tasks:task_archive", args=[self.task.pk]),
            {"archived": "1", "next": reverse("tasks:board_kanban", args=[self.board.pk])},
        )
        self.assertRedirects(response, reverse("tasks:board_kanban", args=[self.board.pk]))
        self.task.refresh_from_db()
        self.assertIsNotNone(self.task.archived_at)

    def test_task_archive_permission_is_unchanged_for_non_editor(self):
        self.client.force_login(self.assignee)
        response = self.client.post(
            reverse("tasks:task_archive", args=[self.task.pk]),
            {"_kanban": "1", "archived": "1"},
            HTTP_HX_REQUEST="true",
            HTTP_HX_TARGET="kanban-board-region",
        )
        self.assertEqual(response.status_code, 404)
        self.task.refresh_from_db()
        self.assertIsNone(self.task.archived_at)

    def test_tasks_js_reinitializes_kanban_after_htmx_refreshes(self):
        script = (Path(__file__).resolve().parent / "static" / "tasks" / "tasks.js").read_text(encoding="utf-8")
        self.assertIn("htmx:afterSwap", script)
        self.assertIn("htmx:oobAfterSwap", script)
        self.assertIn("initDragDrop", script)
        self.assertIn("setDragContext(true)", script)
        self.assertIn("setDropState(container, true)", script)
        self.assertIn("data-stage-empty", script)
        self.assertIn("querySelectorAll(\"[data-task-timer]\")", script)
        self.assertIn("updateMovedCardTimer(card, payload.task)", script)
        self.assertIn("timer.dataset.completedAt = taskPayload.completedAt", script)
        self.assertIn("delete timer.dataset.completedAt", script)
        self.assertIn("knownSignature = null", script)
        self.assertIn("setInterval(pollState, 30000)", script)

    def test_kanban_renders_empty_drop_zones_and_destructive_actions_for_editor(self):
        response = self.client.get(reverse("tasks:board_kanban", args=[self.board.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "data-stage-drop-zone")
        self.assertContains(response, "data-stage-empty")
        self.assertContains(response, "data-card-grip")
        self.assertContains(response, "data-archive-action")
        self.assertContains(response, "btn-outline btn-error")
        self.assertContains(response, "data-stage-fallback-form")
        self.assertContains(response, 'name="expected_version"')
        self.assertContains(response, 'name="target_index"')

    def test_kanban_hides_archive_action_for_non_editor_but_keeps_move_fallback(self):
        self.client.force_login(self.assignee)
        response = self.client.get(reverse("tasks:board_kanban", args=[self.board.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.title)
        self.assertContains(response, "data-stage-fallback-form")
        self.assertContains(response, "data-card-grip")
        self.assertNotContains(response, "data-archive-action")

    def test_stage_create_htmx_refreshes_settings_section(self):
        response = self.client.post(
            reverse("tasks:stage_create", args=[self.board.pk]),
            {
                "new-stage-name": "Validare",
                "new-stage-tone": TaskStage.Tone.INFO,
            },
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="board-settings-content"')
        self.assertContains(response, "Validare")
        self.assertTrue(self.board.stages.filter(name="Validare").exists())
        self.assertNotContains(response, "<html")

    def test_kanban_filters_by_assignee_and_priority(self):
        create_task(
            actor=self.owner,
            board=self.board,
            assignee=self.owner,
            title="Task cu prioritate scăzută",
            priority=Task.Priority.LOW,
            due_at=timezone.now() + timedelta(days=1),
        )
        response = self.client.get(
            reverse("tasks:board_kanban", args=[self.board.pk]),
            {"assignee": self.assignee.pk, "priority": Task.Priority.HIGH},
        )
        self.assertContains(response, "Verifică documentele")
        self.assertNotContains(response, "Task cu prioritate scăzută")
```

## `apps/tasks/urls.py`

Size: 1.8 KB

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

## `apps/tasks/validators.py`

Size: 630 B

```python
from urllib.parse import urlsplit

from django.core.exceptions import ValidationError


def validate_origin_url(value: str) -> None:
    if not value:
        return
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc or not value.startswith("/") or value.startswith("//"):
        raise ValidationError("Linkul sursă trebuie să fie o cale internă sigură.")


def validate_stage_balance(*, terminal_count: int, non_terminal_count: int) -> None:
    if terminal_count < 1 or non_terminal_count < 1:
        raise ValidationError("Board-ul trebuie să păstreze cel puțin o etapă activă și una terminală.")

```

## `apps/tasks/views.py`

Size: 25.0 KB

```python
import hashlib
import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Q
from django.http import Http404, HttpResponse, JsonResponse
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


def _is_htmx(request) -> bool:
    return request.headers.get("HX-Request") == "true"


def _htmx_redirect(url: str) -> HttpResponse:
    response = HttpResponse(status=204)
    response["HX-Redirect"] = url
    return response


def _is_kanban_htmx(request) -> bool:
    return _is_htmx(request) and request.POST.get("_kanban") == "1"


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
    partial_template_name = "tasks/includes/hub_task_list.html"

    def get(self, request):
        boards = list(accessible_boards(user=request.user))
        queryset = _filtered_tasks(request, visible_tasks(user=request.user))
        paginator = Paginator(queryset, 25)
        page = paginator.get_page(request.GET.get("page"))
        _decorate_tasks(page.object_list, request.user)
        stage_options = TaskStage.objects.filter(board__in=boards).order_by("board__name", "position")
        template_name = self.partial_template_name if request.headers.get("HX-Request") == "true" else self.template_name
        return render(
            request,
            template_name,
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
    partial_template_name = "tasks/includes/board_form_panel.html"

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
                if _is_htmx(request):
                    return _htmx_redirect(reverse("tasks:board_kanban", kwargs={"board_id": board.pk}))
                return redirect("tasks:board_kanban", board_id=board.pk)
        template_name = self.partial_template_name if _is_htmx(request) else self.template_name
        return render(request, template_name, {"form": form}, status=400)


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
        "kanban_query": request.META.get("QUERY_STRING", ""),
        "kanban_path": request.get_full_path(),
    }


def _render_kanban_partial(request, board, *, template_name, task_form=None, status=200, **context_overrides):
    context = _board_context(request=request, board=board, task_form=task_form)
    context.update(context_overrides)
    return render(request, template_name, context, status=status)


class BoardKanbanView(LoginRequiredMixin, View):
    template_name = "tasks/board_kanban.html"

    def get(self, request, board_id):
        board = get_accessible_board(user=request.user, board_id=board_id)
        return render(request, self.template_name, _board_context(request=request, board=board))


class BoardListView(LoginRequiredMixin, View):
    template_name = "tasks/board_list.html"
    partial_template_name = "tasks/includes/board_task_list.html"

    def get(self, request, board_id):
        board = get_accessible_board(user=request.user, board_id=board_id)
        queryset = _filtered_tasks(request, visible_board_tasks(user=request.user, board=board))
        page = Paginator(queryset, 25).get_page(request.GET.get("page"))
        _decorate_tasks(page.object_list, request.user)
        context = _board_context(request=request, board=board)
        context.update({"page": page, "priority_choices": Task.Priority.choices, "filters": request.GET})
        template_name = self.partial_template_name if request.headers.get("HX-Request") == "true" else self.template_name
        return render(request, template_name, context)


class TaskCreateView(LoginRequiredMixin, View):
    template_name = "tasks/task_form.html"
    partial_template_name = "tasks/includes/task_form_panel.html"

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
                if _is_kanban_htmx(request):
                    response = _render_kanban_partial(
                        request,
                        board,
                        template_name="tasks/includes/kanban_create_response.html",
                        kanban_board_oob=True,
                        messages_oob=True,
                    )
                    response["HX-Trigger"] = "taskKanban:taskCreated"
                    return response
                if _is_htmx(request):
                    return _htmx_redirect(reverse("tasks:board_kanban", kwargs={"board_id": board.pk}))
                return redirect("tasks:board_kanban", board_id=board.pk)
        if _is_kanban_htmx(request):
            return _render_kanban_partial(
                request,
                board,
                template_name="tasks/includes/task_create_dialog_body.html",
                task_form=form,
                status=400,
            )
        template_name = self.partial_template_name if _is_htmx(request) else self.template_name
        return render(request, template_name, {"board": board, "form": form}, status=400)


class TaskEditView(LoginRequiredMixin, View):
    template_name = "tasks/task_form.html"
    partial_template_name = "tasks/includes/task_form_panel.html"

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
                if _is_htmx(request):
                    return _htmx_redirect(reverse("tasks:board_kanban", kwargs={"board_id": self.task.board_id}))
                return redirect("tasks:board_kanban", board_id=self.task.board_id)
        template_name = self.partial_template_name if _is_htmx(request) else self.template_name
        return render(request, template_name, {"board": self.task.board, "task": self.task, "form": form}, status=400)


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
        if _is_htmx(request):
            if request.POST.get("_kanban") == "1":
                return _render_kanban_partial(
                    request,
                    task.board,
                    template_name="tasks/includes/kanban_board_response.html",
                    messages_oob=True,
                )
            next_url = request.POST.get("next") or reverse("tasks:board_kanban", kwargs={"board_id": task.board_id})
            settings_url = reverse("tasks:board_settings", kwargs={"board_id": task.board_id})
            if next_url == settings_url:
                return _render_board_settings(request, task.board)
            return _htmx_redirect(next_url)
        return redirect(request.POST.get("next") or reverse("tasks:board_kanban", kwargs={"board_id": task.board_id}))


def _board_settings_context(
    *,
    request,
    board,
    member_form=None,
    transfer_form=None,
    stage_form=None,
    stage_forms=None,
    stage_delete_forms=None,
):
    stage_forms = stage_forms or {}
    stage_delete_forms = stage_delete_forms or {}
    stages = list(board.stages.order_by("position"))
    stage_rows = [
        {
            "stage": stage,
            "form": stage_forms.get(stage.pk) or StageForm(instance=stage, prefix=f"stage-{stage.pk}"),
            "delete_form": stage_delete_forms.get(stage.pk) or StageDeleteForm(stage=stage, prefix=f"delete-{stage.pk}"),
        }
        for stage in stages
    ]
    archived_tasks = visible_board_tasks(user=request.user, board=board, include_archived=True).filter(archived_at__isnull=False)
    return {
        "board": board,
        "members": board_members(board=board, active_only=False),
        "member_form": member_form or MemberAddForm(board=board),
        "transfer_form": transfer_form or OwnershipTransferForm(board=board),
        "stage_form": stage_form or StageForm(prefix="new-stage"),
        "stage_rows": stage_rows,
        "archived_tasks": archived_tasks,
    }


def _render_board_settings(request, board, *, status=200, **context_overrides):
    template_name = "tasks/includes/board_settings_content.html" if _is_htmx(request) else BoardSettingsView.template_name
    return render(
        request,
        template_name,
        _board_settings_context(request=request, board=board, **context_overrides),
        status=status,
    )


class BoardSettingsView(LoginRequiredMixin, View):
    template_name = "tasks/board_settings.html"

    def get(self, request, board_id):
        board = get_accessible_board(user=request.user, board_id=board_id, include_archived=True)
        require_board_manager(user=request.user, board=board)
        return _render_board_settings(request, board)


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
        if _is_htmx(request):
            return _render_board_settings(request, board, member_form=form if form.errors else None, status=400 if form.errors else 200)
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
        if _is_htmx(request):
            return _render_board_settings(request, board)
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
        if _is_htmx(request):
            return _render_board_settings(request, board, transfer_form=form if form.errors else None, status=400 if form.errors else 200)
        return redirect("tasks:board_settings", board_id=board.pk)


class BoardArchiveView(LoginRequiredMixin, View):
    def post(self, request, board_id):
        board = get_accessible_board(user=request.user, board_id=board_id, include_archived=True)
        require_board_manager(user=request.user, board=board)
        archived = request.POST.get("archived", "1") != "0"
        set_board_archived(actor=request.user, board=board, archived=archived)
        messages.success(request, "Board arhivat." if archived else "Board restaurat.")
        if _is_htmx(request):
            if not archived:
                return _htmx_redirect(reverse("tasks:board_kanban", kwargs={"board_id": board.pk}))
            return _render_board_settings(request, board)
        return redirect("tasks:board_settings", board_id=board.pk) if archived else redirect("tasks:board_kanban", board_id=board.pk)


class StageCreateView(LoginRequiredMixin, View):
    def post(self, request, board_id):
        board = get_accessible_board(user=request.user, board_id=board_id, include_archived=True)
        require_board_manager(user=request.user, board=board)
        form = StageForm(request.POST, prefix="new-stage")
        if form.is_valid():
            try:
                create_stage(actor=request.user, board=board, **form.cleaned_data)
            except (ValidationError, IntegrityError) as exc:
                messages.error(request, _error_text(exc) if isinstance(exc, ValidationError) else "Există deja o etapă cu acest nume.")
            else:
                messages.success(request, "Etapă adăugată.")
        else:
            messages.error(request, "Verifică datele etapei.")
        if _is_htmx(request):
            return _render_board_settings(request, board, stage_form=form if form.errors else None, status=400 if form.errors else 200)
        return redirect("tasks:board_settings", board_id=board.pk)


class StageUpdateView(LoginRequiredMixin, View):
    def post(self, request, stage_id):
        stage = get_object_or_404(TaskStage.objects.select_related("board"), pk=stage_id)
        get_accessible_board(user=request.user, board_id=stage.board_id, include_archived=True)
        require_board_manager(user=request.user, board=stage.board)
        form = StageForm(request.POST, instance=stage, prefix=f"stage-{stage.pk}")
        if form.is_valid():
            try:
                update_stage(actor=request.user, stage=stage, **form.cleaned_data)
            except (ValidationError, IntegrityError) as exc:
                messages.error(request, _error_text(exc) if isinstance(exc, ValidationError) else "Există deja o etapă cu acest nume.")
            else:
                messages.success(request, "Etapă actualizată.")
        else:
            messages.error(request, "Verifică datele etapei.")
        if _is_htmx(request):
            stage_forms = {stage.pk: form} if form.errors else None
            return _render_board_settings(request, stage.board, stage_forms=stage_forms, status=400 if form.errors else 200)
        return redirect("tasks:board_settings", board_id=stage.board_id)


class StagePositionView(LoginRequiredMixin, View):
    def post(self, request, stage_id):
        stage = get_object_or_404(TaskStage.objects.select_related("board"), pk=stage_id)
        get_accessible_board(user=request.user, board_id=stage.board_id, include_archived=True)
        require_board_manager(user=request.user, board=stage.board)
        direction = -1 if request.POST.get("direction") == "up" else 1
        move_stage_position(actor=request.user, stage=stage, direction=direction)
        if _is_htmx(request):
            return _render_board_settings(request, stage.board)
        return redirect("tasks:board_settings", board_id=stage.board_id)


class StageDeleteView(LoginRequiredMixin, View):
    def post(self, request, stage_id):
        stage = get_object_or_404(TaskStage.objects.select_related("board"), pk=stage_id)
        get_accessible_board(user=request.user, board_id=stage.board_id, include_archived=True)
        require_board_manager(user=request.user, board=stage.board)
        form = StageDeleteForm(request.POST, stage=stage, prefix=f"delete-{stage.pk}")
        if form.is_valid():
            try:
                delete_stage(actor=request.user, stage=stage, replacement=form.cleaned_data["replacement_stage"])
            except ValidationError as exc:
                messages.error(request, _error_text(exc))
            else:
                messages.success(request, "Etapa a fost eliminată, iar task-urile au fost mutate.")
        else:
            messages.error(request, "Alege o etapă validă de înlocuire.")
        if _is_htmx(request):
            stage_delete_forms = {stage.pk: form} if form.errors else None
            return _render_board_settings(request, stage.board, stage_delete_forms=stage_delete_forms, status=400 if form.errors else 200)
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

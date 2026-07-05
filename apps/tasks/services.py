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

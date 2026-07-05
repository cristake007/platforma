# apps/tasks/forms.py

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `apps/tasks/forms.py`
- App: `tasks`
- App guide: `codex-context/apps/tasks.md`
- Role: `backend`
- Size: 6342 bytes
- Source SHA-256: `cb3461e0d41b71b07af261c0afbd00aa070779542cd27ca0663bad48ef26b182`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

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
        labels = {"name": "Nume", "tone": "Ton semantic", "is_terminal": "Etapă terminală"}
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

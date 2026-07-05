# apps/tasks/tests.py

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `apps/tasks/tests.py`
- App: `tasks`
- App guide: `codex-context/apps/tasks.md`
- Role: `test`
- Size: 12785 bytes
- Source SHA-256: `065185852c5a74afbfe070f518417c347a824124f3afa3acc6efbf199f7ead94`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from datetime import timedelta

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

# apps/tasks/templates/tasks/includes/timer.html

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `apps/tasks/templates/tasks/includes/timer.html`
- App: `tasks`
- App guide: `codex-context/apps/tasks.md`
- Role: `template`
- Size: 573 bytes
- Source SHA-256: `adf0f7f1cfdf58031f2832f1cda52aceb5b37f4798f9abdb9045d8ed4eed8fad`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

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

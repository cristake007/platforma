# apps/tasks/templates/tasks/includes/messages.html

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `apps/tasks/templates/tasks/includes/messages.html`
- App: `tasks`
- App guide: `codex-context/apps/tasks.md`
- Role: `template`
- Size: 316 bytes
- Source SHA-256: `4e2ab9c003c72b479813bc6c967913ce961af419d7bf4f3ab60bd5dba265e349`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```html
{% if messages %}
<div class="space-y-2" aria-live="polite">
    {% for message in messages %}
        <div class="alert py-2 text-sm {% if message.tags == 'error' %}alert-error{% elif message.tags == 'success' %}alert-success{% else %}alert-info{% endif %}">{{ message }}</div>
    {% endfor %}
</div>
{% endif %}
```

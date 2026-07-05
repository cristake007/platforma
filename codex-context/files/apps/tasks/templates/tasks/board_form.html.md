# apps/tasks/templates/tasks/board_form.html

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `apps/tasks/templates/tasks/board_form.html`
- App: `tasks`
- App guide: `codex-context/apps/tasks.md`
- Role: `template`
- Size: 786 bytes
- Source SHA-256: `76403136282d1b8aee6c13e616033232cb8846576c9b1e27f9753361f6dc21cf`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```html
{% extends "layouts/base.html" %}
{% block title %}Board nou | Task-uri{% endblock %}
{% block content %}<section class="mx-auto max-w-xl space-y-5"><div><p class="text-xs text-muted"><a href="{% url 'tasks:index' %}" class="hover:text-primary">Task-uri</a> / Board nou</p><h1 class="ops-title mt-1 text-2xl font-bold">Creează un board</h1><p class="mt-1 text-sm text-muted">Vei deveni proprietar și membru al board-ului.</p></div><form method="post" class="space-y-4 border border-base-300 bg-base-100 p-5">{% csrf_token %}{% include "tasks/includes/form_fields.html" %}<div class="flex justify-end gap-2"><a href="{% url 'tasks:index' %}" class="btn btn-ghost btn-sm">Anulează</a><button class="btn btn-primary btn-sm">Creează board</button></div></form></section>{% endblock %}
```

# apps/tasks/templates/tasks/board_kanban.html

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `apps/tasks/templates/tasks/board_kanban.html`
- App: `tasks`
- App guide: `codex-context/apps/tasks.md`
- Role: `template`
- Size: 8825 bytes
- Source SHA-256: `d7a4e0d3379817e17114e2b8a1332ec2eaa69e9e20c5a075d0da690a66b2e32b`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```html
{% extends "layouts/base.html" %}
{% load static %}

{% block title %}{{ board.name }} | Task-uri{% endblock %}

{% block content %}
<section class="space-y-4" data-kanban-root data-state-url="{{ state_url }}">
    {% include "tasks/includes/messages.html" %}
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
        <label class="fieldset"><span class="fieldset-legend">Caută</span><input type="search" name="q" value="{{ filters.q|default:'' }}" class="input input-bordered input-sm w-full" placeholder="Caută task-uri…"></label>
        <div class="flex items-end gap-2"><button class="btn btn-primary btn-sm flex-1">Filtrează</button><a href="{% url 'tasks:board_kanban' board.pk %}" class="btn btn-ghost btn-sm">Resetează</a></div>
    </form>

    <div class="flex min-h-[32rem] gap-3 overflow-x-auto pb-3" data-kanban-board>
        {% for stage in stages %}
        <section class="flex w-72 shrink-0 flex-col border border-base-300 bg-base-200/60 {% if stage.tone == 'error' %}border-t-2 border-t-error{% elif stage.tone == 'success' %}border-t-2 border-t-success{% elif stage.tone == 'warning' %}border-t-2 border-t-warning{% elif stage.tone == 'info' %}border-t-2 border-t-primary{% endif %}" data-stage-column data-stage-id="{{ stage.pk }}">
            <header class="flex items-center justify-between border-b border-base-300 px-3 py-3">
                <h2 class="font-semibold text-base-content">{{ stage.name }}</h2>
                <span class="badge badge-sm bg-base-100" data-stage-count>{{ stage.visible_tasks|length }}</span>
            </header>
            <div class="flex min-h-32 flex-1 flex-col gap-2 p-2" data-stage-cards>
                {% for task in stage.visible_tasks %}
                <article class="border border-base-300 bg-base-100 p-3 shadow-sm focus-within:border-primary {% if task.can_move %}cursor-grab{% endif %}" data-task-card data-task-id="{{ task.pk }}" data-task-version="{{ task.version }}" data-move-url="{% url 'tasks:task_move' task.pk %}" {% if task.can_move %}draggable="true" tabindex="0"{% endif %}>
                    <div class="flex items-start justify-between gap-2"><h3 class="text-sm font-semibold leading-5 text-base-content">{{ task.title }}</h3>{% if task.origin_url %}<a href="{{ task.origin_url }}" class="shrink-0 text-primary" title="{{ task.origin_label|default:'Deschide sursa' }}">↗</a>{% endif %}</div>
                    {% if task.description %}<p class="mt-1 line-clamp-2 text-xs leading-5 text-muted">{{ task.description }}</p>{% endif %}
                    <div class="mt-3 flex items-center gap-2 text-xs"><span class="flex h-6 w-6 items-center justify-center rounded-full bg-base-200 font-bold">{{ task.assignee.username|slice:':2'|upper }}</span><span class="truncate">{{ task.assignee.get_full_name|default:task.assignee.username }}</span></div>
                    <div class="mt-2 flex flex-wrap items-center gap-2 text-xs"><span class="font-medium {% if task.priority == 'high' %}text-error{% elif task.priority == 'medium' %}text-warning{% else %}text-success{% endif %}">⚑ {{ task.get_priority_display }}</span>{% include "tasks/includes/timer.html" %}</div>
                    <div class="mt-3 flex items-center justify-between gap-2 border-t border-base-300 pt-2">
                        {% if task.can_edit %}<a href="{% url 'tasks:task_edit' task.pk %}" class="btn btn-ghost btn-xs">Editează</a>{% else %}<span></span>{% endif %}
                        {% if task.can_move %}
                        <form method="post" action="{% url 'tasks:task_move' task.pk %}" class="flex items-center gap-1" data-stage-fallback-form>
                            {% csrf_token %}<input type="hidden" name="target_index" value="99999"><input type="hidden" name="expected_version" value="{{ task.version }}">
                            <label class="sr-only" for="stage-{{ task.pk }}">Mută în etapa</label><select id="stage-{{ task.pk }}" name="stage" class="select select-ghost select-xs" onchange="this.form.submit()">{% for target in stages %}<option value="{{ target.pk }}"{% if target.pk == task.stage_id %} selected{% endif %}>{{ target.name }}</option>{% endfor %}</select>
                        </form>
                        {% endif %}
                    </div>
                </article>
                {% endfor %}
                <button type="button" class="mt-auto min-h-10 border border-dashed border-base-300 bg-base-100 text-sm text-muted hover:border-primary hover:text-primary" data-open-task-dialog>+ Adaugă task</button>
            </div>
        </section>
        {% endfor %}
    </div>
</section>

<dialog id="task-create-dialog" class="modal">
    <div class="modal-box max-w-2xl rounded-box border border-base-300 bg-base-100 shadow-xl">
        <form method="dialog"><button class="btn btn-ghost btn-sm btn-circle absolute right-3 top-3" aria-label="Închide">✕</button></form>
        <h2 class="text-xl font-bold text-base-content">Task nou</h2><p class="mt-1 text-sm text-muted">Adaugă un task în {{ board.name }}.</p>
        <form method="post" action="{% url 'tasks:task_create' board.pk %}" class="mt-5 space-y-4">
            {% csrf_token %}<div class="grid gap-x-4 sm:grid-cols-2">{% include "tasks/includes/form_fields.html" with form=task_form %}</div>
            <div class="flex justify-end gap-2"><button type="button" class="btn btn-ghost btn-sm" data-close-task-dialog>Anulează</button><button class="btn btn-primary btn-sm">Creează task</button></div>
        </form>
    </div>
    <form method="dialog" class="modal-backdrop"><button>Închide</button></form>
</dialog>
{% endblock %}

{% block page_scripts %}<script src="{% static 'tasks/tasks.js' %}" defer></script>{% endblock %}
```

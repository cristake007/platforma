# apps/tasks/templates/tasks/hub.html

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `apps/tasks/templates/tasks/hub.html`
- App: `tasks`
- App guide: `codex-context/apps/tasks.md`
- Role: `template`
- Size: 8735 bytes
- Source SHA-256: `e92f1f6f03e3e117f1b947c08d2d6e1ac4d456a8758980511fa46f6e20cf7c3c`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

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

    <form method="get" class="grid gap-3 border-b border-base-300 pb-4 sm:grid-cols-2 lg:grid-cols-8">
        <label class="fieldset"><span class="fieldset-legend">Board</span><select name="board" class="select select-bordered select-sm w-full"><option value="">Toate board-urile</option>{% for board in boards %}<option value="{{ board.pk }}"{% if filters.board == board.pk|stringformat:'s' %} selected{% endif %}>{{ board.name }}</option>{% endfor %}</select></label>
        <label class="fieldset lg:col-span-2"><span class="fieldset-legend">Caută</span><input name="q" value="{{ filters.q|default:'' }}" class="input input-bordered input-sm w-full" placeholder="Caută task-uri…"></label>
        <label class="fieldset"><span class="fieldset-legend">Relație</span><select name="relation" class="select select-bordered select-sm w-full"><option value="">Toate</option><option value="assigned"{% if filters.relation == 'assigned' %} selected{% endif %}>Atribuite mie</option><option value="created"{% if filters.relation == 'created' %} selected{% endif %}>Create de mine</option>{% if request.user.is_staff %}<option value="mine"{% if filters.relation == 'mine' %} selected{% endif %}>Doar ale mele</option>{% endif %}</select></label>
        <label class="fieldset"><span class="fieldset-legend">Prioritate</span><select name="priority" class="select select-bordered select-sm w-full"><option value="">Toate</option>{% for value,label in priority_choices %}<option value="{{ value }}"{% if filters.priority == value %} selected{% endif %}>{{ label }}</option>{% endfor %}</select></label>
        <label class="fieldset"><span class="fieldset-legend">Etapă</span><select name="stage" class="select select-bordered select-sm w-full"><option value="">Toate</option>{% for stage in stage_options %}<option value="{{ stage.pk }}"{% if filters.stage == stage.pk|stringformat:'s' %} selected{% endif %}>{{ stage.board.name }} · {{ stage.name }}</option>{% endfor %}</select></label>
        <label class="fieldset"><span class="fieldset-legend">Sortare</span><select name="sort" class="select select-bordered select-sm w-full"><option value="due_asc">Termen crescător</option><option value="due_desc"{% if filters.sort == 'due_desc' %} selected{% endif %}>Termen descrescător</option></select></label>
        <div class="flex items-end gap-2"><button class="btn btn-primary btn-sm flex-1">Filtrează</button><a href="{% url 'tasks:index' %}" class="btn btn-ghost btn-sm">Resetează</a></div>
    </form>

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
    <div class="flex items-center justify-between text-sm text-muted"><span>Pagina {{ page.number }} din {{ page.paginator.num_pages }}</span><div class="join">{% if page.has_previous %}<a class="btn btn-sm join-item" href="?page={{ page.previous_page_number }}">‹</a>{% endif %}{% if page.has_next %}<a class="btn btn-sm join-item" href="?page={{ page.next_page_number }}">›</a>{% endif %}</div></div>
    {% endif %}
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

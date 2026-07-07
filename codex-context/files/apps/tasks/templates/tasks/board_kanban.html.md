# Source snapshot

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

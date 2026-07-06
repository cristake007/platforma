# Source snapshot

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

# Source snapshot

## `apps/tasks/templates/tasks/board_list.html`

Size: 2.6 KB

```html
{% extends "layouts/base.html" %}
{% load static %}

{% block title %}{{ board.name }} — Listă | Task-uri{% endblock %}

{% block content %}
<section class="space-y-4">
    {% include "tasks/includes/messages.html" %}
    <div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div>
            <p class="text-xs text-muted"><a href="{% url 'tasks:index' %}" class="hover:text-primary">Task-uri</a> / Board</p>
            <h1 class="ops-title mt-1 text-2xl font-bold sm:text-[2rem]">{{ board.name }}</h1>
        </div>
        <div class="flex gap-2">
            {% if can_manage_board %}<a href="{% url 'tasks:board_settings' board.pk %}" class="btn btn-outline btn-sm">Setări board</a>{% endif %}
            <a href="{% url 'tasks:task_create' board.pk %}" class="btn btn-primary btn-sm">Task nou</a>
        </div>
    </div>
    <nav class="flex gap-5 border-b border-base-300">
        <a href="{% url 'tasks:board_kanban' board.pk %}" class="px-1 pb-2 text-sm font-medium hover:text-primary">Kanban</a>
        <span class="border-b-2 border-primary px-1 pb-2 text-sm font-semibold text-primary">Listă</span>
    </nav>
    <form
        method="get"
        class="grid gap-3 border-b border-base-300 pb-4 sm:grid-cols-2 lg:grid-cols-5"
        hx-get="{% url 'tasks:board_list' board.pk %}"
        hx-target="#task-list-results"
        hx-swap="outerHTML"
        hx-push-url="true"
    >
        <label class="fieldset lg:col-span-2"><span class="fieldset-legend">Caută</span><input name="q" value="{{ filters.q|default:'' }}" class="input input-bordered input-sm w-full" placeholder="Caută task-uri..."></label>
        <label class="fieldset"><span class="fieldset-legend">Prioritate</span><select name="priority" class="select select-bordered select-sm w-full"><option value="">Toate</option>{% for value,label in priority_choices %}<option value="{{ value }}"{% if filters.priority == value %} selected{% endif %}>{{ label }}</option>{% endfor %}</select></label>
        <label class="fieldset"><span class="fieldset-legend">Sortare</span><select name="sort" class="select select-bordered select-sm w-full"><option value="due_asc">Termen crescător</option><option value="due_desc"{% if filters.sort == 'due_desc' %} selected{% endif %}>Termen descrescător</option></select></label>
        <div class="flex items-end"><button class="btn btn-primary btn-sm w-full">Aplică</button></div>
    </form>
    {% include "tasks/includes/board_task_list.html" %}
</section>
{% endblock %}

{% block page_scripts %}<script src="{% static 'tasks/tasks.js' %}" defer></script>{% endblock %}
```

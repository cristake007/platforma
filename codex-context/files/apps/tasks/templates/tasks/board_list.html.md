# Source snapshot

## `apps/tasks/templates/tasks/board_list.html`

Size: 3.8 KB

```html
{% extends "layouts/base.html" %}
{% load static %}
{% block title %}{{ board.name }} — Listă | Task-uri{% endblock %}
{% block content %}
<section class="space-y-4">
    {% include "tasks/includes/messages.html" %}
    <div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between"><div><p class="text-xs text-muted"><a href="{% url 'tasks:index' %}" class="hover:text-primary">Task-uri</a> / Board</p><h1 class="ops-title mt-1 text-2xl font-bold sm:text-[2rem]">{{ board.name }}</h1></div><div class="flex gap-2">{% if can_manage_board %}<a href="{% url 'tasks:board_settings' board.pk %}" class="btn btn-outline btn-sm">Setări board</a>{% endif %}<a href="{% url 'tasks:task_create' board.pk %}" class="btn btn-primary btn-sm">Task nou</a></div></div>
    <nav class="flex gap-5 border-b border-base-300"><a href="{% url 'tasks:board_kanban' board.pk %}" class="px-1 pb-2 text-sm font-medium hover:text-primary">Kanban</a><span class="border-b-2 border-primary px-1 pb-2 text-sm font-semibold text-primary">Listă</span></nav>
    <form method="get" class="grid gap-3 border-b border-base-300 pb-4 sm:grid-cols-2 lg:grid-cols-5"><label class="fieldset lg:col-span-2"><span class="fieldset-legend">Caută</span><input name="q" value="{{ filters.q|default:'' }}" class="input input-bordered input-sm w-full" placeholder="Caută task-uri…"></label><label class="fieldset"><span class="fieldset-legend">Prioritate</span><select name="priority" class="select select-bordered select-sm w-full"><option value="">Toate</option>{% for value,label in priority_choices %}<option value="{{ value }}"{% if filters.priority == value %} selected{% endif %}>{{ label }}</option>{% endfor %}</select></label><label class="fieldset"><span class="fieldset-legend">Sortare</span><select name="sort" class="select select-bordered select-sm w-full"><option value="due_asc">Termen crescător</option><option value="due_desc"{% if filters.sort == 'due_desc' %} selected{% endif %}>Termen descrescător</option></select></label><div class="flex items-end"><button class="btn btn-primary btn-sm w-full">Aplică</button></div></form>
    <div class="overflow-x-auto border border-base-300"><table class="table table-sm min-w-[900px]"><thead><tr><th>Task</th><th>Etapă</th><th>Prioritate</th><th>Responsabil</th><th>Termen</th><th>Timp rămas</th><th class="text-right">Acțiuni</th></tr></thead><tbody>{% for task in page %}<tr class="hover:bg-base-200/60"><td><p class="font-semibold">{{ task.title }}</p>{% if task.origin_url %}<a href="{{ task.origin_url }}" class="text-xs text-primary">{{ task.origin_label|default:'Deschide sursa' }} ↗</a>{% endif %}</td><td><span class="badge badge-outline badge-sm">{{ task.stage.name }}</span></td><td>{{ task.get_priority_display }}</td><td>{{ task.assignee.get_full_name|default:task.assignee.username }}</td><td class="whitespace-nowrap">{{ task.due_at|date:'d.m.Y H:i' }}</td><td>{% include "tasks/includes/timer.html" %}</td><td><div class="flex justify-end gap-1">{% if task.can_edit %}<a href="{% url 'tasks:task_edit' task.pk %}" class="btn btn-square btn-ghost btn-xs text-primary hover:bg-primary/10" aria-label="Editează task-ul" title="Editează task-ul"><svg xmlns="http://www.w3.org/2000/svg" class="size-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="m16.862 3.487 3.651 3.651M4.5 19.5l4.228-.845a2 2 0 0 0 1.024-.547L20.513 7.347a1.75 1.75 0 0 0 0-2.474l-1.386-1.386a1.75 1.75 0 0 0-2.474 0L5.892 14.248a2 2 0 0 0-.547 1.024L4.5 19.5Z" /></svg></a>{% endif %}</div></td></tr>{% empty %}<tr><td colspan="7" class="py-12 text-center text-muted">Nu există task-uri.</td></tr>{% endfor %}</tbody></table></div>
</section>
{% endblock %}
{% block page_scripts %}<script src="{% static 'tasks/tasks.js' %}" defer></script>{% endblock %}
```

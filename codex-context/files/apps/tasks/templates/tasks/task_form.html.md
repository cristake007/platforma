# Source snapshot

## `apps/tasks/templates/tasks/task_form.html`

Size: 588 B

```html
{% extends "layouts/base.html" %}
{% block title %}{% if task %}Editeaz&#259; {{ task.title }}{% else %}Task nou{% endif %} | Task-uri{% endblock %}
{% block content %}
<section class="mx-auto max-w-2xl space-y-5">
    <div>
        <p class="text-xs text-muted"><a href="{% url 'tasks:board_kanban' board.pk %}" class="hover:text-primary">{{ board.name }}</a> / Task</p>
        <h1 class="ops-title mt-1 text-2xl font-bold">{% if task %}Editeaz&#259; task-ul{% else %}Task nou{% endif %}</h1>
    </div>
    {% include "tasks/includes/task_form_panel.html" %}
</section>
{% endblock %}
```

# Source snapshot

## `apps/tasks/templates/tasks/board_form.html`

Size: 563 B

```html
{% extends "layouts/base.html" %}
{% block title %}Board nou | Task-uri{% endblock %}
{% block content %}
<section class="mx-auto max-w-xl space-y-5">
    <div>
        <p class="text-xs text-muted"><a href="{% url 'tasks:index' %}" class="hover:text-primary">Task-uri</a> / Board nou</p>
        <h1 class="ops-title mt-1 text-2xl font-bold">Creeaz&#259; un board</h1>
        <p class="mt-1 text-sm text-muted">Vei deveni proprietar &#537;i membru al board-ului.</p>
    </div>
    {% include "tasks/includes/board_form_panel.html" %}
</section>
{% endblock %}
```

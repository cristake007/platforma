# Source snapshot

## `apps/tasks/templates/tasks/includes/board_form_panel.html`

Size: 513 B

```html
<form
    id="board-form-panel"
    method="post"
    class="space-y-4 border border-base-300 bg-base-100 p-5"
    hx-post="{% url 'tasks:board_create' %}"
    hx-target="#board-form-panel"
    hx-swap="outerHTML"
>
    {% csrf_token %}
    {% include "tasks/includes/form_fields.html" %}
    <div class="flex justify-end gap-2">
        <a href="{% url 'tasks:index' %}" class="btn btn-ghost btn-sm">Anuleaz&#259;</a>
        <button class="btn btn-primary btn-sm">Creeaz&#259; board</button>
    </div>
</form>
```

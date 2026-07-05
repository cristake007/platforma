# Source snapshot

## `apps/flota/templates/flota/includes/deadline_badge.html`

Size: 409 B

```html
<span
    class="badge badge-sm whitespace-nowrap
        {% if state.tone == 'success' %}badge-success badge-outline
        {% elif state.tone == 'warning' %}badge-warning badge-outline
        {% elif state.tone == 'error' %}badge-error badge-outline
        {% else %}badge-ghost{% endif %}"
    {% if due_on %}data-deadline data-due-date="{{ due_on|date:'Y-m-d' }}"{% endif %}
>{{ state.label }}</span>

```

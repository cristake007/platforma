# Source snapshot

## `apps/tasks/templates/tasks/includes/kanban_messages.html`

Size: 132 B

```html
<div id="task-messages"{% if messages_oob %} hx-swap-oob="true"{% endif %}>
    {% include "tasks/includes/messages.html" %}
</div>
```

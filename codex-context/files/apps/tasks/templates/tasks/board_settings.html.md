# Source snapshot

## `apps/tasks/templates/tasks/board_settings.html`

Size: 203 B

```html
{% extends "layouts/base.html" %}
{% block title %}Set&#259;ri {{ board.name }} | Task-uri{% endblock %}
{% block content %}
    {% include "tasks/includes/board_settings_content.html" %}
{% endblock %}
```

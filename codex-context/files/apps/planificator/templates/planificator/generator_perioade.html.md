# Source snapshot

## `apps/planificator/templates/planificator/generator_perioade.html`

Size: 401 B

```html
{% extends "layouts/base.html" %}
{% load static %}

{% block title %}{% if history_read_only %}Program generat{% else %}Generator perioade{% endif %} | Platforma TUVTK{% endblock %}

{% block content %}
    {% include "planificator/includes/generator_workflow.html" %}
{% endblock %}

{% block page_scripts %}
    <script src="{% static 'planificator/generator.js' %}" defer></script>
{% endblock %}
```

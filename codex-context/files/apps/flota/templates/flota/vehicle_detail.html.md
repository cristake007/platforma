# Source snapshot

## `apps/flota/templates/flota/vehicle_detail.html`

Size: 324 B

```html
{% extends "layouts/base.html" %}
{% load static %}

{% block title %}{{ vehicle.brand }} {{ vehicle.model }} | Flota{% endblock %}

{% block content %}
{% include "flota/includes/vehicle_detail_panel.html" %}
{% endblock %}

{% block page_scripts %}<script src="{% static 'flota/flota.js' %}" defer></script>{% endblock %}
```

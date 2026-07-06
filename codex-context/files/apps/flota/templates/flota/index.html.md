# Source snapshot

## `apps/flota/templates/flota/index.html`

Size: 1.1 KB

```html
{% extends "layouts/base.html" %}
{% load static %}

{% block title %}Flota | Platforma TUVTK{% endblock %}

{% block content %}
<section class="space-y-5">
    {% include "flota/includes/messages.html" %}

    <div class="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
            <h1 class="ops-title text-2xl font-bold sm:text-[2rem]">Flota</h1>
            <p class="mt-1 text-sm text-muted">Administrarea vehiculelor și a termenelor de mentenanță.</p>
        </div>
        {% if request.user.is_staff %}
        <div class="flex flex-wrap gap-2">
            <a href="{% url 'flota:maintenance_type_list' %}" class="btn btn-outline btn-primary btn-sm">Tipuri mentenanță</a>
            <a href="{% url 'flota:vehicle_create' %}" class="btn btn-primary btn-sm">
                <i class="bi bi-plus-lg" aria-hidden="true"></i> Adaugă vehicul
            </a>
        </div>
        {% endif %}
    </div>

    {% include "flota/includes/fleet_panel.html" %}
</section>
{% endblock %}

{% block page_scripts %}<script src="{% static 'flota/flota.js' %}" defer></script>{% endblock %}
```

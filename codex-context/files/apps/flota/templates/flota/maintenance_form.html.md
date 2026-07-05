# Source snapshot

## `apps/flota/templates/flota/maintenance_form.html`

Size: 1.1 KB

```html
{% extends "layouts/base.html" %}

{% block title %}{% if record %}Editează mentenanța{% else %}Mentenanță nouă{% endif %} | Flota{% endblock %}

{% block content %}
<section class="mx-auto max-w-3xl space-y-5">
    <div>
        <p class="text-xs text-muted"><a href="{% url 'flota:vehicle_detail' vehicle.pk %}" class="hover:text-primary">{{ vehicle.brand }} {{ vehicle.model }}</a> / Mentenanță</p>
        <h1 class="ops-title mt-1 text-2xl font-bold">{% if record %}Editează înregistrarea{% else %}Înregistrează mentenanța{% endif %}</h1>
        <p class="mt-1 text-sm text-muted">{{ vehicle.registration_display }} · {{ vehicle.current_mileage }} km</p>
    </div>
    <form method="post" class="space-y-5 border border-base-300 bg-base-100 p-5">
        {% csrf_token %}
        <div class="grid gap-x-4 sm:grid-cols-2">{% include "flota/includes/form_fields.html" %}</div>
        <div class="flex justify-end gap-2">
            <a href="{% url 'flota:vehicle_detail' vehicle.pk %}" class="btn btn-ghost btn-sm">Anulează</a>
            <button class="btn btn-primary btn-sm">Salvează</button>
        </div>
    </form>
</section>
{% endblock %}

```

# apps/flota/templates/flota/maintenance_form.html

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `apps/flota/templates/flota/maintenance_form.html`
- App: `flota`
- App guide: `codex-context/apps/flota.md`
- Role: `template`
- Size: 1173 bytes
- Source SHA-256: `cee3c62ac86e02065a7a63e174fb4cf4418c7f333415fba146a2bd0850875c5b`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

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

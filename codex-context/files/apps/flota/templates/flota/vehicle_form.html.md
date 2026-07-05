# apps/flota/templates/flota/vehicle_form.html

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `apps/flota/templates/flota/vehicle_form.html`
- App: `flota`
- App guide: `codex-context/apps/flota.md`
- Role: `template`
- Size: 1158 bytes
- Source SHA-256: `d2ae18a93a1909a96dfadbdd9c0a7049d9dcc5265da66b5be5c50abdb4359a34`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```html
{% extends "layouts/base.html" %}

{% block title %}{% if vehicle %}Editează {{ vehicle }}{% else %}Vehicul nou{% endif %} | Flota{% endblock %}

{% block content %}
<section class="mx-auto max-w-3xl space-y-5">
    <div>
        <p class="text-xs text-muted"><a href="{% url 'flota:index' %}" class="hover:text-primary">Flota</a> / Vehicul</p>
        <h1 class="ops-title mt-1 text-2xl font-bold">{% if vehicle %}Editează vehiculul{% else %}Adaugă vehicul{% endif %}</h1>
        <p class="mt-1 text-sm text-muted">Datele vehiculului și responsabilul curent.</p>
    </div>
    <form method="post" enctype="multipart/form-data" class="space-y-5 border border-base-300 bg-base-100 p-5">
        {% csrf_token %}
        <div class="grid gap-x-4 sm:grid-cols-2">{% include "flota/includes/form_fields.html" %}</div>
        <div class="flex justify-end gap-2">
            <a href="{% if vehicle %}{% url 'flota:vehicle_detail' vehicle.pk %}{% else %}{% url 'flota:index' %}{% endif %}" class="btn btn-ghost btn-sm">Anulează</a>
            <button class="btn btn-primary btn-sm">Salvează</button>
        </div>
    </form>
</section>
{% endblock %}
```

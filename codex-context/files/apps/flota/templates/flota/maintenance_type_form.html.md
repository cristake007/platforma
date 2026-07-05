# apps/flota/templates/flota/maintenance_type_form.html

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `apps/flota/templates/flota/maintenance_type_form.html`
- App: `flota`
- App guide: `codex-context/apps/flota.md`
- Role: `template`
- Size: 1013 bytes
- Source SHA-256: `637f3e8b1a56feec06251f2960822d3d4013fa1606e32b4806b992bb16cad914`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```html
{% extends "layouts/base.html" %}

{% block title %}{% if maintenance_type %}Editează tipul{% else %}Tip nou{% endif %} | Flota{% endblock %}

{% block content %}
<section class="mx-auto max-w-2xl space-y-5">
    <div>
        <p class="text-xs text-muted"><a href="{% url 'flota:maintenance_type_list' %}" class="hover:text-primary">Tipuri mentenanță</a> / Formular</p>
        <h1 class="ops-title mt-1 text-2xl font-bold">{% if maintenance_type %}Editează tipul{% else %}Tip de mentenanță nou{% endif %}</h1>
    </div>
    <form method="post" class="space-y-5 border border-base-300 bg-base-100 p-5">
        {% csrf_token %}
        <div class="grid gap-x-4 sm:grid-cols-2">{% include "flota/includes/form_fields.html" %}</div>
        <div class="flex justify-end gap-2">
            <a href="{% url 'flota:maintenance_type_list' %}" class="btn btn-ghost btn-sm">Anulează</a>
            <button class="btn btn-primary btn-sm">Salvează</button>
        </div>
    </form>
</section>
{% endblock %}
```

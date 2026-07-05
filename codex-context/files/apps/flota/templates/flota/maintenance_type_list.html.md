# apps/flota/templates/flota/maintenance_type_list.html

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `apps/flota/templates/flota/maintenance_type_list.html`
- App: `flota`
- App guide: `codex-context/apps/flota.md`
- Role: `template`
- Size: 2243 bytes
- Source SHA-256: `52b7cbdc9b6eebbf85b80e3a4cab10b70fcf2c885ebd57839db30aee76ecbaad`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```html
{% extends "layouts/base.html" %}

{% block title %}Tipuri mentenanță | Flota{% endblock %}

{% block content %}
<section class="space-y-5">
    {% include "flota/includes/messages.html" %}
    <div class="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
            <p class="text-xs text-muted"><a href="{% url 'flota:index' %}" class="hover:text-primary">Flota</a> / Configurare</p>
            <h1 class="ops-title mt-1 text-2xl font-bold">Tipuri de mentenanță</h1>
            <p class="mt-1 text-sm text-muted">Tipurile de sistem sunt protejate; tipurile personalizate pot fi arhivate.</p>
        </div>
        <a href="{% url 'flota:maintenance_type_create' %}" class="btn btn-primary btn-sm">Tip nou</a>
    </div>
    <div class="overflow-x-auto border border-base-300 bg-base-100">
        <table class="table table-sm min-w-[680px]">
            <thead><tr><th>Denumire</th><th>Cod</th><th>Ordine</th><th>Tip</th><th>Status</th><th class="text-right">Acțiuni</th></tr></thead>
            <tbody>
            {% for item in maintenance_types %}
                <tr>
                    <td class="font-semibold">{{ item.name }}</td>
                    <td><code class="text-xs">{{ item.code }}</code></td>
                    <td>{{ item.display_order }}</td>
                    <td>{% if item.is_system %}Sistem{% else %}Personalizat{% endif %}</td>
                    <td><span class="badge badge-sm {% if item.is_active %}badge-success badge-outline{% else %}badge-ghost{% endif %}">{% if item.is_active %}Activ{% else %}Arhivat{% endif %}</span></td>
                    <td><div class="flex justify-end gap-1"><a href="{% url 'flota:maintenance_type_edit' item.pk %}" class="btn btn-ghost btn-xs">Editează</a>{% if not item.is_system and item.is_active %}<form method="post" action="{% url 'flota:maintenance_type_archive' item.pk %}">{% csrf_token %}<button class="btn btn-ghost btn-xs text-error">Arhivează</button></form>{% endif %}</div></td>
                </tr>
            {% empty %}<tr><td colspan="6" class="py-10 text-center text-muted">Nu există tipuri de mentenanță.</td></tr>{% endfor %}
            </tbody>
        </table>
    </div>
</section>
{% endblock %}
```

# apps/flota/templates/flota/vehicle_detail.html

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `apps/flota/templates/flota/vehicle_detail.html`
- App: `flota`
- App guide: `codex-context/apps/flota.md`
- Role: `template`
- Size: 9845 bytes
- Source SHA-256: `607eaa93a86b5b06cb7d5f956fa2421c432e74932d6382f677414b933b5f29ac`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```html
{% extends "layouts/base.html" %}
{% load static %}

{% block title %}{{ vehicle.brand }} {{ vehicle.model }} | Flota{% endblock %}

{% block content %}
<section class="space-y-5">
    {% include "flota/includes/messages.html" %}
    <nav class="text-xs text-muted" aria-label="Breadcrumb">
        <a href="{% url 'flota:index' %}" class="hover:text-primary">Flota</a> / {{ vehicle.registration_display }}
    </nav>

    <header class="flex flex-col gap-4 border border-base-300 bg-base-100 p-4 lg:flex-row lg:items-center">
        <span class="flex h-16 w-16 shrink-0 items-center justify-center border border-base-300 bg-base-100">
            {% if vehicle.emblem %}
                <img src="{{ vehicle.emblem.url }}" alt="Emblema {{ vehicle.brand }}" class="h-12 w-12 object-contain">
            {% else %}
                <span class="text-xl font-bold text-primary" aria-hidden="true">{{ vehicle.brand|slice:":1"|upper }}</span>
            {% endif %}
        </span>
        <div class="min-w-0">
            <h1 class="ops-title text-2xl font-bold">{{ vehicle.brand }} {{ vehicle.model }}</h1>
            <div class="mt-1 flex flex-wrap items-center gap-2 text-sm">
                <span class="font-semibold text-base-content">{{ vehicle.registration_display }}</span>
                <span class="badge badge-sm {% if vehicle.is_archived %}badge-ghost{% elif vehicle.status == 'active' %}badge-success badge-outline{% else %}badge-warning badge-outline{% endif %}">
                    {% if vehicle.is_archived %}Arhivat{% else %}{{ vehicle.get_status_display }}{% endif %}
                </span>
            </div>
        </div>
        <div class="lg:ml-8 lg:border-l lg:border-base-300 lg:pl-8">
            <p class="text-xs text-muted">Responsabil</p>
            <p class="mt-1 text-sm font-medium text-base-content">
                {% if current_assignment %}{{ current_assignment.assignee.get_full_name|default:current_assignment.assignee.username }}{% else %}Neatribuit{% endif %}
            </p>
        </div>
        {% if request.user.is_staff %}
        <div class="flex flex-wrap gap-2 lg:ml-auto">
            <a href="{% url 'flota:vehicle_edit' vehicle.pk %}" class="btn btn-primary btn-sm">Editează</a>
            {% if vehicle.is_archived %}
            <form method="post" action="{% url 'flota:vehicle_restore' vehicle.pk %}">{% csrf_token %}<button class="btn btn-outline btn-success btn-sm">Restaurează</button></form>
            {% else %}
            <form method="post" action="{% url 'flota:vehicle_archive' vehicle.pk %}">{% csrf_token %}<button class="btn btn-outline btn-error btn-sm">Arhivează</button></form>
            {% endif %}
        </div>
        {% endif %}
    </header>

    <div class="grid gap-5 xl:grid-cols-[minmax(280px,0.8fr)_minmax(0,2fr)]">
        <div class="space-y-5">
            <section class="border border-base-300 bg-base-100">
                <h2 class="border-b border-base-300 px-4 py-3 text-sm font-semibold text-base-content">Date vehicul</h2>
                <dl class="divide-y divide-base-300 text-sm">
                    <div class="grid grid-cols-2 gap-3 px-4 py-3"><dt class="text-muted">VIN</dt><dd class="text-right font-medium">{{ vehicle.vin|default:"—" }}</dd></div>
                    <div class="grid grid-cols-2 gap-3 px-4 py-3"><dt class="text-muted">An fabricație</dt><dd class="text-right font-medium">{{ vehicle.manufacture_year|default:"—" }}</dd></div>
                    <div class="grid grid-cols-2 gap-3 px-4 py-3"><dt class="text-muted">Kilometraj</dt><dd class="text-right font-medium">{{ vehicle.current_mileage }} km</dd></div>
                    <div class="grid grid-cols-2 gap-3 px-4 py-3"><dt class="text-muted">Status</dt><dd class="text-right font-medium">{{ vehicle.get_status_display }}</dd></div>
                    <div class="grid grid-cols-2 gap-3 px-4 py-3"><dt class="text-muted">Responsabil</dt><dd class="text-right font-medium">{% if current_assignment %}{{ current_assignment.assignee.get_full_name|default:current_assignment.assignee.username }}{% else %}Neatribuit{% endif %}</dd></div>
                </dl>
            </section>

            <section class="border border-base-300 bg-base-100">
                <div class="flex items-center justify-between border-b border-base-300 px-4 py-3">
                    <h2 class="text-sm font-semibold text-base-content">Termene mentenanță</h2>
                    {% if request.user.is_staff and not vehicle.is_archived %}<a href="{% url 'flota:maintenance_create' vehicle.pk %}" class="btn btn-primary btn-xs">Înregistrează</a>{% endif %}
                </div>
                <div class="divide-y divide-base-300">
                    {% for row in deadline_rows %}
                    <div class="space-y-2 px-4 py-3">
                        <div class="flex items-center justify-between gap-3">
                            <h3 class="text-sm font-semibold text-base-content">{{ row.type.name }}</h3>
                            {% include "flota/includes/deadline_badge.html" with state=row.state due_on=row.record.next_due_on %}
                        </div>
                        <div class="grid grid-cols-2 gap-3 text-xs">
                            <div><span class="block text-muted">Ultima efectuare</span><span class="font-medium">{% if row.record %}{{ row.record.completed_on|date:"d.m.Y" }}{% else %}—{% endif %}</span></div>
                            <div><span class="block text-muted">Următorul termen</span><span class="font-medium">{% if row.record %}{{ row.record.next_due_on|date:"d.m.Y" }}{% else %}—{% endif %}</span></div>
                        </div>
                        {% if request.user.is_staff and not vehicle.is_archived %}<a href="{% url 'flota:maintenance_create' vehicle.pk %}?type={{ row.type.pk }}" class="text-xs font-medium text-primary hover:underline">Înregistrează {{ row.type.name|lower }}</a>{% endif %}
                    </div>
                    {% empty %}<p class="px-4 py-8 text-center text-sm text-muted">Nu există tipuri de mentenanță active.</p>{% endfor %}
                </div>
            </section>
        </div>

        <div class="space-y-5">
            <section class="border border-base-300 bg-base-100">
                <div class="flex items-center justify-between border-b border-base-300 px-4 py-3">
                    <h2 class="text-sm font-semibold text-base-content">Istoric servicii</h2>
                    {% if request.user.is_staff and not vehicle.is_archived %}<a href="{% url 'flota:maintenance_create' vehicle.pk %}" class="btn btn-primary btn-xs">Înregistrare nouă</a>{% endif %}
                </div>
                <div class="overflow-x-auto">
                    <table class="table table-sm min-w-[760px]">
                        <thead><tr><th>Tip</th><th>Efectuat la</th><th>Următorul termen</th><th>Kilometraj</th><th>Furnizor</th><th>Cost</th><th class="text-right">Acțiuni</th></tr></thead>
                        <tbody>
                        {% for record in maintenance_records %}
                            <tr>
                                <td class="font-medium">{{ record.maintenance_type.name }}</td>
                                <td class="whitespace-nowrap">{{ record.completed_on|date:"d.m.Y" }}</td>
                                <td class="whitespace-nowrap">{{ record.next_due_on|date:"d.m.Y" }}</td>
                                <td class="whitespace-nowrap">{% if record.mileage is not None %}{{ record.mileage }} km{% else %}—{% endif %}</td>
                                <td>{{ record.provider|default:"—" }}</td>
                                <td class="whitespace-nowrap">{% if record.cost is not None %}{{ record.cost }} lei{% else %}—{% endif %}</td>
                                <td class="text-right">{% if request.user.is_staff %}<a href="{% url 'flota:maintenance_edit' record.pk %}" class="btn btn-ghost btn-xs">Editează</a>{% else %}—{% endif %}</td>
                            </tr>
                        {% empty %}<tr><td colspan="7" class="py-10 text-center text-muted">Nu există intervenții înregistrate.</td></tr>{% endfor %}
                        </tbody>
                    </table>
                </div>
            </section>

            <section class="border border-base-300 bg-base-100">
                <h2 class="border-b border-base-300 px-4 py-3 text-sm font-semibold text-base-content">Istoric atribuiri</h2>
                <div class="overflow-x-auto">
                    <table class="table table-sm min-w-[560px]">
                        <thead><tr><th>De la</th><th>Până la</th><th>Responsabil</th><th>Atribuit de</th></tr></thead>
                        <tbody>
                        {% for assignment in assignment_history %}
                            <tr>
                                <td class="whitespace-nowrap">{{ assignment.starts_at|date:"d.m.Y H:i" }}</td>
                                <td class="whitespace-nowrap">{% if assignment.ends_at %}{{ assignment.ends_at|date:"d.m.Y H:i" }}{% else %}Prezent{% endif %}</td>
                                <td>{{ assignment.assignee.get_full_name|default:assignment.assignee.username }}</td>
                                <td>{{ assignment.assigned_by.get_full_name|default:assignment.assigned_by.username }}</td>
                            </tr>
                        {% empty %}<tr><td colspan="4" class="py-8 text-center text-muted">Vehiculul nu a fost atribuit.</td></tr>{% endfor %}
                        </tbody>
                    </table>
                </div>
            </section>
        </div>
    </div>
</section>
{% endblock %}

{% block page_scripts %}<script src="{% static 'flota/flota.js' %}" defer></script>{% endblock %}
```

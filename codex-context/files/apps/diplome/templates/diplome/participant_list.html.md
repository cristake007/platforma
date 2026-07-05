# apps/diplome/templates/diplome/participant_list.html

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `apps/diplome/templates/diplome/participant_list.html`
- App: `diplome`
- App guide: `codex-context/apps/diplome.md`
- Role: `template`
- Size: 4464 bytes
- Source SHA-256: `a2ca95509b0fe3839cc002f04a7e6f73a646e2b24b981b2db2b857b54334b61a`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```html
{% extends "layouts/base.html" %}

{% block title %}Liste participanți | Platforma TUVTK{% endblock %}

{% block content %}
<section class="mx-auto w-full max-w-6xl space-y-6">
    <div class="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div class="space-y-2">
            <div class="breadcrumbs p-0 text-sm text-muted"><ul><li>Diplome</li><li>Liste participanți</li></ul></div>
            <div>
                <h1 class="text-2xl font-bold text-primary">Liste participanți</h1>
                <p class="mt-1 text-sm text-muted">Listele confirmate rămân disponibile până când alegi să le ștergi.</p>
            </div>
        </div>
        <a href="{% url 'diplome:participant_import' %}" class="btn btn-primary btn-sm">Importă o listă</a>
    </div>

    {% if messages %}
        {% for message in messages %}
            <div class="alert {% if message.tags == 'error' %}alert-error{% else %}alert-success{% endif %} py-2 text-sm" role="status"><span>{{ message }}</span></div>
        {% endfor %}
    {% endif %}

    <div class="overflow-hidden border border-base-300 bg-base-100">
        {% if participant_lists %}
            <div class="overflow-x-auto">
                <table class="table table-sm">
                    <thead class="bg-base-200 text-xs uppercase tracking-wide text-muted">
                        <tr><th>Listă</th><th>Curs</th><th>Participanți</th><th>Fișier sursă</th><th>Creată</th><th class="text-right">Acțiuni</th></tr>
                    </thead>
                    <tbody>
                        {% for participant_list in participant_lists %}
                            <tr>
                                <td>
                                    <a href="{% url 'diplome:participant_list_detail' participant_list.pk %}" class="font-semibold text-primary hover:underline">{{ participant_list.name }}</a>
                                    {% if participant_list.description %}<p class="mt-0.5 max-w-lg text-xs text-muted">{{ participant_list.description }}</p>{% endif %}
                                </td>
                                <td>{{ participant_list.course_name|default:"—" }}</td>
                                <td>{{ participant_list.participant_count }}</td>
                                <td>{{ participant_list.source_file_name }}</td>
                                <td class="whitespace-nowrap">{{ participant_list.created_at|date:"d.m.Y H:i" }}</td>
                                <td>
                                    <div class="flex justify-end gap-2">
                                        <a href="{% url 'diplome:participant_list_detail' participant_list.pk %}" class="btn btn-outline btn-primary btn-xs">Deschide</a>
                                        <form method="post" action="{% url 'diplome:participant_list_delete' participant_list.pk %}">
                                            {% csrf_token %}
                                            <button type="submit" class="btn btn-ghost btn-xs text-error">Șterge</button>
                                        </form>
                                    </div>
                                </td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        {% else %}
            <div class="px-6 py-14 text-center">
                <h2 class="text-lg font-semibold text-base-content">Nu există liste de participanți</h2>
                <p class="mt-2 text-sm text-muted">Importă un fișier CSV sau XLSX pentru a crea prima listă.</p>
                <a href="{% url 'diplome:participant_import' %}" class="btn btn-primary btn-sm mt-5">Importă prima listă</a>
            </div>
        {% endif %}
    </div>
    {% if is_paginated %}
        <nav class="flex items-center justify-between text-sm" aria-label="Paginare liste participanți">
            <span class="text-muted">Pagina {{ page_obj.number }} din {{ page_obj.paginator.num_pages }}</span>
            <div class="join">
                {% if page_obj.has_previous %}<a href="?page={{ page_obj.previous_page_number }}" class="btn btn-sm join-item">Anterior</a>{% endif %}
                {% if page_obj.has_next %}<a href="?page={{ page_obj.next_page_number }}" class="btn btn-sm join-item">Următor</a>{% endif %}
            </div>
        </nav>
    {% endif %}
</section>
{% endblock %}
```

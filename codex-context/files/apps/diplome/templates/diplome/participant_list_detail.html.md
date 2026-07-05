# apps/diplome/templates/diplome/participant_list_detail.html

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `apps/diplome/templates/diplome/participant_list_detail.html`
- App: `diplome`
- App guide: `codex-context/apps/diplome.md`
- Role: `template`
- Size: 2993 bytes
- Source SHA-256: `da3d2935b47dd16a3325879e7a7c3e7d6f28c910b49e10329f8108738f8300ca`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```html
{% extends "layouts/base.html" %}

{% block title %}{{ participant_list.name }} | Platforma TUVTK{% endblock %}

{% block content %}
<section class="mx-auto w-full max-w-7xl space-y-6">
    <div class="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div class="space-y-2">
            <div class="breadcrumbs p-0 text-sm text-muted"><ul><li>Diplome</li><li><a href="{% url 'diplome:list_index' %}">Liste participanți</a></li><li>{{ participant_list.name }}</li></ul></div>
            <div>
                <h1 class="text-2xl font-bold text-primary">{{ participant_list.name }}</h1>
                {% if participant_list.description %}<p class="mt-1 text-sm text-muted">{{ participant_list.description }}</p>{% endif %}
                <p class="mt-2 text-xs text-muted">{% if participant_list.course_name %}Curs: {{ participant_list.course_name }} · {% endif %}Fișier: {{ participant_list.source_file_name }} · {{ participant_list.participant_count }} participanți</p>
            </div>
        </div>
        <form method="post" action="{% url 'diplome:participant_list_delete' participant_list.pk %}">
            {% csrf_token %}
            <button type="submit" class="btn btn-outline btn-error btn-sm">Șterge lista</button>
        </form>
    </div>

    {% if messages %}{% for message in messages %}<div class="alert alert-success py-2 text-sm" role="status"><span>{{ message }}</span></div>{% endfor %}{% endif %}

    <div class="overflow-x-auto border border-base-300 bg-base-100">
        <table class="table table-sm">
            <thead class="bg-base-200 text-xs uppercase tracking-wide text-muted"><tr><th>#</th><th>Nume complet</th><th>Data nașterii</th><th>Locul nașterii</th><th>Număr certificat</th></tr></thead>
            <tbody>
                {% for participant in participants %}
                    <tr><td>{{ page_obj.start_index|add:forloop.counter0 }}</td><td class="font-medium">{{ participant.full_name }}</td><td>{{ participant.date_of_birth|date:"d.m.Y" }}</td><td>{{ participant.place_of_birth }}</td><td>{{ participant.certificate_number }}</td></tr>
                {% empty %}
                    <tr><td colspan="5" class="py-8 text-center text-muted">Lista nu conține participanți.</td></tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    {% if is_paginated %}
        <nav class="flex items-center justify-between text-sm" aria-label="Paginare participanți">
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

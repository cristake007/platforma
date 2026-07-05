# apps/diplome/templates/diplome/generation_preview.html

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `apps/diplome/templates/diplome/generation_preview.html`
- App: `diplome`
- App guide: `codex-context/apps/diplome.md`
- Role: `template`
- Size: 5156 bytes
- Source SHA-256: `1f6249ba15ed03b7fe0c1dacd62a6f9726765c29746ff1d3ea732c83440b6ba3`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```html
{% extends "layouts/base.html" %}
{% load static %}

{% block title %}Previzualizare diplomă | Platforma TUVTK{% endblock %}

{% block page_styles %}
<link rel="stylesheet" href="{% static 'diplome/template_editor.css' %}">
{% endblock %}

{% block content %}
<section class="mx-auto w-full max-w-7xl space-y-6">
    <header class="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div class="space-y-2">
            <div class="breadcrumbs p-0 text-sm text-muted">
                <ul><li>Diplome</li><li><a href="{% url 'diplome:generation_index' %}?{{ selection_query }}">Generare</a></li><li>Previzualizare</li></ul>
            </div>
            <div>
                <h1 class="text-2xl font-bold text-primary">Previzualizare diplomă</h1>
                <p class="mt-1 text-sm text-muted">Verifică datele și aspectul înainte de generarea fișierului PDF.</p>
            </div>
        </div>
        <a href="{% url 'diplome:generation_index' %}?{{ selection_query }}" class="btn btn-outline btn-primary btn-sm">Înapoi la selecție</a>
    </header>

    {% if messages %}
        {% for message in messages %}<div class="alert alert-success py-2 text-sm" role="status"><span>{{ message }}</span></div>{% endfor %}
    {% endif %}

    {% if generated_diploma %}
        <div class="flex flex-col gap-3 border border-success/40 bg-success/10 p-4 sm:flex-row sm:items-center sm:justify-between" role="status">
            <div>
                <p class="font-semibold text-base-content">Diploma PDF a fost generată.</p>
                <p class="mt-1 text-xs text-muted">{{ generated_diploma.created_at|date:"d.m.Y H:i" }} · {{ generated_diploma.participant_name }} · {{ generated_diploma.certificate_number }}</p>
            </div>
            <a href="{% url 'diplome:generation_download' generated_diploma.pk %}" class="btn btn-success btn-sm">Descarcă PDF</a>
        </div>
    {% endif %}

    <div class="grid gap-6 xl:grid-cols-[minmax(0,1fr)_20rem]">
        <div id="generation-diploma-preview" class="overflow-hidden border border-base-300 bg-base-100">
            <div class="preview-workspace !min-h-0 p-4 sm:p-6">
                <div class="preview-canvas-frame" id="preview-canvas-frame">
                    <div class="diploma-canvas preview-canvas" id="preview-canvas" aria-label="Previzualizare diplomă cu datele participantului"></div>
                </div>
            </div>
            {{ layout|json_script:"diploma-layout-data" }}
            {{ participant_data|json_script:"diploma-sample-data" }}
            {{ media_assets|json_script:"diploma-media-assets-data" }}
        </div>

        <aside class="space-y-5 border border-base-300 bg-base-100 p-5">
            <div>
                <h2 class="text-sm font-semibold uppercase tracking-wide text-muted">Participant</h2>
                <p class="mt-2 font-semibold text-base-content">{{ participant.full_name }}</p>
                <dl class="mt-3 space-y-2 text-sm">
                    <div><dt class="text-xs text-muted">Număr certificat</dt><dd class="font-medium text-base-content">{{ participant.certificate_number }}</dd></div>
                    <div><dt class="text-xs text-muted">Data nașterii</dt><dd class="text-base-content">{{ participant.date_of_birth|date:"d.m.Y" }}</dd></div>
                    <div><dt class="text-xs text-muted">Locul nașterii</dt><dd class="text-base-content">{{ participant.place_of_birth }}</dd></div>
                </dl>
            </div>
            <div class="border-t border-base-300 pt-4">
                <h2 class="text-sm font-semibold uppercase tracking-wide text-muted">Sursă și template</h2>
                <dl class="mt-3 space-y-2 text-sm">
                    <div><dt class="text-xs text-muted">Listă</dt><dd class="text-base-content">{{ participant_list.name }}</dd></div>
                    <div><dt class="text-xs text-muted">Template</dt><dd class="text-base-content">{{ diploma_template.name }}</dd></div>
                    <div><dt class="text-xs text-muted">Format</dt><dd class="text-base-content">{{ diploma_template.page_size }} · {{ diploma_template.get_orientation_display }}</dd></div>
                </dl>
            </div>
            <form method="post" action="{% url 'diplome:generation_create' %}" class="border-t border-base-300 pt-5">
                {% csrf_token %}
                <input type="hidden" name="participant_list" value="{{ participant_list.pk }}">
                <input type="hidden" name="participant" value="{{ participant.pk }}">
                <input type="hidden" name="template" value="{{ diploma_template.pk }}">
                <button type="submit" class="btn btn-primary btn-sm w-full">Generează PDF</button>
                <p class="mt-2 text-center text-xs text-muted">Se creează un singur fișier pentru participantul selectat.</p>
            </form>
        </aside>
    </div>
</section>
{% endblock %}

{% block page_scripts %}
<script src="{% static 'diplome/template_renderer.js' %}" defer></script>
<script src="{% static 'diplome/template_preview.js' %}" defer></script>
{% endblock %}
```

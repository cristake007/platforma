# apps/diplome/templates/diplome/participant_import_mapping.html

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `apps/diplome/templates/diplome/participant_import_mapping.html`
- App: `diplome`
- App guide: `codex-context/apps/diplome.md`
- Role: `template`
- Size: 5881 bytes
- Source SHA-256: `62762dc81ba64b26365a787a9abdf764e7a139e32d11681b2b1ccc0fe09b26d0`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```html
{% extends "layouts/base.html" %}
{% load static %}

{% block title %}Asociere coloane | Platforma TUVTK{% endblock %}

{% block content %}
<section class="mx-auto w-full max-w-6xl space-y-8">
    <div class="space-y-2">
        <div class="breadcrumbs p-0 text-sm text-muted"><ul><li>Diplome</li><li><a href="{% url 'diplome:list_index' %}">Liste participanți</a></li><li>Asociere coloane</li></ul></div>
        <div>
            <h1 class="text-2xl font-bold text-primary">Importă și asociază datele</h1>
            <p class="mt-1 text-sm text-muted">Fișierul {{ draft.source_file_name }} conține {{ draft.source_rows_json|length }} rânduri și {{ draft.source_columns_json|length }} coloane.</p>
        </div>
    </div>

    <section class="space-y-3" aria-labelledby="source-preview-title">
        <div>
            <h2 id="source-preview-title" class="text-lg font-semibold text-base-content"><span class="mr-2 inline-flex size-6 items-center justify-center rounded-full border border-base-content text-sm">1</span>Verifică datele importate</h2>
            <p class="mt-1 pl-8 text-sm text-muted">Primele cinci rânduri sunt afișate pentru orientare.</p>
        </div>
        <div class="overflow-x-auto border border-base-300 bg-base-100">
            <table class="table table-sm">
                <thead class="bg-base-200 text-xs uppercase tracking-wide text-muted">
                    <tr>{% for column in draft.source_columns_json %}<th>{{ column.label }}</th>{% endfor %}</tr>
                </thead>
                <tbody>
                    {% for row in draft.source_rows_json|slice:":5" %}
                        <tr>{% for value in row.values %}<td class="max-w-64 truncate">{{ value|default:"—" }}</td>{% endfor %}</tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </section>

    <form method="post" class="space-y-5" data-mapping-form>
        {% csrf_token %}
        <div>
            <h2 class="text-lg font-semibold text-base-content"><span class="mr-2 inline-flex size-6 items-center justify-center rounded-full border border-base-content text-sm">2</span>Asociază coloanele</h2>
            <p class="mt-1 pl-8 text-sm text-muted">Pentru fiecare coloană din fișier, selectează câmpul predefinit din sistem. Coloanele suplimentare pot rămâne pe „Nu importa”.</p>
        </div>

        {% if form.non_field_errors %}
            <div class="alert alert-error py-3 text-sm" role="alert">{{ form.non_field_errors }}</div>
        {% endif %}

        <div class="hidden grid-cols-[minmax(10rem,0.8fr)_minmax(16rem,1.5fr)_minmax(14rem,1fr)_7rem] gap-5 px-5 text-xs font-semibold uppercase tracking-wide text-muted md:grid">
            <span>Coloană din fișier</span>
            <span>Date detectate</span>
            <span>Câmp în sistem</span>
            <span>Stare</span>
        </div>

        <div class="space-y-3">
            {% for row in mapping_rows %}
                <div class="grid gap-4 border border-base-300 bg-base-100 p-5 transition-colors md:grid-cols-[minmax(10rem,0.8fr)_minmax(16rem,1.5fr)_minmax(14rem,1fr)_7rem] md:items-center md:gap-5" data-mapping-row>
                    <div>
                        <span class="mb-1 block text-xs font-semibold uppercase tracking-wide text-muted md:hidden">Coloană din fișier</span>
                        <p class="font-semibold text-base-content">{{ row.column.label }}</p>
                    </div>
                    <div>
                        <span class="mb-1 block text-xs font-semibold uppercase tracking-wide text-muted md:hidden">Date detectate</span>
                        <ul class="space-y-0.5 text-sm text-base-content">
                            {% for sample in row.column.samples %}<li class="truncate">{{ sample }}</li>{% empty %}<li class="text-muted">—</li>{% endfor %}
                        </ul>
                    </div>
                    <label class="form-control w-full">
                        <span class="mb-1 block text-xs font-semibold uppercase tracking-wide text-muted md:hidden">Câmp în sistem</span>
                        {{ row.field }}
                        {% for error in row.field.errors %}<span class="mt-1 text-xs text-error">{{ error }}</span>{% endfor %}
                    </label>
                    <div class="flex items-center gap-2 text-sm text-muted" data-mapping-status>
                        <svg class="hidden size-5 text-success" data-mapped-icon viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path fill-rule="evenodd" d="M10 18a8 8 0 1 0 0-16 8 8 0 0 0 0 16Zm3.7-9.3a1 1 0 0 0-1.4-1.4L9 10.6 7.7 9.3a1 1 0 0 0-1.4 1.4l2 2a1 1 0 0 0 1.4 0l4-4Z" clip-rule="evenodd"/></svg>
                        <svg class="size-5" data-ignored-icon viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path fill-rule="evenodd" d="M4 10a1 1 0 0 1 1-1h10a1 1 0 1 1 0 2H5a1 1 0 0 1-1-1Z" clip-rule="evenodd"/></svg>
                        <span data-status-label>Ignorată</span>
                    </div>
                </div>
            {% endfor %}
        </div>

        <div class="flex flex-col gap-3 border-t border-base-300 pt-5 sm:flex-row sm:items-center sm:justify-between">
            <p class="text-sm text-muted"><span class="font-semibold text-base-content" data-mapped-count>0</span> din 4 câmpuri obligatorii asociate</p>
            <div class="flex justify-end gap-2">
                <a href="{% url 'diplome:participant_import' %}" class="btn btn-ghost btn-sm">Încarcă alt fișier</a>
                <button type="submit" class="btn btn-primary btn-sm">Continuă la verificare</button>
            </div>
        </div>
    </form>
</section>
{% endblock %}

{% block page_scripts %}
<script src="{% static 'diplome/participant_mapping.js' %}" defer></script>
{% endblock %}
```

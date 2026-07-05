# apps/diplome/templates/diplome/participant_import.html

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `apps/diplome/templates/diplome/participant_import.html`
- App: `diplome`
- App guide: `codex-context/apps/diplome.md`
- Role: `template`
- Size: 3928 bytes
- Source SHA-256: `c3bec8c8000161113b0950dae9be23b3702398eb2fb76d4493ed7a4068e779a8`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```html
{% extends "layouts/base.html" %}
{% load static %}

{% block title %}Import participanți | Platforma TUVTK{% endblock %}

{% block content %}
<section class="mx-auto w-full max-w-2xl space-y-6">
    <div class="space-y-2">
        <div class="breadcrumbs p-0 text-sm text-muted"><ul><li>Diplome</li><li><a href="{% url 'diplome:list_index' %}">Liste participanți</a></li><li>Import</li></ul></div>
        <div>
            <h1 class="text-2xl font-bold text-primary">Importă participanți</h1>
            <p class="mt-1 text-sm text-muted">Completează detaliile listei și încarcă fișierul pentru verificare.</p>
        </div>
    </div>

    <form method="post" enctype="multipart/form-data" class="space-y-5 border border-base-300 bg-base-100 p-6" data-participant-import-form novalidate>
        {% csrf_token %}
        {% if form.non_field_errors %}<div class="alert alert-error py-2 text-sm">{{ form.non_field_errors }}</div>{% endif %}
        <label class="form-control w-full">
            <span class="label-text mb-1 text-sm font-semibold">Numele listei</span>
            {{ form.list_name }}
            {% for error in form.list_name.errors %}<span class="mt-1 text-xs text-error">{{ error }}</span>{% endfor %}
        </label>
        <label class="form-control w-full">
            <span class="label-text mb-1 text-sm font-semibold">Descriere <span class="font-normal text-muted">(opțional)</span></span>
            {{ form.description }}
            {% for error in form.description.errors %}<span class="mt-1 text-xs text-error">{{ error }}</span>{% endfor %}
        </label>
        <label class="form-control w-full">
            <span class="label-text mb-1 text-sm font-semibold">Denumirea cursului <span class="font-normal text-muted">(opțional)</span></span>
            {{ form.course_name }}
            {% for error in form.course_name.errors %}<span class="mt-1 text-xs text-error">{{ error }}</span>{% endfor %}
        </label>
        <label class="form-control w-full">
            <span class="label-text mb-1 text-sm font-semibold">Fișier CSV sau XLSX</span>
            {{ form.source_file }}
            <span class="mt-2 text-xs text-muted">Fișierul trebuie să conțină valorile pentru nume, data și locul nașterii și numărul certificatului. Denumirile coloanelor sunt libere și vor fi asociate în pasul următor. Pentru un XLSX cu mai multe foi valide, vei alege foaia pe care dorești să o imporți. Data trebuie scrisă strict DD.MM.YYYY.</span>
            {% for error in form.source_file.errors %}<span class="mt-1 text-xs text-error">{{ error }}</span>{% endfor %}
        </label>
        <label class="flex cursor-pointer items-center gap-3 border border-base-300 bg-base-200/50 p-3">
            {{ form.first_row_has_headers }}
            <span>
                <span class="block text-sm font-semibold">Primul rând conține denumirile coloanelor</span>
                <span class="block text-xs text-muted">Debifează pentru fișiere fără antet; coloanele vor fi numerotate automat.</span>
            </span>
        </label>
        <div class="flex justify-end gap-2 border-t border-base-300 pt-5">
            <a href="{% url 'diplome:list_index' %}" class="btn btn-ghost btn-sm">Renunță</a>
            <button type="submit" class="btn btn-primary btn-sm">Descoperă coloanele</button>
        </div>
    </form>
</section>

<div class="toast toast-top toast-end z-50{% if not form.list_name.errors %} hidden{% endif %}" data-participant-import-toast aria-live="assertive" aria-atomic="true">
    <div class="alert alert-error text-sm shadow-lg" role="alert">
        <span data-participant-import-toast-message>{% if form.list_name.errors %}{{ form.list_name.errors.0 }}{% endif %}</span>
    </div>
</div>
{% endblock %}

{% block page_scripts %}
<script src="{% static 'diplome/participant_import.js' %}" defer></script>
{% endblock %}
```

# apps/diplome/templates/diplome/template_form.html

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `apps/diplome/templates/diplome/template_form.html`
- App: `diplome`
- App guide: `codex-context/apps/diplome.md`
- Role: `template`
- Size: 2662 bytes
- Source SHA-256: `d4e5d9c0d278108fe4dab3b40b88b02598a5eed5c48efa4d4d01ba70dc60abd0`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```html
{% extends "layouts/base.html" %}

{% block title %}Template nou | Platforma TUVTK{% endblock %}

{% block content %}
<section class="w-full max-w-2xl space-y-6">
    <div class="space-y-2">
        <div class="breadcrumbs p-0 text-sm text-muted">
            <ul><li>Diplome</li><li><a href="{% url 'diplome:template_list' %}">Template-uri</a></li><li>Template nou</li></ul>
        </div>
        <div>
            <h1 class="text-2xl font-bold text-primary">Creează un template</h1>
            <p class="mt-1 text-sm text-muted">Configurează documentul de bază. Elementele vizuale se editează în pasul următor.</p>
        </div>
    </div>

    <form method="post" class="space-y-5 border border-base-300 bg-base-100 p-6">
        {% csrf_token %}
        {% if form.non_field_errors %}<div class="alert alert-error py-2 text-sm">{{ form.non_field_errors }}</div>{% endif %}
        <label class="form-control w-full">
            <span class="label-text mb-1 text-sm font-semibold">Nume</span>
            {{ form.name }}
            {% for error in form.name.errors %}<span class="mt-1 text-xs text-error">{{ error }}</span>{% endfor %}
        </label>
        <label class="form-control w-full">
            <span class="label-text mb-1 text-sm font-semibold">Categorie</span>
            {{ form.category }}
            <span class="mt-1 text-xs text-muted">Folosită pentru organizarea și filtrarea template-urilor.</span>
            {% for error in form.category.errors %}<span class="mt-1 text-xs text-error">{{ error }}</span>{% endfor %}
        </label>
        <label class="form-control w-full">
            <span class="label-text mb-1 text-sm font-semibold">Descriere</span>
            {{ form.description }}
            {% for error in form.description.errors %}<span class="mt-1 text-xs text-error">{{ error }}</span>{% endfor %}
        </label>
        <div class="grid gap-4 sm:grid-cols-2">
            <label class="form-control w-full">
                <span class="label-text mb-1 text-sm font-semibold">Format pagină</span>
                {{ form.page_size }}
            </label>
            <label class="form-control w-full">
                <span class="label-text mb-1 text-sm font-semibold">Orientare</span>
                {{ form.orientation }}
            </label>
        </div>
        <div class="flex justify-end gap-2 border-t border-base-300 pt-5">
            <a href="{% url 'diplome:template_list' %}" class="btn btn-ghost btn-sm">Renunță</a>
            <button type="submit" class="btn btn-primary btn-sm">Creează și deschide editorul</button>
        </div>
    </form>
</section>
{% endblock %}
```

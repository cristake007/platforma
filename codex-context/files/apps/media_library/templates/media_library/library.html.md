# apps/media_library/templates/media_library/library.html

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `apps/media_library/templates/media_library/library.html`
- App: `media_library`
- App guide: `codex-context/apps/media_library.md`
- Role: `template`
- Size: 3967 bytes
- Source SHA-256: `85184fc6c7f3e3615dc51a1d2588dbfc2db186741a2e57fcabb8dcf1fa5fd367`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```html
{% extends "layouts/base.html" %}
{% load static %}

{% block title %}Bibliotecă media | Platforma TUVTK{% endblock %}

{% block page_styles %}
<link rel="stylesheet" href="{% static 'media_library/library.css' %}">
{% endblock %}

{% block content %}
<section class="mx-auto w-full max-w-7xl space-y-6">
    <header class="space-y-2">
        <div class="breadcrumbs p-0 text-sm text-muted"><ul><li>Operațiuni</li><li>Bibliotecă media</li></ul></div>
        <div>
            <h1 class="text-2xl font-bold text-primary">Bibliotecă media</h1>
            <p class="mt-1 text-sm text-muted">Încarcă o singură dată imagini reutilizabile în template-urile de diplomă.</p>
        </div>
    </header>

    {% if messages %}
        {% for message in messages %}<div class="alert {% if message.tags == 'error' %}alert-error{% else %}alert-success{% endif %} py-2 text-sm" role="status"><span>{{ message }}</span></div>{% endfor %}
    {% endif %}

    <div class="grid gap-6 lg:grid-cols-[22rem_minmax(0,1fr)]">
        <form method="post" enctype="multipart/form-data" class="space-y-4 border border-base-300 bg-base-100 p-5">
            {% csrf_token %}
            <div><h2 class="font-semibold text-base-content">Adaugă fișier</h2><p class="mt-1 text-xs text-muted">SVG static sigur, PNG, JPG, JPEG sau WEBP. Maximum 10 MB.</p></div>
            {% if form.non_field_errors %}<div class="alert alert-error py-2 text-sm">{{ form.non_field_errors }}</div>{% endif %}
            {% for field in form %}
                <label class="form-control w-full">
                    <span class="label"><span class="label-text font-medium">{{ field.label }}</span></span>
                    {{ field }}
                    {% for error in field.errors %}<span class="mt-1 text-xs text-error">{{ error }}</span>{% endfor %}
                </label>
            {% endfor %}
            <button type="submit" class="btn btn-primary btn-sm w-full">Încarcă în bibliotecă</button>
        </form>

        <div class="border border-base-300 bg-base-100">
            <div class="flex items-center justify-between border-b border-base-300 px-5 py-4"><h2 class="font-semibold text-base-content">Fișierele mele</h2><span class="badge badge-ghost">{{ assets|length }}</span></div>
            {% if assets %}
                <div class="grid grid-cols-2 gap-4 p-5 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6">
                    {% for asset in assets %}
                        <article class="flex h-full flex-col overflow-hidden border border-base-300 bg-base-100">
                            <div class="media-asset-preview shrink-0 bg-base-200"><img src="{% url 'media_library:content' asset.pk %}" alt="{{ asset.name }}"></div>
                            <div class="flex flex-1 flex-col gap-3 p-3">
                                <div class="grid h-10 min-w-0 grid-rows-2 content-start">
                                    <h3 class="h-5 truncate text-sm font-semibold leading-5 text-base-content" title="{{ asset.name }}">{{ asset.name }}</h3>
                                    <p class="h-5 truncate text-xs leading-5 text-muted" title="{{ asset.original_filename }}">{{ asset.original_filename }}</p>
                                </div>
                                <div class="mt-auto flex min-h-7 items-center justify-between gap-2"><span class="badge badge-outline h-7">{{ asset.extension|upper }}</span><form method="post" action="{% url 'media_library:delete' asset.pk %}" class="flex items-center">{% csrf_token %}<button type="submit" class="btn btn-ghost h-7 min-h-7 px-2 text-error">Șterge</button></form></div>
                            </div>
                        </article>
                    {% endfor %}
                </div>
            {% else %}
                <div class="p-10 text-center text-sm text-muted">Biblioteca este goală.</div>
            {% endif %}
        </div>
    </div>
</section>
{% endblock %}
```

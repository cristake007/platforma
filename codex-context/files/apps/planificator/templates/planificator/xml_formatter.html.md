# Source snapshot

## `apps/planificator/templates/planificator/xml_formatter.html`

Size: 5.3 KB

```html
{% extends "layouts/base.html" %}
{% load static %}

{% block title %}Convertor XML | Platforma TUVTK{% endblock %}

{% block content %}
    <section class="mx-auto w-full min-w-0 max-w-340 space-y-5">
        <div class="space-y-2">
            <div class="breadcrumbs p-0 text-sm text-muted">
                <ul>
                    <li>Planificator</li>
                    <li>Convertor XML</li>
                </ul>
            </div>
            <div>
                <h1 class="ops-title text-2xl font-bold sm:text-[2rem]">Generează exportul XML</h1>
                <p class="mt-1 max-w-3xl text-sm leading-6 text-muted">
                    Încarcă programul de cursuri și generează fișierul XML compatibil cu importul evenimentelor în WordPress.
                </p>
            </div>
        </div>

        <div id="xml-export-error" class="alert alert-error hidden py-2 text-sm" role="alert" aria-live="assertive"></div>
        <div id="xml-export-success" class="alert alert-success hidden py-2 text-sm" role="status" aria-live="polite"></div>

        <form
            id="xml-export-form"
            method="post"
            action="{% url 'planificator:xml_export' %}"
            enctype="multipart/form-data"
            class="card card-border border-base-300 bg-base-100 shadow-none"
            data-download-filename="formatted_courses.xml"
            hx-boost="false"
            x-data="{ fileName: 'Niciun fișier selectat' }"
            x-on:xml-reset-upload.window="fileName = 'Niciun fișier selectat'"
            novalidate
        >
            {% csrf_token %}
            <div class="card-body gap-5 p-4 sm:p-5">
                <div class="flex flex-col justify-between gap-2 border-b border-base-300 pb-3 sm:flex-row sm:items-start">
                    <div>
                        <p class="text-xs font-semibold uppercase tracking-[0.16em] text-primary">Fișier sursă</p>
                        <h2 class="mt-1 text-lg font-semibold text-base-content">Programul generat</h2>
                        <p class="mt-1 text-sm text-muted">Fișierul trebuie să conțină coloanele Title, Permalink și cel puțin o coloană lunară.</p>
                    </div>
                    <span class="badge badge-outline badge-sm self-start whitespace-nowrap">Maximum 20 MB</span>
                </div>

                <fieldset class="fieldset min-w-0 rounded-field border border-base-300 bg-base-200 p-3">
                    <label class="fieldset-legend" for="{{ form.input_file.id_for_label }}">{{ form.input_file.label }}</label>
                    <div x-ref="xmlInput" x-on:change="fileName = $event.target.files?.[0]?.name || 'Niciun fișier selectat'">{{ form.input_file }}</div>
                    <div class="flex min-w-0 flex-col gap-2 sm:flex-row sm:items-center">
                        <button id="xml-file-select" type="button" class="btn btn-outline btn-primary btn-sm shrink-0" x-on:click="$refs.xmlInput.querySelector('input').click()">Alege CSV/XLSX</button>
                        <span id="xml-file-name" class="min-w-0 truncate text-sm" x-bind:class="{ 'text-muted': fileName === 'Niciun fișier selectat' }" x-text="fileName">Niciun fișier selectat</span>
                    </div>
                    <p class="label block whitespace-normal wrap-break-word text-xs leading-5 text-muted">
                        Sunt acceptate CSV și XLSX. Coloanele lunare pot folosi denumiri în română, engleză sau formatul Luna 1–Luna 12.
                    </p>
                    <p id="xml-file-error" class="label hidden text-error" role="alert"></p>
                </fieldset>

                <fieldset class="fieldset max-w-sm rounded-field border border-base-300 bg-base-200 p-3">
                    <label class="fieldset-legend" for="{{ form.start_post_id.id_for_label }}">{{ form.start_post_id.label }}</label>
                    {{ form.start_post_id }}
                    <p class="label block whitespace-normal text-xs leading-5 text-muted">
                        Primul eveniment va primi exact acest ID. Evenimentele următoare vor fi numerotate consecutiv.
                    </p>
                    <p id="xml-post-id-error" class="label hidden text-error" role="alert"></p>
                </fieldset>

                <div class="flex flex-col-reverse justify-between gap-3 border-t border-base-300 pt-4 sm:flex-row sm:items-center">
                    <p class="text-xs leading-5 text-muted">Fișierul este procesat doar pentru export și nu este salvat în istoric.</p>
                    <button id="xml-generate-button" type="submit" class="btn btn-primary btn-sm">
                        Generează XML
                    </button>
                </div>
            </div>
        </form>
    </section>

    <div id="xml-export-loading" class="fixed inset-0 z-70 hidden items-center justify-center bg-base-content/20 p-4" role="status" aria-live="polite">
        <div class="flex items-center gap-3 rounded-field border border-base-300 bg-base-100 px-4 py-3 shadow-lg">
            <span class="loading loading-spinner loading-md text-primary" aria-hidden="true"></span>
            <span class="text-sm font-medium">Se generează fișierul XML…</span>
        </div>
    </div>
{% endblock %}

{% block page_scripts %}
    <script src="{% static 'planificator/xml_formatter.js' %}" defer></script>
{% endblock %}
```

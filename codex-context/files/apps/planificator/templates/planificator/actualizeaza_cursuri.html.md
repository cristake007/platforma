# apps/planificator/templates/planificator/actualizeaza_cursuri.html

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `apps/planificator/templates/planificator/actualizeaza_cursuri.html`
- App: `planificator`
- App guide: `codex-context/apps/planificator.md`
- Role: `template`
- Size: 9188 bytes
- Source SHA-256: `5223c7124da169d9ac7abc9371113512b180733d0397dfb69f1e4de02267704c`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```html
{% extends "layouts/base.html" %}
{% load static %}

{% block title %}Actualizează cursuri | Platforma TUVTK{% endblock %}

{% block content %}
    <section class="mx-auto w-full min-w-0 max-w-[1500px] space-y-5">
        <div class="space-y-2">
            <div class="breadcrumbs p-0 text-sm text-muted">
                <ul>
                    <li>Planificator</li>
                    <li>Actualizează cursuri</li>
                </ul>
            </div>
            <div>
                <h1 class="ops-title text-2xl font-bold sm:text-[2rem]">Actualizează cursuri</h1>
                <p class="mt-1 max-w-4xl text-sm leading-6 text-muted">
                    Încarcă programul, verifică datele existente din WordPress și aplică actualizările individual, numai după previzualizare.
                </p>
            </div>
        </div>

        <div class="alert items-start border border-secondary/40 bg-secondary/5 py-3 text-sm text-base-content shadow-none" role="note">
            <i class="bi bi-shield-exclamation mt-0.5 text-base text-secondary" aria-hidden="true"></i>
            <div>
                <p class="font-semibold">Accesul WordPress depinde de rețeaua serverului.</p>
                <p class="mt-0.5 leading-5 opacity-90">
                    Conectarea trebuie rulată din mediul cu acces VPN autorizat. Cloudflare poate afișa o provocare și respinge cererile provenite de la alte adrese IP.
                </p>
            </div>
        </div>

        <div id="course-updater-error" class="alert hidden border border-error/40 bg-error/5 py-2 text-sm text-error shadow-none" role="alert" aria-live="assertive"></div>
        <div id="course-updater-success" class="alert hidden border border-success/40 bg-success/5 py-2 text-sm text-success shadow-none" role="status" aria-live="polite"></div>

        <form
            id="course-updater-form"
            method="post"
            action="{% url 'planificator:actualizeaza_cursuri_preview' %}"
            enctype="multipart/form-data"
            class="grid min-w-0 gap-4 lg:grid-cols-[minmax(0,0.9fr)_minmax(0,1.35fr)]"
            data-connect-url="{% url 'planificator:actualizeaza_cursuri_connect' %}"
            data-fetch-dates-url="{% url 'planificator:actualizeaza_cursuri_fetch_dates' %}"
            data-update-url="{% url 'planificator:actualizeaza_cursuri_update_row' %}"
            novalidate
        >
            {% csrf_token %}
            <section class="card card-border min-w-0 border-base-300 bg-base-100 shadow-none">
                <div class="card-body gap-4 p-4 sm:p-5">
                    <div class="border-b border-base-300 pb-3">
                        <h2 class="text-lg font-semibold text-base-content">Program sursă</h2>
                        <p class="mt-1 text-sm leading-5 text-muted">Previzualizarea locală nu necesită conexiune la WordPress.</p>
                    </div>

                    <fieldset class="fieldset min-w-0 rounded-field border border-base-300 bg-base-200 p-3">
                        <label class="fieldset-legend" for="{{ form.input_file.id_for_label }}">{{ form.input_file.label }}</label>
                        {{ form.input_file }}
                        <div class="flex min-w-0 flex-col gap-2 sm:flex-row sm:items-center">
                            <button id="course-file-select" type="button" class="btn btn-outline btn-primary btn-sm shrink-0">Alege CSV/XLSX</button>
                            <span id="course-file-name" class="min-w-0 truncate text-sm text-muted">Niciun fișier selectat</span>
                        </div>
                        <p class="label block whitespace-normal text-xs leading-5 text-muted">Coloane obligatorii: Title și Permalink. Dimensiune maximă: 20 MB.</p>
                        <p id="course-file-error" class="label hidden text-error" role="alert"></p>
                    </fieldset>

                    <div class="mt-auto border-t border-base-300 pt-4">
                        <button id="course-preview-button" type="submit" class="btn btn-primary btn-sm w-full sm:w-auto">
                            <i class="bi bi-table" aria-hidden="true"></i>
                            Construiește previzualizarea
                        </button>
                    </div>
                </div>
            </section>

            <section class="card card-border min-w-0 border-base-300 bg-base-100 shadow-none">
                <div class="card-body gap-4 p-4 sm:p-5">
                    <div class="flex flex-col justify-between gap-2 border-b border-base-300 pb-3 sm:flex-row sm:items-start">
                        <div>
                            <h2 class="text-lg font-semibold text-base-content">Conexiune WordPress</h2>
                            <p class="mt-1 text-sm leading-5 text-muted">Parola de aplicație este folosită numai pentru cererea curentă și nu este salvată.</p>
                        </div>
                        <span id="wp-connection-status" class="badge badge-outline badge-sm whitespace-nowrap" role="status" aria-live="polite">Neconectat</span>
                    </div>

                    <div class="grid gap-3 md:grid-cols-2">
                        <fieldset class="fieldset md:col-span-2">
                            <label class="fieldset-legend" for="wp-base-url">URL WordPress</label>
                            <input id="wp-base-url" type="url" class="input input-primary input-sm w-full" value="{{ updater_settings.wp_base_url }}" placeholder="https://tuvkarpat.ro" autocomplete="url">
                        </fieldset>
                        <fieldset class="fieldset">
                            <label class="fieldset-legend" for="wp-username">Utilizator</label>
                            <input id="wp-username" type="text" class="input input-primary input-sm w-full" value="{{ updater_settings.wp_username }}" autocomplete="username">
                        </fieldset>
                        <fieldset class="fieldset">
                            <label class="fieldset-legend" for="wp-app-password">Parolă de aplicație</label>
                            <input id="wp-app-password" type="password" class="input input-primary input-sm w-full" autocomplete="off">
                        </fieldset>
                    </div>

                    <div class="mt-auto flex flex-wrap gap-2 border-t border-base-300 pt-4">
                        <button id="wp-connect-button" type="button" class="btn btn-primary btn-sm">
                            <i class="bi bi-plug" aria-hidden="true"></i>
                            Conectează
                        </button>
                        <button id="wp-disconnect-button" type="button" class="btn btn-outline btn-sm hidden">
                            Deconectează
                        </button>
                    </div>
                </div>
            </section>
        </form>

        <section id="course-preview-container" class="card card-border hidden min-w-0 border-base-300 bg-base-100 shadow-none">
            <div class="flex flex-col justify-between gap-2 border-b border-base-300 px-4 py-3 sm:flex-row sm:items-center sm:px-5">
                <div>
                    <h2 class="text-lg font-semibold text-base-content">Rezultate</h2>
                    <p id="course-preview-count" class="mt-0.5 text-xs text-muted"></p>
                </div>
                <p class="text-xs leading-5 text-muted">Fiecare actualizare este aplicată separat.</p>
            </div>
            <div class="min-w-0 p-4 pt-3 sm:p-5 sm:pt-3">
                <div id="course-preview-top-scroll" class="ops-course-updater-top-scroll" aria-hidden="true">
                    <div id="course-preview-top-scroll-inner"></div>
                </div>
                <div id="course-preview-table-scroll" class="ops-course-updater-scroll ops-scrollbar">
                    <table id="course-preview-table" class="table table-zebra table-sm ops-course-updater-table">
                        <colgroup>
                            <col class="w-[17.5rem]">
                            <col class="w-[12.5rem]">
                            <col class="w-[11.5rem]">
                            <col class="w-[14rem]">
                            <col class="w-[8rem]">
                            <col class="w-[9rem]">
                        </colgroup>
                        <thead>
                            <tr>
                                <th>Curs</th>
                                <th>Date din fișier</th>
                                <th>Date existente</th>
                                <th>Program final</th>
                                <th>Stare</th>
                                <th>Acțiuni</th>
                            </tr>
                        </thead>
                        <tbody id="course-preview-table-body"></tbody>
                    </table>
                </div>
            </div>
        </section>
    </section>
{% endblock %}

{% block page_scripts %}
    <script src="{% static 'planificator/course_updater.js' %}" defer></script>
{% endblock %}
```

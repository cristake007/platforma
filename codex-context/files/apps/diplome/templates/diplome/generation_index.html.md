# apps/diplome/templates/diplome/generation_index.html

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `apps/diplome/templates/diplome/generation_index.html`
- App: `diplome`
- App guide: `codex-context/apps/diplome.md`
- Role: `template`
- Size: 11312 bytes
- Source SHA-256: `0af0b97dcdff7152855f08781ad6afa0f887b27fd4ded5a0ae9b5dcb381b6000`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```html
{% extends "layouts/base.html" %}
{% load static %}

{% block title %}Generator diplome | Platforma TUVTK{% endblock %}

{% block content %}
<section class="mx-auto w-full max-w-6xl space-y-6">
    <header class="space-y-2">
        <div class="breadcrumbs p-0 text-sm text-muted">
            <ul><li>Diplome</li><li>Generare</li></ul>
        </div>
        <div>
            <h1 class="text-2xl font-bold text-primary">Generator diplome</h1>
            <p class="mt-1 text-sm text-muted">Generează o diplomă individuală sau toate diplomele unei liste.</p>
        </div>
    </header>

    <div class="grid gap-6 lg:grid-cols-[minmax(0,1.35fr)_minmax(18rem,0.65fr)]">
        <div class="border border-base-300 bg-base-100 p-5 sm:p-6">
            {% if form.non_field_errors %}
                <div class="alert alert-error mb-5 py-2 text-sm" role="alert">
                    {% for error in form.non_field_errors %}<span>{{ error }}</span>{% endfor %}
                </div>
            {% endif %}

            {% if not has_participant_lists or not has_templates %}
                <div class="mb-6 border border-warning/40 bg-warning/10 p-4 text-sm text-base-content" role="status">
                    <p class="font-semibold">Completează datele necesare înainte de generare.</p>
                    <ul class="mt-2 list-inside list-disc space-y-1 text-muted">
                        {% if not has_participant_lists %}<li>Importă cel puțin o listă de participanți.</li>{% endif %}
                        {% if not has_templates %}<li>Creează cel puțin un template de diplomă.</li>{% endif %}
                    </ul>
                </div>
            {% endif %}

            <form method="post" class="space-y-5" data-generation-form>
                {% csrf_token %}
                <div class="form-control">
                    <label for="{{ form.participant_list.id_for_label }}" class="mb-1.5 text-sm font-semibold text-base-content">{{ form.participant_list.label }}</label>
                    {{ form.participant_list }}
                    {% for error in form.participant_list.errors %}<p class="mt-1 text-xs text-error">{{ error }}</p>{% endfor %}
                    <p class="mt-1.5 text-xs text-muted">Lista determină participanții disponibili în pasul următor.</p>
                </div>

                <div class="form-control">
                    <span id="generation-participant-label" class="mb-1.5 text-sm font-semibold text-base-content">{{ form.participant.label }}</span>
                    <div class="overflow-hidden border border-base-300 bg-base-100" role="group" aria-labelledby="generation-participant-label" data-participant-table>
                        <div class="flex items-center justify-between gap-3 border-b border-base-300 bg-base-200 px-3 py-2 text-xs text-muted">
                            <span>Selectează un singur participant</span>
                            <span>Selectați: <strong class="font-semibold text-base-content" data-participant-count>0</strong></span>
                        </div>
                        <div class="max-h-64 overflow-auto" data-participant-scroll>
                            <table class="table table-xs min-w-[46rem]">
                                <thead class="sticky top-0 z-10 bg-base-200 text-[0.68rem] uppercase tracking-wide text-muted">
                                    <tr>
                                        <th class="w-10 text-center">Alege</th>
                                        <th class="w-16">Nr.</th>
                                        <th>Nume complet</th>
                                        <th class="w-28">Data nașterii</th>
                                        <th>Locul nașterii</th>
                                        <th class="w-32">Nr. certificat</th>
                                    </tr>
                                </thead>
                                <tbody data-participant-rows>
                                    {% for participant in form.fields.participant.queryset %}
                                        <tr class="cursor-pointer border-base-300 hover:bg-base-200/70" data-participant-row data-participant-id="{{ participant.pk }}" data-participant-list-id="{{ participant.participant_list_id }}">
                                            <td class="text-center">
                                                <input type="radio" name="{{ form.participant.html_name }}" class="radio radio-primary radio-sm h-4 w-4" value="{{ participant.pk }}" aria-label="Selectează {{ participant.full_name }}" data-participant-checkbox {% if selected_participant_id == participant.pk|stringformat:"s" %}checked{% endif %}>
                                            </td>
                                            <td class="font-mono text-xs text-muted">{{ participant.source_row }}</td>
                                            <td class="max-w-56 truncate font-medium text-base-content" title="{{ participant.full_name }}">{{ participant.full_name }}</td>
                                            <td class="whitespace-nowrap">{{ participant.date_of_birth|date:"d.m.Y" }}</td>
                                            <td class="max-w-56 truncate" title="{{ participant.place_of_birth }}">{{ participant.place_of_birth }}</td>
                                            <td class="whitespace-nowrap font-mono text-xs">{{ participant.certificate_number }}</td>
                                        </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                        <p class="px-3 py-5 text-center text-sm text-muted" data-participant-empty hidden>Selectează mai întâi o listă cu participanți.</p>
                    </div>
                    {% for error in form.participant.errors %}<p class="mt-1 text-xs text-error">{{ error }}</p>{% endfor %}
                    <p class="mt-1.5 text-xs text-muted">PDF-ul va fi generat doar pentru participantul selectat.</p>
                </div>

                <div class="form-control">
                    <label for="{{ form.template.id_for_label }}" class="mb-1.5 text-sm font-semibold text-base-content">{{ form.template.label }}</label>
                    {{ form.template }}
                    {% for error in form.template.errors %}<p class="mt-1 text-xs text-error">{{ error }}</p>{% endfor %}
                    <p class="mt-1.5 text-xs text-muted">Previzualizarea folosește pozițiile și stilurile salvate în template.</p>
                </div>

                <div class="flex flex-col gap-3 border-t border-base-300 pt-5 sm:flex-row sm:items-center sm:justify-between">
                    <button type="submit" class="btn btn-primary btn-sm" {% if not has_participant_lists or not has_templates %}disabled{% endif %}>Previzualizează diploma</button>
                    <div class="flex flex-wrap gap-x-4 gap-y-2 text-sm">
                        <a href="{% url 'diplome:list_index' %}" class="link link-primary link-hover">Administrează liste</a>
                        <a href="{% url 'diplome:template_list' %}" class="link link-primary link-hover">Administrează template-uri</a>
                    </div>
                </div>
            </form>
        </div>

        <aside class="border border-base-300 bg-base-200 p-5 sm:p-6" aria-labelledby="generation-next-step">
            <div class="mx-auto flex aspect-210/297 w-full max-w-52 items-center justify-center border border-base-300 bg-base-100 shadow-sm" aria-hidden="true">
                <div class="w-3/4 space-y-4 text-center">
                    <div class="mx-auto h-1 w-1/3 bg-primary/30"></div>
                    <div class="mx-auto h-2 w-2/3 bg-primary/20"></div>
                    <div class="mx-auto h-px w-full bg-base-300"></div>
                    <div class="mx-auto h-1 w-1/2 bg-base-300"></div>
                    <div class="mx-auto h-1 w-2/3 bg-base-300"></div>
                </div>
            </div>
            <h2 id="generation-next-step" class="mt-6 text-lg font-semibold text-base-content">Pasul următor</h2>
            <p class="mt-2 text-sm leading-6 text-muted">Verifici diploma cu datele reale ale participantului, apoi generezi și descarci fișierul PDF.</p>
            <p class="mt-4 border-l-2 border-primary pl-3 text-xs leading-5 text-muted">O selecție generează o singură diplomă.</p>
        </aside>
    </div>

    <section class="border border-base-300 bg-base-100 p-5 sm:p-6" aria-labelledby="bulk-generation-title">
        <div class="grid gap-6 lg:grid-cols-[minmax(0,1fr)_18rem]">
            <div>
                <h2 id="bulk-generation-title" class="text-lg font-semibold text-primary">Generare pentru întreaga listă</h2>
                <p class="mt-1 text-sm text-muted">Se creează câte un PDF pentru fiecare participant și un lot disponibil ulterior în istoric.</p>

                {% if bulk_form.non_field_errors %}
                    <div class="alert alert-error mt-4 py-2 text-sm" role="alert">
                        {% for error in bulk_form.non_field_errors %}<span>{{ error }}</span>{% endfor %}
                    </div>
                {% endif %}

                <form method="post" action="{% url 'diplome:generation_bulk_create' %}" class="mt-5 grid gap-5 md:grid-cols-2">
                    {% csrf_token %}
                    <div class="form-control">
                        <label for="{{ bulk_form.participant_list.id_for_label }}" class="mb-1.5 text-sm font-semibold text-base-content">{{ bulk_form.participant_list.label }}</label>
                        {{ bulk_form.participant_list }}
                        {% for error in bulk_form.participant_list.errors %}<p class="mt-1 text-xs text-error">{{ error }}</p>{% endfor %}
                    </div>
                    <div class="form-control">
                        <label for="{{ bulk_form.template.id_for_label }}" class="mb-1.5 text-sm font-semibold text-base-content">{{ bulk_form.template.label }}</label>
                        {{ bulk_form.template }}
                        {% for error in bulk_form.template.errors %}<p class="mt-1 text-xs text-error">{{ error }}</p>{% endfor %}
                    </div>
                    <div class="md:col-span-2">
                        <button type="submit" class="btn btn-primary btn-sm" {% if not has_participant_lists or not has_templates %}disabled{% endif %}>Generează diplome pentru toată lista</button>
                    </div>
                </form>
            </div>
            <aside class="border-l-2 border-primary pl-4 text-sm text-muted">
                <p class="font-semibold text-base-content">Rezultatul lotului</p>
                <p class="mt-2 leading-6">După generare vei vedea numărul de fișiere reușite, eventualele erori și descărcarea ZIP.</p>
                <a href="{% url 'diplome:history_index' %}" class="link link-primary link-hover mt-3 inline-block">Deschide istoricul</a>
            </aside>
        </div>
    </section>
</section>
{% endblock %}

{% block page_scripts %}
<script src="{% static 'diplome/generation.js' %}" defer></script>
{% endblock %}
```

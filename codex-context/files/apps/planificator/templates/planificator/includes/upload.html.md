# apps/planificator/templates/planificator/includes/upload.html

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `apps/planificator/templates/planificator/includes/upload.html`
- App: `planificator`
- App guide: `codex-context/apps/planificator.md`
- Role: `template`
- Size: 4844 bytes
- Source SHA-256: `dafcfb83ef83792f95ac8fad42eba3d05a644bc29dcb8174f97a4a63f1370d46`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```html
<section id="generator-upload" class="card generator-step-card bg-base-100 shadow-none" data-generator-card="1">
    <div class="card-body gap-0 p-0">
        <header class="generator-card-header flex flex-col gap-3 bg-base-200 px-4 py-3 sm:flex-row sm:items-center sm:px-5">
            <div class="generator-card-step min-w-0 flex-1">
                <ul class="steps steps-vertical w-full text-xs font-semibold text-primary">
                    <li class="step {% if generation %}step-primary{% else %}step-secondary{% endif %}" data-generator-step="1" data-content="1">
                        <div class="generator-card-step-copy">
                            <h2 class="card-title text-base text-primary">Fișier sursă</h2>
                            <p class="mt-0.5 text-xs font-normal text-muted">Încarcă lista de cursuri în format CSV sau XLSX.</p>
                        </div>
                    </li>
                </ul>
            </div>
            {% if not history_read_only %}<a href="{% url 'planificator:generator_perioade_sample_csv' %}" class="btn btn-outline btn-secondary btn-sm self-start sm:self-auto">Descarcă modelul CSV</a>{% endif %}
        </header>

        <div class="p-4">
            <div class="sr-only">
                <label for="{{ form.input_file.id_for_label }}">Selectează fișierul</label>
                {{ form.input_file }}
            </div>

            <div id="ops-upload-dropzone" class="card card-border {% if not generation %}border-dashed{% endif %} border-base-300 bg-base-100 shadow-none">
                <label id="ops-upload-prompt" for="{{ form.input_file.id_for_label }}" class="card-body cursor-pointer items-center gap-1.5 px-4 py-6 text-center hover:bg-base-200 {% if generation %}hidden{% endif %}">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 16V4m0 0L7.5 8.5M12 4l4.5 4.5M5 15v3a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-3" />
                    </svg>
                    <span class="text-sm font-semibold text-base-content">Trage fișierul aici</span>
                    <span class="link link-primary text-sm font-semibold">sau alege de pe dispozitiv</span>
                    <span class="text-xs text-muted">CSV sau XLSX · maximum 20 MB</span>
                </label>

                <div id="ops-upload-state" class="card-body flex-col items-stretch justify-between gap-3 px-4 py-3 sm:flex-row sm:items-center {% if not generation %}hidden{% endif %}" aria-live="polite">
                    <div class="min-w-0">
                        <p id="ops-upload-file-name" class="truncate text-sm font-semibold text-primary">{{ uploaded_file_name }}</p>
                        <p id="ops-upload-status" class="text-xs text-muted">
                            {% if generation %}Fișier procesat · {{ source_course_count }} cursuri · SHA-256 {{ source_file_digest }}{% else %}Pregătit pentru validare{% endif %}
                        </p>
                    </div>
                    {% if not history_read_only %}<div class="card-actions flex-wrap sm:shrink-0">
                        <label id="ops-replace-upload" for="{{ form.input_file.id_for_label }}" class="btn btn-outline btn-primary btn-sm {% if not generation %}hidden{% endif %}">Alege alt fișier</label>
                        {% if generation %}<a id="ops-clear-processed-upload" href="{% url 'planificator:generator_perioade' %}" class="btn btn-outline btn-secondary btn-sm">Șterge fișierul</a>{% endif %}
                        <button type="button" id="ops-clear-upload" class="btn btn-outline btn-secondary btn-sm {% if generation %}hidden{% endif %}">Șterge fișierul</button>
                    </div>{% endif %}
                </div>
            </div>

            <p class="mt-2 text-xs text-muted">Coloane necesare: Title, Durata Curs, Permalink și, opțional, investitie.</p>
            <div id="ops-upload-warning" class="alert alert-warning mt-3 py-2 text-sm {% if not form.input_file.errors %}hidden{% endif %}" role="alert" aria-live="assertive">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M12 9v4m0 4h.01M10.3 4.4 2.8 17.5A1 1 0 0 0 3.7 19h16.6a1 1 0 0 0 .9-1.5L13.7 4.4a1 1 0 0 0-1.7 0Z" /></svg>
                <span id="ops-upload-warning-text">{% if form.input_file.errors %}{{ form.input_file.errors|join:", " }}{% else %}Selectează un fișier CSV sau XLSX pentru a continua.{% endif %}</span>
            </div>
        </div>
    </div>
</section>
```

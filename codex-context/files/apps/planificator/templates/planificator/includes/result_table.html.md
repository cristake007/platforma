# apps/planificator/templates/planificator/includes/result_table.html

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `apps/planificator/templates/planificator/includes/result_table.html`
- App: `planificator`
- App guide: `codex-context/apps/planificator.md`
- Role: `template`
- Size: 4847 bytes
- Source SHA-256: `63548cd80bf6bff8e32b72ea5f898c1561d94835fb584a65f022d2c905a23439`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```html
<section id="generator-result" class="card generator-step-card overflow-hidden bg-base-100 shadow-none" data-generator-card="3">
    <div class="card-body gap-0 p-0">
        <header class="generator-card-header flex flex-col gap-3 bg-base-200 px-4 py-3 sm:flex-row sm:items-center sm:px-5">
            <div class="generator-card-step min-w-0 flex-1">
                <ul class="steps steps-vertical w-full text-xs font-semibold text-primary">
                    <li class="step {% if generation %}step-secondary{% endif %}" data-generator-step="3" data-content="3">
                        <div class="generator-card-step-copy">
                            <h2 class="card-title text-base text-primary">Program generat</h2>
                            <p class="mt-0.5 text-xs font-normal text-muted">Fiecare curs primește o perioadă pentru fiecare lună selectată.</p>
                        </div>
                    </li>
                </ul>
            </div>
            {% if generation %}
                <button type="submit" form="export-form" class="btn btn-outline btn-primary btn-sm self-start sm:self-auto">
                    Descarcă XLSX
                </button>
            {% endif %}
        </header>
        {% if preview_rows %}
            <div id="ops-preview-table-wrap" class="max-h-[32rem] overflow-auto border-t border-base-300" tabindex="0" aria-label="Tabel generat; derulează pentru a vedea toate rândurile și coloanele">
                <table class="ops-schedule-table table table-zebra table-sm [--course-width:9rem] [--duration-width:4rem] [--investment-width:5rem] sm:[--course-width:16rem] sm:[--duration-width:6rem] sm:[--investment-width:7rem] lg:[--course-width:20rem] lg:[--duration-width:7rem]">
                    <caption class="sr-only">Perioadele generate pentru cursuri</caption>
                    <thead>
                        <tr>
                            <th scope="col" class="ops-schedule-course-column z-[4] bg-base-200">Curs</th>
                            <th scope="col" class="ops-schedule-duration-column z-[4] bg-base-200">Durată</th>
                            <th scope="col" class="ops-schedule-investment-column z-[4] bg-base-200">Investiție</th>
                            {% for month_name in selected_month_headers %}
                                <th scope="col" class="z-[3] whitespace-nowrap bg-base-200 text-center">
                                    {{ month_name }}
                                </th>
                            {% endfor %}
                        </tr>
                    </thead>
                    <tbody>
                        {% for row in preview_rows %}
                            <tr>
                                <th scope="row" class="ops-schedule-course-column z-[2] whitespace-normal break-words bg-base-100 text-left">
                                    {{ row.Title }}
                                </th>
                                <td class="ops-schedule-duration-column z-[2] whitespace-nowrap bg-base-100">
                                    {{ row.duration_label }}
                                </td>
                                <td class="ops-schedule-investment-column z-[2] whitespace-nowrap bg-base-100">
                                    {{ row.investitie|default:"-" }}
                                </td>
                                {% for value in row.months %}
                                    <td class="whitespace-nowrap text-center">{{ value }}</td>
                                {% endfor %}
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        {% else %}
            <div class="hero min-h-44 border-t border-base-300 bg-base-100" role="status">
                <div class="hero-content px-4 py-8 text-center">
                    <div class="max-w-lg">
                        <svg xmlns="http://www.w3.org/2000/svg" class="mx-auto h-9 w-9 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 5.5h16M4 10h16M4 14.5h16M8 5.5v13m8-13v13M5.5 19h13a1.5 1.5 0 0 0 1.5-1.5v-12A1.5 1.5 0 0 0 18.5 4h-13A1.5 1.5 0 0 0 4 5.5v12A1.5 1.5 0 0 0 5.5 19Z" />
                        </svg>
                        <h3 class="mt-3 text-base font-semibold text-primary">Programul este pregătit pentru generare</h3>
                        <p class="mt-1 text-sm text-muted">Încarcă fișierul, verifică setările și folosește butonul „Generează programul”. Rezultatele vor fi afișate în acest tabel.</p>
                    </div>
                </div>
            </div>
        {% endif %}
    </div>
</section>
```

# Source snapshot

## `apps/planificator/templates/planificator/includes/settings.html`

Size: 4.3 KB

```html
<section id="generator-settings" class="card generator-step-card bg-base-100 shadow-none" data-generator-card="2">
    <div class="card-body gap-0 p-0">
        <header class="generator-card-header bg-base-200 px-4 py-3 sm:px-5">
            <div class="generator-card-step min-w-0">
                <ul class="steps steps-vertical w-full text-xs font-semibold text-primary">
                    <li class="step {% if generation %}step-primary{% endif %}" data-generator-step="2" data-content="2">
                        <div class="generator-card-step-copy">
                            <h2 class="card-title text-base text-primary">Setări programare</h2>
                            <p class="mt-0.5 text-xs font-normal text-muted">Configurează anul, lunile, variația și zilele nelucrătoare.</p>
                        </div>
                    </li>
                </ul>
            </div>
        </header>

        <div class="space-y-4 p-4">
            <div class="grid gap-4 md:grid-cols-3 md:items-start">
                <fieldset class="fieldset text-center">
                    <legend class="fieldset-legend mx-auto">An</legend>
                    {{ form.year }}
                    {% if form.year.errors %}<p class="label text-error" role="alert">{{ form.year.errors|join:", " }}</p>{% endif %}
                </fieldset>
                <fieldset class="fieldset relative text-center">
                    <label class="fieldset-legend mx-auto" for="{{ form.randomness.id_for_label }}">Nivel de variație</label>
                    <span id="ops-randomness-value" class="badge badge-primary badge-outline badge-sm absolute right-0 top-0">{{ form.randomness.value }}</span>
                    {{ form.randomness }}
                    <div class="flex justify-between text-[11px] text-muted">
                        <span>Predictibil</span>
                        <span>Variat</span>
                    </div>
                    {% if form.randomness.errors %}<p class="label text-error" role="alert">{{ form.randomness.errors|join:", " }}</p>{% endif %}
                </fieldset>
                <fieldset class="fieldset text-center">
                    <legend class="fieldset-legend mx-auto">Zile nelucrătoare</legend>
                    <div class="join w-full" aria-label="Selectează data nelucrătoare">
                        <label class="sr-only" for="ops-holiday-date">Dată nelucrătoare</label>
                        <input type="date" id="ops-holiday-date" lang="ro" class="input input-primary input-sm join-item min-w-0 flex-1" aria-label="Dată nelucrătoare">
                        <button type="button" id="ops-add-holiday" class="btn btn-outline btn-primary btn-sm join-item">Adaugă</button>
                    </div>
                    <div id="ops-holiday-list" class="mt-1 flex flex-wrap justify-start gap-1.5"></div>
                    <div class="hidden">{{ form.holidays }}</div>
                    <p id="ops-holiday-live" class="sr-only" aria-live="polite"></p>
                    {% if form.holidays.errors %}<p class="label text-error" role="alert">{{ form.holidays.errors|join:", " }}</p>{% endif %}
                </fieldset>
            </div>

            <fieldset class="fieldset border-t border-base-300 pt-4">
                <div class="flex items-center justify-between gap-3">
                    <legend class="fieldset-legend">Luni incluse</legend>
                    <button type="button" id="ops-toggle-months" class="btn btn-outline btn-primary btn-sm">Selectează toate</button>
                </div>
                <div class="grid gap-2 sm:grid-cols-3 xl:grid-cols-6">
                    {% for checkbox in form.months %}
                        <label class="label cursor-pointer justify-start gap-2 rounded-field border border-base-300 bg-base-200 px-2 py-1.5 hover:border-primary hover:bg-base-100">
                            {{ checkbox.tag }}
                            <span class="text-xs">{{ checkbox.choice_label }}</span>
                        </label>
                    {% endfor %}
                </div>
                {% if form.months.errors %}<p class="label text-error" role="alert">{{ form.months.errors|join:", " }}</p>{% endif %}
            </fieldset>
        </div>

        {% include "planificator/includes/actions.html" %}
    </div>
</section>
```

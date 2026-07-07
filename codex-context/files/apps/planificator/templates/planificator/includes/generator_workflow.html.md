# Source snapshot

## `apps/planificator/templates/planificator/includes/generator_workflow.html`

Size: 2.3 KB

```html
<section id="generator-workflow" data-current-step="{% if generation %}3{% else %}1{% endif %}" class="mx-auto w-full max-w-[1360px] space-y-12" style="max-width:1360px">
    <div class="space-y-2">
        <div class="breadcrumbs p-0 text-sm text-muted">
            <ul>
                <li>Planificator</li>
                {% if history_read_only %}<li><a href="{% url 'planificator:istoric' %}">Istoric</a></li><li>Program generat</li>{% else %}<li>Generator perioade</li>{% endif %}
            </ul>
        </div>
        <div>
            <h1 class="text-xl font-bold text-primary sm:text-[1.75rem]">{% if history_read_only %}Program generat{% else %}Planifică seriile de curs{% endif %}</h1>
            <p class="mt-1 max-w-3xl text-sm text-muted">{% if history_read_only %}Vizualizare în mod citire a unei generări din istoric.{% else %}Încarcă oferta de cursuri, configurează programarea și verifică rezultatul.{% endif %}</p>
        </div>
    </div>

    {% if history_read_only %}
        <div class="alert alert-info py-2 text-sm" role="status">
            <span>Acest program este deschis din istoric. Fișierul sursă și setările nu pot fi modificate.</span>
        </div>
    {% endif %}

    {% include "planificator/includes/messages.html" %}

    <form
        id="generator-form"
        method="post"
        action="{% url 'planificator:generator_perioade' %}"
        enctype="multipart/form-data"
        class="space-y-5"
        hx-post="{% url 'planificator:generator_perioade' %}"
        hx-encoding="multipart/form-data"
        hx-target="#generator-workflow"
        hx-swap="outerHTML"
        hx-indicator="#ops-generator-loading"
    >
        {% csrf_token %}
        <fieldset class="contents"{% if history_read_only %} disabled aria-disabled="true"{% endif %}>
            <div class="space-y-12">
                {{ form.source_generation_id }}
                {% include "planificator/includes/upload.html" %}

                {% include "planificator/includes/settings.html" %}
            </div>
        </fieldset>
    </form>

    {% if generation %}
        <form id="export-form" method="post" action="{% url 'planificator:generator_perioade_export' %}">
            {% csrf_token %}
            {{ export_form.generation_id }}
        </form>
    {% endif %}

    {% include "planificator/includes/result_table.html" %}
</section>
```

# Source snapshot

## `apps/planificator/templates/planificator/istoric.html`

Size: 1.1 KB

```html
{% extends "layouts/base.html" %}

{% block title %}Istoric generări | Platforma TUVTK{% endblock %}

{% block content %}
    <section class="mx-auto w-full max-w-[1360px] space-y-5" style="max-width:1360px">
        <div class="space-y-2">
            <div class="breadcrumbs p-0 text-sm text-muted">
                <ul>
                    <li>Planificator</li>
                    <li>Istoric</li>
                </ul>
            </div>
            <div class="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
                <div>
                    <h1 class="text-xl font-bold text-primary sm:text-[1.75rem]">Istoric generări</h1>
                    <p class="mt-1 max-w-3xl text-sm text-muted">Consultă programele generate în ultimele 24 de ore și descarcă din nou fișierele XLSX.</p>
                </div>
                <a href="{% url 'planificator:generator_perioade' %}" class="btn btn-outline btn-primary btn-sm self-start sm:self-auto">Generează program nou</a>
            </div>
        </div>

        {% include "planificator/includes/history_list.html" %}
    </section>
{% endblock %}
```

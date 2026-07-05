# Source snapshot

## `apps/diplome/templates/diplome/participant_import_sheet.html`

Size: 1.8 KB

```html
{% extends "layouts/base.html" %}

{% block title %}Selectare foaie XLSX | Platforma TUVTK{% endblock %}

{% block content %}
<section class="mx-auto w-full max-w-2xl space-y-6">
    <div class="space-y-2">
        <div class="breadcrumbs p-0 text-sm text-muted"><ul><li>Diplome</li><li><a href="{% url 'diplome:list_index' %}">Liste participanți</a></li><li>Selectare foaie</li></ul></div>
        <div>
            <h1 class="text-2xl font-bold text-primary">Alege foaia de importat</h1>
            <p class="mt-1 text-sm text-muted">Fișierul {{ draft.source_file_name }} conține mai multe foi cu date. Va fi importată numai foaia selectată.</p>
        </div>
    </div>

    <form method="post" class="space-y-5 border border-base-300 bg-base-100 p-6">
        {% csrf_token %}
        <fieldset class="space-y-3">
            <legend class="text-sm font-semibold text-base-content">Foi disponibile</legend>
            {% for choice in form.sheet_index %}
                <label class="flex cursor-pointer items-center gap-3 border border-base-300 bg-base-100 p-4 transition-colors hover:bg-base-200/50">
                    {{ choice.tag }}
                    <span class="text-sm text-base-content">{{ choice.choice_label }}</span>
                </label>
            {% endfor %}
            {% for error in form.sheet_index.errors %}<p class="text-sm text-error" role="alert">{{ error }}</p>{% endfor %}
        </fieldset>
        <div class="flex justify-end gap-2 border-t border-base-300 pt-5">
            <a href="{% url 'diplome:participant_import' %}" class="btn btn-ghost btn-sm">Încarcă alt fișier</a>
            <button type="submit" class="btn btn-primary btn-sm">Continuă la asocierea coloanelor</button>
        </div>
    </form>
</section>
{% endblock %}
```

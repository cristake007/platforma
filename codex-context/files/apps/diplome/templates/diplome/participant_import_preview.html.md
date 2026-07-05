# Source snapshot

## `apps/diplome/templates/diplome/participant_import_preview.html`

Size: 3.5 KB

```html
{% extends "layouts/base.html" %}

{% block title %}Verificare import | Platforma TUVTK{% endblock %}

{% block content %}
<section class="mx-auto w-full max-w-7xl space-y-6">
    <div class="space-y-2">
        <div class="breadcrumbs p-0 text-sm text-muted"><ul><li>Diplome</li><li><a href="{% url 'diplome:list_index' %}">Liste participanți</a></li><li>Verificare import</li></ul></div>
        <div>
            <h1 class="text-2xl font-bold text-primary">Verifică lista „{{ draft.list_name }}”</h1>
            <p class="mt-1 text-sm text-muted">{{ draft.source_file_name }} · {{ draft.valid_rows_json|length }} rânduri valide · {{ draft.invalid_rows_json|length }} rânduri invalide</p>
        </div>
    </div>

    {% if messages %}{% for message in messages %}<div class="alert alert-error py-2 text-sm" role="alert"><span>{{ message }}</span></div>{% endfor %}{% endif %}
    {% if draft.warnings_json %}
        <div class="alert alert-warning items-start py-3 text-sm" role="status">
            <div><p class="font-semibold">Avertismente</p><ul class="mt-1 list-disc pl-5">{% for warning in draft.warnings_json %}<li>{{ warning }}</li>{% endfor %}</ul></div>
        </div>
    {% endif %}

    {% if draft.invalid_rows_json %}
        <div class="space-y-2">
            <h2 class="text-lg font-semibold text-error">Rânduri invalide</h2>
            <div class="overflow-x-auto border border-error/30 bg-base-100">
                <table class="table table-sm">
                    <thead class="bg-error/10"><tr><th>Rând</th><th>Nume complet</th><th>Data nașterii</th><th>Locul nașterii</th><th>Număr certificat</th><th>Erori</th></tr></thead>
                    <tbody>{% for row in draft.invalid_rows_json %}<tr><td>{{ row.source_row }}</td><td>{{ row.full_name|default:"—" }}</td><td>{{ row.date_of_birth|default:"—" }}</td><td>{{ row.place_of_birth|default:"—" }}</td><td>{{ row.certificate_number|default:"—" }}</td><td class="text-error">{{ row.errors|join:" " }}</td></tr>{% endfor %}</tbody>
                </table>
            </div>
        </div>
    {% endif %}

    <div class="space-y-2">
        <h2 class="text-lg font-semibold text-base-content">Rânduri valide</h2>
        <div class="overflow-x-auto border border-base-300 bg-base-100">
            {% if draft.valid_rows_json %}
                <table class="table table-sm">
                    <thead class="bg-base-200"><tr><th>Rând</th><th>Nume complet</th><th>Data nașterii</th><th>Locul nașterii</th><th>Număr certificat</th></tr></thead>
                    <tbody>{% for row in draft.valid_rows_json %}<tr><td>{{ row.source_row }}</td><td class="font-medium">{{ row.full_name }}</td><td>{{ row.date_of_birth }}</td><td>{{ row.place_of_birth }}</td><td>{{ row.certificate_number }}</td></tr>{% endfor %}</tbody>
                </table>
            {% else %}
                <p class="px-5 py-8 text-center text-sm text-muted">Nu există rânduri valide pentru import.</p>
            {% endif %}
        </div>
    </div>

    <div class="flex justify-end gap-2 border-t border-base-300 pt-5">
        <a href="{% url 'diplome:participant_import' %}" class="btn btn-ghost btn-sm">Încarcă alt fișier</a>
        <form method="post" action="{% url 'diplome:participant_import_confirm' draft.pk %}">
            {% csrf_token %}
            <button type="submit" class="btn btn-primary btn-sm" {% if not draft.valid_rows_json %}disabled{% endif %}>Confirmă importul</button>
        </form>
    </div>
</section>
{% endblock %}
```

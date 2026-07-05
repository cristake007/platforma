# apps/diplome/templates/diplome/template_list.html

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `apps/diplome/templates/diplome/template_list.html`
- App: `diplome`
- App guide: `codex-context/apps/diplome.md`
- Role: `template`
- Size: 5352 bytes
- Source SHA-256: `0cc21f07a50ba06b02d36349c5485b66df4e3d2e732b6fa875935748e8cbd3d9`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```html
{% extends "layouts/base.html" %}

{% block title %}Template-uri diplome | Platforma TUVTK{% endblock %}

{% block content %}
<section class="mx-auto w-full max-w-6xl space-y-6">
    <div class="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div class="space-y-2">
            <div class="breadcrumbs p-0 text-sm text-muted">
                <ul><li>Diplome</li><li>Template-uri</li></ul>
            </div>
            <div>
                <h1 class="text-2xl font-bold text-primary">Template-uri diplome</h1>
                <p class="mt-1 text-sm text-muted">Creează și administrează machetele vizuale folosite pentru diplome.</p>
            </div>
        </div>
        <a href="{% url 'diplome:template_create' %}" class="btn btn-primary btn-sm">Template nou</a>
    </div>

    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-success py-2 text-sm" role="status"><span>{{ message }}</span></div>
        {% endfor %}
    {% endif %}

    <form method="get" class="flex flex-col gap-3 border border-base-300 bg-base-100 p-4 sm:flex-row sm:items-end">
        <label class="form-control">
            <span class="label-text mb-1 text-xs font-semibold uppercase tracking-wide text-muted">Categorie</span>
            {{ filter_form.category }}
        </label>
        <div class="flex items-center gap-2">
            <button type="submit" class="btn btn-primary btn-sm">Filtrează</button>
            {% if selected_category %}
                <a href="{% url 'diplome:template_list' %}" class="btn btn-ghost btn-sm">Șterge filtrul</a>
            {% endif %}
        </div>
    </form>

    <div class="overflow-hidden border border-base-300 bg-base-100">
        {% if templates %}
            <div class="overflow-x-auto">
                <table class="table table-sm">
                    <thead class="bg-base-200 text-xs uppercase tracking-wide text-muted">
                        <tr>
                            <th>Nume</th>
                            <th>Categorie</th>
                            <th>Format</th>
                            <th>Stare</th>
                            <th>Actualizat</th>
                            <th class="text-right">Acțiuni</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for diploma_template in templates %}
                            <tr>
                                <td>
                                    <p class="font-semibold text-base-content">{{ diploma_template.name }}</p>
                                    {% if diploma_template.description %}<p class="mt-0.5 max-w-xl text-xs text-muted">{{ diploma_template.description }}</p>{% endif %}
                                </td>
                                <td><span class="badge badge-outline badge-sm">{{ diploma_template.category }}</span></td>
                                <td>{{ diploma_template.page_size }} · {{ diploma_template.get_orientation_display }}</td>
                                <td>{% if diploma_template.is_active %}<span class="text-success">Activ</span>{% else %}<span class="text-muted">Inactiv</span>{% endif %}</td>
                                <td>{{ diploma_template.updated_at|date:"d.m.Y H:i" }}</td>
                                <td>
                                    <div class="flex justify-end gap-2">
                                        <a href="{% url 'diplome:template_editor' diploma_template.pk %}" class="btn btn-outline btn-primary btn-xs">Editează</a>
                                        <a href="{% url 'diplome:template_preview' diploma_template.pk %}" class="btn btn-ghost btn-xs" target="_blank" rel="noopener">Preview</a>
                                        <form method="post" action="{% url 'diplome:template_delete' diploma_template.pk %}">
                                            {% csrf_token %}
                                            <button type="submit" class="btn btn-ghost btn-xs text-error">Șterge</button>
                                        </form>
                                    </div>
                                </td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        {% else %}
            <div class="px-6 py-14 text-center">
                {% if selected_category %}
                    <h2 class="text-lg font-semibold text-base-content">Niciun template în categoria „{{ selected_category }}”</h2>
                    <p class="mt-2 text-sm text-muted">Alege o altă categorie sau elimină filtrul curent.</p>
                    <a href="{% url 'diplome:template_list' %}" class="btn btn-outline btn-primary btn-sm mt-5">Afișează toate template-urile</a>
                {% else %}
                    <h2 class="text-lg font-semibold text-base-content">Nu există template-uri</h2>
                    <p class="mt-2 text-sm text-muted">Creează primul template și configurează-l în editorul vizual.</p>
                    <a href="{% url 'diplome:template_create' %}" class="btn btn-primary btn-sm mt-5">Creează primul template</a>
                {% endif %}
            </div>
        {% endif %}
    </div>
</section>
{% endblock %}
```

# apps/diplome/templates/diplome/history_index.html

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `apps/diplome/templates/diplome/history_index.html`
- App: `diplome`
- App guide: `codex-context/apps/diplome.md`
- Role: `template`
- Size: 7078 bytes
- Source SHA-256: `724645a83ab345c06b6e9ea689162bcfc7b606a532faf73b801d8352c6b65f9e`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```html
{% extends "layouts/base.html" %}

{% block title %}Istoric generări | Platforma TUVTK{% endblock %}

{% block content %}
<section class="mx-auto w-full max-w-7xl space-y-6">
    <header class="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div class="space-y-2">
            <div class="breadcrumbs p-0 text-sm text-muted">
                <ul><li>Diplome</li><li>Istoric</li></ul>
            </div>
            <div>
                <h1 class="text-2xl font-bold text-primary">Istoric generări</h1>
                <p class="mt-1 text-sm text-muted">Loturile de diplome generate, ordonate de la cel mai recent.</p>
            </div>
        </div>
        <a href="{% url 'diplome:generation_index' %}" class="btn btn-primary btn-sm">Generare nouă</a>
    </header>

    <form method="get" class="grid gap-3 border border-base-300 bg-base-100 p-4 sm:grid-cols-2 lg:grid-cols-5">
        <div>
            <label for="{{ filter_form.participant_list.id_for_label }}" class="mb-1 block text-xs font-semibold text-muted">{{ filter_form.participant_list.label }}</label>
            {{ filter_form.participant_list }}
        </div>
        <div>
            <label for="{{ filter_form.template.id_for_label }}" class="mb-1 block text-xs font-semibold text-muted">{{ filter_form.template.label }}</label>
            {{ filter_form.template }}
        </div>
        <div>
            <label for="{{ filter_form.status.id_for_label }}" class="mb-1 block text-xs font-semibold text-muted">{{ filter_form.status.label }}</label>
            {{ filter_form.status }}
        </div>
        <div>
            <label for="{{ filter_form.date.id_for_label }}" class="mb-1 block text-xs font-semibold text-muted">{{ filter_form.date.label }}</label>
            {{ filter_form.date }}
        </div>
        <div class="flex items-end gap-2">
            <button type="submit" class="btn btn-primary btn-sm">Filtrează</button>
            <a href="{% url 'diplome:history_index' %}" class="btn btn-ghost btn-sm">Resetează</a>
        </div>
    </form>

    <div class="overflow-x-auto border border-base-300 bg-base-100">
        <table class="table table-xs">
            <thead>
                <tr>
                    <th>Listă</th>
                    <th>Template</th>
                    <th>Status</th>
                    <th class="text-right">Reușite</th>
                    <th class="text-right">Erori</th>
                    <th>Creat</th>
                    <th class="text-right">Acțiuni</th>
                </tr>
            </thead>
            <tbody>
                {% for batch in batches %}
                    <tr>
                        <td class="font-medium text-base-content">{{ batch.participant_list_display_name }}</td>
                        <td>{{ batch.template_display_name }}</td>
                        <td>
                            <span class="badge badge-sm {% if batch.status == 'completed' %}badge-success{% elif batch.status == 'completed_with_errors' %}badge-warning{% elif batch.status == 'failed' %}badge-error{% else %}badge-ghost{% endif %}">{{ batch.get_status_display }}</span>
                        </td>
                        <td class="text-right">{{ batch.success_count }}/{{ batch.total_count }}</td>
                        <td class="text-right">{{ batch.failed_count }}</td>
                        <td class="whitespace-nowrap">{{ batch.created_at|date:"d.m.Y H:i" }}</td>
                        <td>
                            <div class="flex justify-end gap-1">
                                {% if batch.status == 'pending' %}
                                    <form method="post" action="{% url 'diplome:batch_resume' batch.pk %}" class="inline-flex">
                                        {% csrf_token %}
                                        <button
                                            type="submit"
                                            class="btn btn-square btn-ghost btn-xs text-primary hover:bg-primary/10"
                                            aria-label="Reia generarea lotului"
                                            title="Reia generarea lotului"
                                        >
                                            <svg xmlns="http://www.w3.org/2000/svg" class="size-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M8.25 6.75v-3m0 0h-3m3 0L5.6 6.4a7.5 7.5 0 1 0 2.15-1.45M10 8.75l5 3.25-5 3.25v-6.5Z" />
                                            </svg>
                                        </button>
                                    </form>
                                {% endif %}
                                <a
                                    href="{% url 'diplome:batch_detail' batch.pk %}"
                                    class="btn btn-square btn-ghost btn-xs text-primary hover:bg-primary/10"
                                    aria-label="Vezi detaliile lotului"
                                    title="Vezi detaliile lotului"
                                >
                                    <svg xmlns="http://www.w3.org/2000/svg" class="size-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M14 3.75H6.75A1.75 1.75 0 0 0 5 5.5v13A1.75 1.75 0 0 0 6.75 20.25h6.5M14 3.75v4.5h4.5M14 3.75l4.5 4.5v3.25M17.25 14.25a3 3 0 1 0 0 6 3 3 0 0 0 0-6Zm2.15 5.15 2.1 2.1" />
                                    </svg>
                                </a>
                                {% if batch.success_count %}
                                    <a
                                        href="{% url 'diplome:batch_zip_download' batch.pk %}"
                                        class="btn btn-square btn-ghost btn-xs text-success hover:bg-success/10"
                                        aria-label="Descarcă lotul ca arhivă ZIP"
                                        title="Descarcă lotul ca arhivă ZIP"
                                    >
                                        <svg xmlns="http://www.w3.org/2000/svg" class="size-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M12 3.75v11.5m0 0 4-4m-4 4-4-4M5 19.25h14" />
                                        </svg>
                                    </a>
                                {% endif %}
                            </div>
                        </td>
                    </tr>
                {% empty %}
                    <tr><td colspan="7" class="py-10 text-center text-muted">Nu există loturi pentru filtrele selectate.</td></tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</section>
{% endblock %}
```

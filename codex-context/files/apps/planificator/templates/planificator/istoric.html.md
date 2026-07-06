# Source snapshot

## `apps/planificator/templates/planificator/istoric.html`

Size: 8.3 KB

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

        <section class="card generator-step-card bg-base-100 shadow-none" aria-labelledby="history-list-title">
            <header class="generator-card-header bg-base-200 px-4 py-4 sm:px-5">
                <h2 id="history-list-title" class="text-base font-semibold text-primary">Programe disponibile</h2>
                <p class="mt-1 text-xs text-muted">Fișierele expirate nu mai pot fi descărcate și sunt eliminate automat.</p>
            </header>

            {% if generations %}
                <div class="divide-y divide-base-300 md:hidden">
                    {% for generation in generations %}
                        <article class="space-y-3 p-4">
                            <div>
                                <a href="{% url 'planificator:istoric_detail' generation.pk %}" class="link link-primary font-semibold">{{ generation.source_file_name }}</a>
                                <span class="mt-0.5 block font-mono text-[11px] text-muted">SHA-256 {{ generation.source_file_digest|slice:":12" }}</span>
                            </div>
                            <dl class="grid grid-cols-2 gap-x-4 gap-y-2 text-sm">
                                <div><dt class="text-xs text-muted">An</dt><dd class="font-semibold">{{ generation.year }}</dd></div>
                                <div><dt class="text-xs text-muted">Luni</dt><dd class="font-semibold">{{ generation.selected_months|join:", " }}</dd></div>
                                <div><dt class="text-xs text-muted">Cursuri</dt><dd class="font-semibold">{{ generation.source_course_count }}</dd></div>
                                <div><dt class="text-xs text-muted">Perioade</dt><dd class="font-semibold">{{ generation.generated_entry_count }}</dd></div>
                                <div><dt class="text-xs text-muted">Generat</dt><dd>{{ generation.created_at|date:"d.m.Y H:i" }}</dd></div>
                                <div><dt class="text-xs text-muted">Expiră</dt><dd>{{ generation.expires_at|date:"d.m.Y H:i" }}</dd></div>
                            </dl>
                            <div class="flex flex-wrap gap-2">
                                <a href="{% url 'planificator:istoric_detail' generation.pk %}" class="btn btn-outline btn-primary btn-sm">Vezi</a>
                                <form method="post" action="{% url 'planificator:generator_perioade_export' %}">
                                    {% csrf_token %}
                                    <input type="hidden" name="generation_id" value="{{ generation.pk }}">
                                    <button type="submit" class="btn btn-outline btn-secondary btn-sm">Descarcă XLSX</button>
                                </form>
                            </div>
                        </article>
                    {% endfor %}
                </div>

                <div class="hidden overflow-x-auto md:block">
                    <table class="table table-sm">
                        <thead>
                            <tr>
                                <th scope="col">Fișier sursă</th>
                                <th scope="col">An</th>
                                <th scope="col">Luni</th>
                                <th scope="col">Cursuri</th>
                                <th scope="col">Perioade</th>
                                <th scope="col">Generat</th>
                                <th scope="col">Expiră</th>
                                <th scope="col" class="text-right">Acțiuni</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for generation in generations %}
                                <tr>
                                    <th scope="row" class="min-w-48">
                                        <a href="{% url 'planificator:istoric_detail' generation.pk %}" class="link link-primary font-semibold">{{ generation.source_file_name }}</a>
                                        <span class="mt-0.5 block font-mono text-[11px] font-normal text-muted">SHA-256 {{ generation.source_file_digest|slice:":12" }}</span>
                                    </th>
                                    <td>{{ generation.year }}</td>
                                    <td>{{ generation.selected_months|join:", " }}</td>
                                    <td>{{ generation.source_course_count }}</td>
                                    <td>{{ generation.generated_entry_count }}</td>
                                    <td class="whitespace-nowrap">{{ generation.created_at|date:"d.m.Y H:i" }}</td>
                                    <td class="whitespace-nowrap">{{ generation.expires_at|date:"d.m.Y H:i" }}</td>
                                    <td>
                                        <div class="flex justify-end gap-2">
                                            <a href="{% url 'planificator:istoric_detail' generation.pk %}" class="btn btn-outline btn-primary btn-sm">Vezi</a>
                                            <form method="post" action="{% url 'planificator:generator_perioade_export' %}">
                                                {% csrf_token %}
                                                <input type="hidden" name="generation_id" value="{{ generation.pk }}">
                                                <button type="submit" class="btn btn-outline btn-secondary btn-sm">Descarcă XLSX</button>
                                            </form>
                                        </div>
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <div class="px-4 py-12 text-center sm:px-6">
                    <svg xmlns="http://www.w3.org/2000/svg" class="mx-auto h-10 w-10 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 6.5h16M6.5 3.5v3m11-3v3M5.5 20.5h13a1.5 1.5 0 0 0 1.5-1.5V6.5H4V19a1.5 1.5 0 0 0 1.5 1.5Zm2.5-10h3v3H8v-3Z" /></svg>
                    <h3 class="mt-3 text-base font-semibold text-primary">Nu există programe disponibile</h3>
                    <p class="mx-auto mt-1 max-w-md text-sm text-muted">Generează primul program pentru a-l putea consulta și descărca de aici.</p>
                    <a href="{% url 'planificator:generator_perioade' %}" class="btn btn-outline btn-primary btn-sm mt-4">Deschide generatorul</a>
                </div>
            {% endif %}
        </section>

        {% if is_paginated %}
            <nav class="flex items-center justify-between gap-3" aria-label="Paginare istoric">
                {% if page_obj.has_previous %}<a href="?page={{ page_obj.previous_page_number }}" class="btn btn-outline btn-primary btn-sm">Pagina anterioară</a>{% else %}<span></span>{% endif %}
                <span class="text-sm text-muted">Pagina {{ page_obj.number }} din {{ page_obj.paginator.num_pages }}</span>
                {% if page_obj.has_next %}<a href="?page={{ page_obj.next_page_number }}" class="btn btn-outline btn-primary btn-sm">Pagina următoare</a>{% else %}<span></span>{% endif %}
            </nav>
        {% endif %}
    </section>
{% endblock %}
```

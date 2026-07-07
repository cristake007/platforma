# Source snapshot

## `apps/diplome/templates/diplome/includes/participant_list_panel.html`

Size: 5.3 KB

```html
<div id="participant-list-panel" class="space-y-4">
    {% include "diplome/includes/messages.html" %}

    <div class="relative overflow-hidden border border-base-300 bg-base-100" aria-live="polite">
        <div
            id="participant-list-loading"
            class="htmx-indicator absolute inset-0 z-10 flex items-center justify-center bg-base-100/80"
            role="status"
        >
            <span class="inline-flex items-center gap-3 border border-base-300 bg-base-100 px-4 py-3 text-sm font-medium text-base-content shadow-sm">
                <span class="loading loading-spinner loading-md text-primary" aria-hidden="true"></span>
                Se actualizează listele
            </span>
        </div>
        {% if participant_lists %}
            <div class="overflow-x-auto">
                <table class="table table-sm">
                    <thead class="bg-base-200 text-xs uppercase tracking-wide text-muted">
                        <tr><th>Listă</th><th>Curs</th><th>Participanți</th><th>Fișier sursă</th><th>Creată</th><th class="text-right">Acțiuni</th></tr>
                    </thead>
                    <tbody>
                        {% for participant_list in participant_lists %}
                            <tr>
                                <td>
                                    <a href="{% url 'diplome:participant_list_detail' participant_list.pk %}" class="font-semibold text-primary hover:underline">{{ participant_list.name }}</a>
                                    {% if participant_list.description %}<p class="mt-0.5 max-w-lg text-xs text-muted">{{ participant_list.description }}</p>{% endif %}
                                </td>
                                <td>{{ participant_list.course_name|default:"—" }}</td>
                                <td>{{ participant_list.participant_count }}</td>
                                <td>{{ participant_list.source_file_name }}</td>
                                <td class="whitespace-nowrap">{{ participant_list.created_at|date:"d.m.Y H:i" }}</td>
                                <td>
                                    <div class="flex justify-end gap-2">
                                        <a href="{% url 'diplome:participant_list_detail' participant_list.pk %}" class="btn btn-outline btn-primary btn-xs">Deschide</a>
                                        <form
                                            method="post"
                                            action="{% url 'diplome:participant_list_delete' participant_list.pk %}{% if request.GET.urlencode %}?{{ request.GET.urlencode }}{% endif %}"
                                            hx-post="{% url 'diplome:participant_list_delete' participant_list.pk %}{% if request.GET.urlencode %}?{{ request.GET.urlencode }}{% endif %}"
                                            hx-target="#participant-list-panel"
                                            hx-swap="outerHTML show:top"
                                            hx-confirm="Ștergi această listă de participanți?"
                                        >
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
                <h2 class="text-lg font-semibold text-base-content">Nu există liste de participanți</h2>
                <p class="mt-2 text-sm text-muted">Importă un fișier CSV sau XLSX pentru a crea prima listă.</p>
                <a href="{% url 'diplome:participant_import' %}" class="btn btn-primary btn-sm mt-5">Importă prima listă</a>
            </div>
        {% endif %}
    </div>
    {% if is_paginated %}
        <nav class="flex items-center justify-between text-sm" aria-label="Paginare liste participanți">
            <span class="text-muted">Pagina {{ page_obj.number }} din {{ page_obj.paginator.num_pages }}</span>
            <div class="join">
                {% if page_obj.has_previous %}
                    <a
                        href="?page={{ page_obj.previous_page_number }}"
                        class="btn btn-sm join-item"
                        hx-get="?page={{ page_obj.previous_page_number }}"
                        hx-target="#participant-list-panel"
                        hx-swap="outerHTML show:top"
                        hx-push-url="true"
                        hx-indicator="#participant-list-loading"
                    >Anterior</a>
                {% endif %}
                {% if page_obj.has_next %}
                    <a
                        href="?page={{ page_obj.next_page_number }}"
                        class="btn btn-sm join-item"
                        hx-get="?page={{ page_obj.next_page_number }}"
                        hx-target="#participant-list-panel"
                        hx-swap="outerHTML show:top"
                        hx-push-url="true"
                        hx-indicator="#participant-list-loading"
                    >Următor</a>
                {% endif %}
            </div>
        </nav>
    {% endif %}
</div>
```

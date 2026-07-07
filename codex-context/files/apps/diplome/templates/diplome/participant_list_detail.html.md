# Source snapshot

## `apps/diplome/templates/diplome/participant_list_detail.html`

Size: 1.4 KB

```html
{% extends "layouts/base.html" %}

{% block title %}{{ participant_list.name }} | Platforma TUVTK{% endblock %}

{% block content %}
<section class="mx-auto w-full max-w-7xl space-y-6">
    <div class="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div class="space-y-2">
            <div class="breadcrumbs p-0 text-sm text-muted"><ul><li>Diplome</li><li><a href="{% url 'diplome:list_index' %}">Liste participanți</a></li><li>{{ participant_list.name }}</li></ul></div>
            <div>
                <h1 class="text-2xl font-bold text-primary">{{ participant_list.name }}</h1>
                {% if participant_list.description %}<p class="mt-1 text-sm text-muted">{{ participant_list.description }}</p>{% endif %}
                <p class="mt-2 text-xs text-muted">{% if participant_list.course_name %}Curs: {{ participant_list.course_name }} · {% endif %}Fișier: {{ participant_list.source_file_name }} · {{ participant_list.participant_count }} participanți</p>
            </div>
        </div>
        <form method="post" action="{% url 'diplome:participant_list_delete' participant_list.pk %}">
            {% csrf_token %}
            <button type="submit" class="btn btn-outline btn-error btn-sm">Șterge lista</button>
        </form>
    </div>

    {% include "diplome/includes/participant_list_detail_panel.html" %}
</section>
{% endblock %}
```

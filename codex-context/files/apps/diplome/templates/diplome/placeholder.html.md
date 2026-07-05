# Source snapshot

## `apps/diplome/templates/diplome/placeholder.html`

Size: 687 B

```html
{% extends "layouts/base.html" %}

{% block title %}{{ page_title }} | Platforma TUVTK{% endblock %}

{% block content %}
<section class="mx-auto w-full max-w-4xl space-y-5">
    <div class="breadcrumbs p-0 text-sm text-muted"><ul><li>Diplome</li><li>{{ page_title }}</li></ul></div>
    <div class="border border-base-300 bg-base-100 px-6 py-12 text-center">
        <h1 class="text-2xl font-bold text-primary">{{ page_title }}</h1>
        <p class="mx-auto mt-3 max-w-2xl text-sm text-muted">{{ page_description }}</p>
        <a href="{% url 'diplome:template_list' %}" class="btn btn-outline btn-primary btn-sm mt-6">Deschide template-urile</a>
    </div>
</section>
{% endblock %}
```

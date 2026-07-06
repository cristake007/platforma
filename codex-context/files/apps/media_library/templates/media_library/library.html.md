# Source snapshot

## `apps/media_library/templates/media_library/library.html`

Size: 800 B

```html
{% extends "layouts/base.html" %}
{% load static %}

{% block title %}Bibliotecă media | Platforma TUVTK{% endblock %}

{% block page_styles %}
<link rel="stylesheet" href="{% static 'media_library/library.css' %}">
{% endblock %}

{% block content %}
<section class="mx-auto w-full max-w-7xl space-y-6">
    <header class="space-y-2">
        <div class="breadcrumbs p-0 text-sm text-muted"><ul><li>Operațiuni</li><li>Bibliotecă media</li></ul></div>
        <div>
            <h1 class="text-2xl font-bold text-primary">Bibliotecă media</h1>
            <p class="mt-1 text-sm text-muted">Încarcă o singură dată imagini reutilizabile în template-urile de diplomă.</p>
        </div>
    </header>

    {% include "media_library/includes/library_content.html" %}
</section>
{% endblock %}
```

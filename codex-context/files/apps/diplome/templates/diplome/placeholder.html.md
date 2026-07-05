# apps/diplome/templates/diplome/placeholder.html

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `apps/diplome/templates/diplome/placeholder.html`
- App: `diplome`
- App guide: `codex-context/apps/diplome.md`
- Role: `template`
- Size: 687 bytes
- Source SHA-256: `ea5864d50b38ce0b8403f308f98aeaa35d47ff955a1389255be5d8b319e514e3`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

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

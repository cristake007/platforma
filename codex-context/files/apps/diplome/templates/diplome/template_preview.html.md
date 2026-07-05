# apps/diplome/templates/diplome/template_preview.html

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `apps/diplome/templates/diplome/template_preview.html`
- App: `diplome`
- App guide: `codex-context/apps/diplome.md`
- Role: `template`
- Size: 1559 bytes
- Source SHA-256: `8ac16dea92aaa51307a08702cb8da63079ff83cb51dce0b96226f77280f1ee80`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```html
{% extends "layouts/base.html" %}
{% load static %}

{% block title %}Preview {{ diploma_template.name }} | Platforma TUVTK{% endblock %}

{% block page_styles %}
<link rel="stylesheet" href="{% static 'diplome/template_editor.css' %}">
{% endblock %}

{% block content %}
<section id="diploma-preview" class="diploma-preview-page" data-sidebar-start-collapsed="true">
    <header class="preview-heading">
        <div>
            <div class="breadcrumbs p-0 text-xs text-muted">
                <ul><li>Diplome</li><li><a href="{% url 'diplome:template_list' %}">Template-uri</a></li><li>Preview</li></ul>
            </div>
            <h1>Previzualizare diplomă</h1>
            <p>{{ diploma_template.name }} · date demonstrative</p>
        </div>
        <a href="{% url 'diplome:template_editor' diploma_template.pk %}" class="btn btn-outline btn-primary btn-sm">Înapoi la editor</a>
    </header>
    <div class="preview-workspace">
        <div class="preview-canvas-frame" id="preview-canvas-frame">
            <div class="diploma-canvas preview-canvas" id="preview-canvas" aria-label="Previzualizare template diplomă"></div>
        </div>
    </div>
    {{ layout|json_script:"diploma-layout-data" }}
    {{ sample_participant|json_script:"diploma-sample-data" }}
    {{ media_assets|json_script:"diploma-media-assets-data" }}
</section>
{% endblock %}

{% block page_scripts %}
<script src="{% static 'diplome/template_renderer.js' %}" defer></script>
<script src="{% static 'diplome/template_preview.js' %}" defer></script>
{% endblock %}
```

# apps/diplome/templates/diplome/template_preview.html

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `apps/diplome/templates/diplome/template_preview.html`
- App: `diplome`
- App guide: `codex-context/apps/diplome.md`
- Role: `template`
- Size: 1577 bytes
- Source SHA-256: `101d4ab945a312b352961ff2f5e55e2d40c115649561701bf2a64618b4ae1e49`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```html
{% extends "layouts/base.html" %}
{% load static %}

{% block title %}Preview {{ diploma_template.name }} | Platforma TUVTK{% endblock %}
{% block sidebar_start_collapsed %}true{% endblock %}

{% block page_styles %}
<link rel="stylesheet" href="{% static 'diplome/template_editor.css' %}">
{% endblock %}

{% block content %}
<section id="diploma-preview" class="diploma-preview-page">
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

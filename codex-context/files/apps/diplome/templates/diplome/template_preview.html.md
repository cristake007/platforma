# Source snapshot

## `apps/diplome/templates/diplome/template_preview.html`

Size: 1.5 KB

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

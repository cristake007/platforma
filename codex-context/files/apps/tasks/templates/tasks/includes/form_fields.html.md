# apps/tasks/templates/tasks/includes/form_fields.html

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `apps/tasks/templates/tasks/includes/form_fields.html`
- App: `tasks`
- App guide: `codex-context/apps/tasks.md`
- Role: `template`
- Size: 775 bytes
- Source SHA-256: `8509b459ad530de92859342a8d25fb369165c4c7343b296092793df2d53a34ad`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```html
{% if form.non_field_errors %}
    <div class="alert alert-error py-2 text-sm" role="alert">{{ form.non_field_errors|join:", " }}</div>
{% endif %}
{% for field in form %}
    <fieldset class="fieldset min-w-0 {% if field.name == 'description' %}sm:col-span-2{% endif %}">
        <label class="fieldset-legend" for="{{ field.id_for_label }}">{{ field.label }}{% if field.field.required %}<span class="text-error" aria-hidden="true"> *</span>{% endif %}</label>
        {{ field }}
        {% if field.help_text %}<p class="label whitespace-normal text-xs text-muted">{{ field.help_text }}</p>{% endif %}
        {% if field.errors %}<p class="label whitespace-normal text-xs text-error" role="alert">{{ field.errors|join:", " }}</p>{% endif %}
    </fieldset>
{% endfor %}
```

# Source snapshot

## `apps/tasks/templates/tasks/includes/form_fields.html`

Size: 775 B

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

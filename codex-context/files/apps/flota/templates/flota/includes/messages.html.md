# Source snapshot

## `apps/flota/templates/flota/includes/messages.html`

Size: 338 B

```html
{% if messages %}
<div class="space-y-2" aria-live="polite">
    {% for message in messages %}
        <div class="alert py-2 text-sm {% if message.tags == 'error' %}alert-error{% elif message.tags == 'success' %}alert-success{% else %}alert-info{% endif %}">
            {{ message }}
        </div>
    {% endfor %}
</div>
{% endif %}

```

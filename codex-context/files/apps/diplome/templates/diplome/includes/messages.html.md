# Source snapshot

## `apps/diplome/templates/diplome/includes/messages.html`

Size: 522 B

```html
{% if messages %}
    <div class="space-y-2">
        {% for message in messages %}
            <div
                class="alert {% if message.tags == 'error' %}alert-error{% elif message.tags == 'warning' %}alert-warning{% elif message.tags == 'info' %}alert-info{% else %}alert-success{% endif %} py-2 text-sm"
                role="{% if message.tags == 'error' %}alert{% else %}status{% endif %}"
            >
                <span>{{ message }}</span>
            </div>
        {% endfor %}
    </div>
{% endif %}
```

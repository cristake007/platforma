# apps/planificator/templates/planificator/includes/messages.html

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `apps/planificator/templates/planificator/includes/messages.html`
- App: `planificator`
- App guide: `codex-context/apps/planificator.md`
- Role: `template`
- Size: 773 bytes
- Source SHA-256: `37504803047b3cdc710473bd8446c6b1d56960fe9f3231f7b6b038c1eae6f551`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```html
{% if page_messages %}
    <div class="space-y-2" aria-live="polite">
        {% for message in page_messages %}
            <div class="alert border-primary/20 bg-base-200 py-2 text-base-content {% if message.level == 'error' %}border-error/30{% endif %}" role="{% if message.level == 'error' %}alert{% else %}status{% endif %}">
                <span class="badge badge-outline" aria-hidden="true">{% if message.level == 'error' %}!{% else %}✓{% endif %}</span>
                <div><h2 class="font-semibold">{{ message.title }}</h2><p class="text-sm">{{ message.body }}</p></div>
            </div>
        {% endfor %}
    </div>
{% endif %}
{% if form.non_field_errors %}
    <div class="alert alert-error" role="alert">{{ form.non_field_errors }}</div>
{% endif %}
```

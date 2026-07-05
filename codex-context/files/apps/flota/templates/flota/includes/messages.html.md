# apps/flota/templates/flota/includes/messages.html

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `apps/flota/templates/flota/includes/messages.html`
- App: `flota`
- App guide: `codex-context/apps/flota.md`
- Role: `template`
- Size: 338 bytes
- Source SHA-256: `98dead86b4f79b4f400102289af21a0a85232f8bdf08f4b0f071442047c29cb2`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

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

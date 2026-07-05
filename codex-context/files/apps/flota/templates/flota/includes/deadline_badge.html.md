# apps/flota/templates/flota/includes/deadline_badge.html

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `apps/flota/templates/flota/includes/deadline_badge.html`
- App: `flota`
- App guide: `codex-context/apps/flota.md`
- Role: `template`
- Size: 409 bytes
- Source SHA-256: `f231f46e5e69e96375f2e67019be5e279bb645b5099f4945027e339720d8ebad`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```html
<span
    class="badge badge-sm whitespace-nowrap
        {% if state.tone == 'success' %}badge-success badge-outline
        {% elif state.tone == 'warning' %}badge-warning badge-outline
        {% elif state.tone == 'error' %}badge-error badge-outline
        {% else %}badge-ghost{% endif %}"
    {% if due_on %}data-deadline data-due-date="{{ due_on|date:'Y-m-d' }}"{% endif %}
>{{ state.label }}</span>
```

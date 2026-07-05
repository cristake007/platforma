# apps/planificator/templates/planificator/includes/actions.html

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `apps/planificator/templates/planificator/includes/actions.html`
- App: `planificator`
- App guide: `codex-context/apps/planificator.md`
- Role: `template`
- Size: 998 bytes
- Source SHA-256: `a4a9e278b770382079631eca9fe92da238f21d15124556b41b6aaba9b0bc5f7d`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```html
<div class="card-actions items-center justify-between gap-3 border-t border-base-300 bg-base-200 p-4">
    <p class="text-xs font-semibold text-base-content">
        <span id="ops-month-count-summary">{{ selected_month_count }}</span> luni ·
        <span id="ops-holiday-count">{{ holiday_count }}</span> zile nelucrătoare · variație
        <span id="ops-randomness-summary">{{ form.randomness.value }}</span>/10
    </p>
    <button type="submit" id="ops-preview-submit" class="btn btn-outline btn-primary btn-sm">Generează programul</button>
</div>

{% if generation_error %}
    <div class="p-4 pt-0">
        <div class="alert alert-error" role="alert">
            <div>
                <p class="font-semibold">{{ generation_error }}</p>
                {% for month, courses in unscheduled_courses.items %}
                    <p class="mt-1 text-sm">Luna {{ month }}: {{ courses|join:", " }}</p>
                {% endfor %}
            </div>
        </div>
    </div>
{% endif %}
```

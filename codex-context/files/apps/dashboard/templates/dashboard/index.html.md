# apps/dashboard/templates/dashboard/index.html

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `apps/dashboard/templates/dashboard/index.html`
- App: `dashboard`
- App guide: `codex-context/apps/dashboard.md`
- Role: `template`
- Size: 520 bytes
- Source SHA-256: `f48aa0026b331b1f59290d006a4a118f9790bae8ea6c70bb6c77370d86b3c0ee`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```html
{% extends "layouts/base.html" %}

{% block title %}Operations Dashboard | Platforma TUVTK{% endblock %}

{% block content %}
    <section class="space-y-4">
        <div>
            <h1 class="ops-title text-2xl font-bold sm:text-[2rem]">Internal operations command center</h1>
            <p class="mt-1 max-w-3xl text-sm leading-6 text-muted">
                Monitor work intake, field activity, asset health, and alerts from a single shared workspace.
            </p>
        </div>
    </section>
{% endblock %}
```

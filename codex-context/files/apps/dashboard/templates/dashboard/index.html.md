# Source snapshot

## `apps/dashboard/templates/dashboard/index.html`

Size: 520 B

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

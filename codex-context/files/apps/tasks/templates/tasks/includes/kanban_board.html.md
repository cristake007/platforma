# Source snapshot

## `apps/tasks/templates/tasks/includes/kanban_board.html`

Size: 2.1 KB

```html
<div id="kanban-board-region" class="flex min-h-[34rem] gap-3 overflow-x-auto border-y border-base-300 bg-base-100 py-3" data-kanban-board{% if kanban_board_oob %} hx-swap-oob="true"{% endif %}>
    {% for stage in stages %}
        <section class="flex w-80 shrink-0 flex-col border border-base-300 bg-base-200/60 transition-colors {% if stage.tone == 'error' %}border-t-4 border-t-error{% elif stage.tone == 'success' %}border-t-4 border-t-success{% elif stage.tone == 'warning' %}border-t-4 border-t-warning{% elif stage.tone == 'info' %}border-t-4 border-t-primary{% else %}border-t-4 border-t-base-300{% endif %}" data-stage-column data-stage-id="{{ stage.pk }}">
            <header class="border-b border-base-300 bg-base-100 px-3 py-3">
                <div class="flex items-start justify-between gap-3">
                    <div class="min-w-0">
                        <h2 class="truncate text-sm font-semibold text-base-content">{{ stage.name }}</h2>
                        <p class="mt-0.5 text-[11px] font-medium uppercase tracking-wide text-muted">{% if stage.is_terminal %}Etapă finală{% else %}Etapă activă{% endif %}</p>
                    </div>
                    <span class="badge badge-sm border-base-300 bg-base-200 font-semibold" data-stage-count>{{ stage.visible_tasks|length }}</span>
                </div>
            </header>
            <div class="flex min-h-80 flex-1 flex-col gap-2 border border-transparent p-2 transition-colors" data-stage-cards data-stage-drop-zone>
                {% include "tasks/includes/kanban_empty_stage.html" %}
                {% for task in stage.visible_tasks %}
                    {% include "tasks/includes/kanban_card.html" %}
                {% endfor %}
                <button type="button" class="mt-auto min-h-10 border border-dashed border-base-300 bg-base-100 px-3 text-sm font-medium text-muted transition-colors hover:border-primary hover:text-primary focus-visible:outline focus-visible:outline-2 focus-visible:outline-primary" data-open-task-dialog>+ Adaugă task</button>
            </div>
        </section>
    {% endfor %}
</div>
```

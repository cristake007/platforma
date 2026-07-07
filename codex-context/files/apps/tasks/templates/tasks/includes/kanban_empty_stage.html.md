# Source snapshot

## `apps/tasks/templates/tasks/includes/kanban_empty_stage.html`

Size: 368 B

```html
<div class="{% if stage.visible_tasks %}hidden {% endif %}flex min-h-28 flex-col items-center justify-center border border-dashed border-base-300 bg-base-100 px-3 py-5 text-center text-xs text-muted" data-stage-empty>
    <span class="font-semibold text-base-content">Etapă liberă</span>
    <span class="mt-1">Trage un task aici sau adaugă unul nou.</span>
</div>
```

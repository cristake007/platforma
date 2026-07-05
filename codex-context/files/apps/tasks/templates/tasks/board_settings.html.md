# apps/tasks/templates/tasks/board_settings.html

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `apps/tasks/templates/tasks/board_settings.html`
- App: `tasks`
- App guide: `codex-context/apps/tasks.md`
- Role: `template`
- Size: 6334 bytes
- Source SHA-256: `27b6018eeb06e9e0f7607246d4bc57419e8c072e307a38c44229b907673dd682`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```html
{% extends "layouts/base.html" %}
{% block title %}Setări {{ board.name }} | Task-uri{% endblock %}
{% block content %}
<section class="space-y-6">
    {% include "tasks/includes/messages.html" %}
    <div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between"><div><p class="text-xs text-muted"><a href="{% url 'tasks:index' %}" class="hover:text-primary">Task-uri</a> / Setări</p><h1 class="ops-title mt-1 text-2xl font-bold">{{ board.name }}</h1><p class="mt-1 text-sm text-muted">Membri, proprietate și flux Kanban.</p></div>{% if not board.is_archived %}<a href="{% url 'tasks:board_kanban' board.pk %}" class="btn btn-outline btn-sm">Înapoi la Kanban</a>{% endif %}</div>

    <div class="grid gap-5 lg:grid-cols-2">
        <section class="border border-base-300 bg-base-100 p-5"><h2 class="font-semibold text-base-content">Membri</h2><p class="mt-1 text-xs text-muted">Task-urile pot fi atribuite doar membrilor activi.</p><div class="mt-4 divide-y divide-base-300">{% for membership in members %}<div class="flex items-center justify-between gap-3 py-3"><div><p class="text-sm font-medium">{{ membership.user.get_full_name|default:membership.user.username }}</p><p class="text-xs text-muted">{% if membership.user_id == board.owner_id %}Proprietar{% else %}Membru{% endif %}{% if not membership.user.is_active %} · Inactiv{% endif %}</p></div>{% if membership.user_id != board.owner_id %}<form method="post" action="{% url 'tasks:member_remove' board.pk membership.user_id %}">{% csrf_token %}<button class="btn btn-ghost btn-xs text-error">Elimină</button></form>{% endif %}</div>{% endfor %}</div>{% if member_form.fields.user.queryset.exists %}<form method="post" action="{% url 'tasks:member_add' board.pk %}" class="mt-4 flex items-end gap-2">{% csrf_token %}<fieldset class="fieldset flex-1"><label class="fieldset-legend" for="{{ member_form.user.id_for_label }}">Adaugă membru</label>{{ member_form.user }}</fieldset><button class="btn btn-primary btn-sm">Adaugă</button></form>{% endif %}</section>
        <section class="border border-base-300 bg-base-100 p-5"><h2 class="font-semibold">Proprietate și arhivare</h2><p class="mt-1 text-xs text-muted">Proprietarul configurează board-ul; staff-ul păstrează acces de administrare.</p>{% if transfer_form.fields.new_owner.queryset.exists %}<form method="post" action="{% url 'tasks:ownership_transfer' board.pk %}" class="mt-4 space-y-3">{% csrf_token %}<fieldset class="fieldset"><label class="fieldset-legend" for="{{ transfer_form.new_owner.id_for_label }}">Transferă proprietatea</label>{{ transfer_form.new_owner }}</fieldset><button class="btn btn-outline btn-primary btn-sm">Transferă</button></form>{% endif %}<form method="post" action="{% url 'tasks:board_archive' board.pk %}" class="mt-6 border-t border-base-300 pt-4">{% csrf_token %}<input type="hidden" name="archived" value="{% if board.is_archived %}0{% else %}1{% endif %}"><button class="btn btn-outline {% if board.is_archived %}btn-success{% else %}btn-error{% endif %} btn-sm">{% if board.is_archived %}Restaurează board-ul{% else %}Arhivează board-ul{% endif %}</button></form></section>
    </div>

    <section class="border border-base-300 bg-base-100 p-5"><div><h2 class="font-semibold">Etape Kanban</h2><p class="mt-1 text-xs text-muted">Păstrează cel puțin o etapă activă și una terminală.</p></div><div class="mt-4 space-y-3">{% for row in stage_rows %}<article class="border border-base-300 bg-base-200/40 p-4"><form method="post" action="{% url 'tasks:stage_update' row.stage.pk %}" class="grid items-end gap-3 md:grid-cols-[1.4fr_1fr_auto_auto]">{% csrf_token %}<fieldset class="fieldset"><label class="fieldset-legend" for="{{ row.form.name.id_for_label }}">Nume</label>{{ row.form.name }}</fieldset><fieldset class="fieldset"><label class="fieldset-legend" for="{{ row.form.tone.id_for_label }}">Ton semantic</label>{{ row.form.tone }}</fieldset><label class="flex h-8 items-center gap-2 text-sm">{{ row.form.is_terminal }} Terminală</label><div class="flex gap-1"><button class="btn btn-primary btn-sm">Salvează</button></div></form><div class="mt-3 flex flex-wrap items-end justify-between gap-3 border-t border-base-300 pt-3"><form method="post" action="{% url 'tasks:stage_position' row.stage.pk %}" class="join">{% csrf_token %}<button name="direction" value="up" class="btn btn-ghost btn-xs join-item" aria-label="Mută etapa în sus">↑</button><button name="direction" value="down" class="btn btn-ghost btn-xs join-item" aria-label="Mută etapa în jos">↓</button></form><form method="post" action="{% url 'tasks:stage_delete' row.stage.pk %}" class="flex items-end gap-2">{% csrf_token %}<fieldset class="fieldset"><label class="fieldset-legend" for="{{ row.delete_form.replacement_stage.id_for_label }}">Înlocuire</label>{{ row.delete_form.replacement_stage }}</fieldset><button class="btn btn-ghost btn-xs text-error">Șterge etapa</button></form></div></article>{% endfor %}</div><form method="post" action="{% url 'tasks:stage_create' board.pk %}" class="mt-5 grid items-end gap-3 border-t border-base-300 pt-5 md:grid-cols-[1.4fr_1fr_auto_auto]">{% csrf_token %}<fieldset class="fieldset"><label class="fieldset-legend" for="{{ stage_form.name.id_for_label }}">Etapă nouă</label>{{ stage_form.name }}</fieldset><fieldset class="fieldset"><label class="fieldset-legend" for="{{ stage_form.tone.id_for_label }}">Ton semantic</label>{{ stage_form.tone }}</fieldset><label class="flex h-8 items-center gap-2 text-sm">{{ stage_form.is_terminal }} Terminală</label><button class="btn btn-outline btn-primary btn-sm">Adaugă</button></form></section>

    {% if archived_tasks %}<section class="border border-base-300 bg-base-100 p-5"><h2 class="font-semibold">Task-uri arhivate</h2><div class="mt-3 divide-y divide-base-300">{% for task in archived_tasks %}<div class="flex items-center justify-between gap-3 py-3"><span class="text-sm">{{ task.title }}</span><form method="post" action="{% url 'tasks:task_archive' task.pk %}">{% csrf_token %}<input type="hidden" name="archived" value="0"><input type="hidden" name="next" value="{% url 'tasks:board_settings' board.pk %}"><button class="btn btn-ghost btn-xs text-success">Restaurează</button></form></div>{% endfor %}</div></section>{% endif %}
</section>
{% endblock %}
```

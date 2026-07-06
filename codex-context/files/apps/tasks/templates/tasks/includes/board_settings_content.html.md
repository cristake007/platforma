# Source snapshot

## `apps/tasks/templates/tasks/includes/board_settings_content.html`

Size: 12.7 KB

```html
<section id="board-settings-content" class="space-y-6">
    {% include "tasks/includes/messages.html" %}
    <div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div>
            <p class="text-xs text-muted"><a href="{% url 'tasks:index' %}" class="hover:text-primary">Task-uri</a> / Set&#259;ri</p>
            <h1 class="ops-title mt-1 text-2xl font-bold">{{ board.name }}</h1>
            <p class="mt-1 text-sm text-muted">Membri, proprietate &#537;i flux Kanban.</p>
        </div>
        {% if not board.is_archived %}<a href="{% url 'tasks:board_kanban' board.pk %}" class="btn btn-outline btn-sm">&#206;napoi la Kanban</a>{% endif %}
    </div>

    <div class="grid gap-5 lg:grid-cols-2">
        <section class="border border-base-300 bg-base-100 p-5">
            <h2 class="font-semibold text-base-content">Membri</h2>
            <p class="mt-1 text-xs text-muted">Task-urile pot fi atribuite doar membrilor activi.</p>
            <div class="mt-4 divide-y divide-base-300">
                {% for membership in members %}
                    <div class="flex items-center justify-between gap-3 py-3">
                        <div>
                            <p class="text-sm font-medium">{{ membership.user.get_full_name|default:membership.user.username }}</p>
                            <p class="text-xs text-muted">{% if membership.user_id == board.owner_id %}Proprietar{% else %}Membru{% endif %}{% if not membership.user.is_active %} &middot; Inactiv{% endif %}</p>
                        </div>
                        {% if membership.user_id != board.owner_id %}
                            <form method="post" action="{% url 'tasks:member_remove' board.pk membership.user_id %}" hx-post="{% url 'tasks:member_remove' board.pk membership.user_id %}" hx-target="#board-settings-content" hx-swap="outerHTML">
                                {% csrf_token %}
                                <button class="btn btn-ghost btn-xs text-error">Elimin&#259;</button>
                            </form>
                        {% endif %}
                    </div>
                {% endfor %}
            </div>
            {% if member_form.fields.user.queryset.exists %}
                <form method="post" action="{% url 'tasks:member_add' board.pk %}" class="mt-4 flex items-end gap-2" hx-post="{% url 'tasks:member_add' board.pk %}" hx-target="#board-settings-content" hx-swap="outerHTML">
                    {% csrf_token %}
                    <fieldset class="fieldset flex-1">
                        <label class="fieldset-legend" for="{{ member_form.user.id_for_label }}">Adaug&#259; membru</label>
                        {{ member_form.user }}
                        {% if member_form.user.errors %}<p class="label whitespace-normal text-xs text-error" role="alert">{{ member_form.user.errors|join:", " }}</p>{% endif %}
                    </fieldset>
                    <button class="btn btn-primary btn-sm">Adaug&#259;</button>
                </form>
            {% endif %}
        </section>

        <section class="border border-base-300 bg-base-100 p-5">
            <h2 class="font-semibold">Proprietate &#537;i arhivare</h2>
            <p class="mt-1 text-xs text-muted">Proprietarul configureaz&#259; board-ul; staff-ul p&#259;streaz&#259; acces de administrare.</p>
            {% if transfer_form.fields.new_owner.queryset.exists %}
                <form method="post" action="{% url 'tasks:ownership_transfer' board.pk %}" class="mt-4 space-y-3" hx-post="{% url 'tasks:ownership_transfer' board.pk %}" hx-target="#board-settings-content" hx-swap="outerHTML">
                    {% csrf_token %}
                    <fieldset class="fieldset">
                        <label class="fieldset-legend" for="{{ transfer_form.new_owner.id_for_label }}">Transfer&#259; proprietatea</label>
                        {{ transfer_form.new_owner }}
                        {% if transfer_form.new_owner.errors %}<p class="label whitespace-normal text-xs text-error" role="alert">{{ transfer_form.new_owner.errors|join:", " }}</p>{% endif %}
                    </fieldset>
                    <button class="btn btn-outline btn-primary btn-sm">Transfer&#259;</button>
                </form>
            {% endif %}
            <form method="post" action="{% url 'tasks:board_archive' board.pk %}" class="mt-6 border-t border-base-300 pt-4" hx-post="{% url 'tasks:board_archive' board.pk %}" hx-target="#board-settings-content" hx-swap="outerHTML">
                {% csrf_token %}
                <input type="hidden" name="archived" value="{% if board.is_archived %}0{% else %}1{% endif %}">
                <button class="btn btn-outline {% if board.is_archived %}btn-success{% else %}btn-error{% endif %} btn-sm">{% if board.is_archived %}Restaureaz&#259; board-ul{% else %}Arhiveaz&#259; board-ul{% endif %}</button>
            </form>
        </section>
    </div>

    <section class="border border-base-300 bg-base-100 p-5">
        <div class="flex flex-col gap-2 lg:flex-row lg:items-start lg:justify-between">
            <div>
                <h2 class="font-semibold">Etape Kanban</h2>
                <p class="mt-1 text-xs text-muted">P&#259;streaz&#259; cel pu&#539;in o etap&#259; activ&#259; &#537;i una final&#259;.</p>
            </div>
            <p class="max-w-xl text-xs text-muted">
                Etapele finale marcheaz&#259; task-urile ca finalizate. La &#537;tergerea unei etape, task-urile existente trebuie mutate
                &#238;ntr-o alt&#259; etap&#259; din acela&#537;i board.
            </p>
        </div>

        <form method="post" action="{% url 'tasks:stage_create' board.pk %}" class="mt-5 border border-dashed border-base-300 bg-base-200/30 p-4" hx-post="{% url 'tasks:stage_create' board.pk %}" hx-target="#board-settings-content" hx-swap="outerHTML">
            {% csrf_token %}
            <div class="grid items-end gap-3 md:grid-cols-[1.4fr_1fr_auto_auto]">
                <fieldset class="fieldset">
                    <label class="fieldset-legend" for="{{ stage_form.name.id_for_label }}">Etap&#259; nou&#259;</label>
                    {{ stage_form.name }}
                    {% if stage_form.name.errors %}<p class="label whitespace-normal text-xs text-error" role="alert">{{ stage_form.name.errors|join:", " }}</p>{% endif %}
                </fieldset>
                <fieldset class="fieldset">
                    <label class="fieldset-legend" for="{{ stage_form.tone.id_for_label }}">Ton semantic</label>
                    {{ stage_form.tone }}
                    {% if stage_form.tone.errors %}<p class="label whitespace-normal text-xs text-error" role="alert">{{ stage_form.tone.errors|join:", " }}</p>{% endif %}
                </fieldset>
                <label class="flex h-8 items-center gap-2 text-sm">{{ stage_form.is_terminal }} Etap&#259; final&#259;</label>
                <button class="btn btn-primary btn-sm">Adaug&#259; etap&#259;</button>
            </div>
        </form>

        <div class="mt-5 space-y-3">
            {% for row in stage_rows %}
                <article class="border border-base-300 bg-base-100 p-4">
                    <div class="flex flex-col gap-1 border-b border-base-300 pb-3 sm:flex-row sm:items-center sm:justify-between">
                        <div>
                            <h3 class="text-sm font-semibold text-base-content">{{ row.stage.name }}</h3>
                            <p class="text-xs text-muted">Pozi&#539;ia {{ row.stage.position|add:1 }}{% if row.stage.is_terminal %} &middot; etap&#259; final&#259;{% endif %}</p>
                        </div>
                        <span class="badge badge-outline badge-sm">{{ row.stage.get_tone_display }}</span>
                    </div>

                    <form method="post" action="{% url 'tasks:stage_update' row.stage.pk %}" class="mt-4" hx-post="{% url 'tasks:stage_update' row.stage.pk %}" hx-target="#board-settings-content" hx-swap="outerHTML">
                        {% csrf_token %}
                        <div class="grid items-end gap-3 md:grid-cols-[1.4fr_1fr_auto_auto]">
                            <fieldset class="fieldset">
                                <label class="fieldset-legend" for="{{ row.form.name.id_for_label }}">Nume</label>
                                {{ row.form.name }}
                                {% if row.form.name.errors %}<p class="label whitespace-normal text-xs text-error" role="alert">{{ row.form.name.errors|join:", " }}</p>{% endif %}
                            </fieldset>
                            <fieldset class="fieldset">
                                <label class="fieldset-legend" for="{{ row.form.tone.id_for_label }}">Ton semantic</label>
                                {{ row.form.tone }}
                                {% if row.form.tone.errors %}<p class="label whitespace-normal text-xs text-error" role="alert">{{ row.form.tone.errors|join:", " }}</p>{% endif %}
                            </fieldset>
                            <label class="flex h-8 items-center gap-2 text-sm">{{ row.form.is_terminal }} Etap&#259; final&#259;</label>
                            <button class="btn btn-outline btn-sm">Salveaz&#259;</button>
                        </div>
                    </form>

                    <div class="mt-4 grid gap-3 border-t border-base-300 pt-3 lg:grid-cols-[auto_1fr]">
                        <div>
                            <p class="mb-2 text-xs font-medium text-base-content">Mutare</p>
                            <form method="post" action="{% url 'tasks:stage_position' row.stage.pk %}" class="join" hx-post="{% url 'tasks:stage_position' row.stage.pk %}" hx-target="#board-settings-content" hx-swap="outerHTML">
                                {% csrf_token %}
                                <button name="direction" value="up" class="btn btn-ghost btn-xs join-item" aria-label="Mut&#259; etapa &#238;n sus">&uarr;</button>
                                <button name="direction" value="down" class="btn btn-ghost btn-xs join-item" aria-label="Mut&#259; etapa &#238;n jos">&darr;</button>
                            </form>
                        </div>
                        <details class="border-l-0 border-base-300 lg:border-l lg:pl-4" {% if row.delete_form.replacement_stage.errors %}open{% endif %}>
                            <summary class="btn btn-outline btn-error btn-xs">Preg&#259;te&#537;te &#537;tergerea</summary>
                            <form method="post" action="{% url 'tasks:stage_delete' row.stage.pk %}" class="mt-3 flex flex-col gap-3 sm:flex-row sm:items-end" hx-post="{% url 'tasks:stage_delete' row.stage.pk %}" hx-target="#board-settings-content" hx-swap="outerHTML">
                                {% csrf_token %}
                                <fieldset class="fieldset min-w-64 flex-1">
                                    <label class="fieldset-legend" for="{{ row.delete_form.replacement_stage.id_for_label }}">Mut&#259; task-urile &#238;n</label>
                                    {{ row.delete_form.replacement_stage }}
                                    <p class="label whitespace-normal text-xs text-muted">Aceast&#259; alegere se aplic&#259; tuturor task-urilor din etapa &#537;tears&#259;.</p>
                                    {% if row.delete_form.replacement_stage.errors %}<p class="label whitespace-normal text-xs text-error" role="alert">{{ row.delete_form.replacement_stage.errors|join:", " }}</p>{% endif %}
                                </fieldset>
                                <button class="btn btn-error btn-sm">&#536;terge etapa</button>
                            </form>
                        </details>
                    </div>
                </article>
            {% endfor %}
        </div>
    </section>

    {% if archived_tasks %}
        <section class="border border-base-300 bg-base-100 p-5">
            <h2 class="font-semibold">Task-uri arhivate</h2>
            <div class="mt-3 divide-y divide-base-300">
                {% for task in archived_tasks %}
                    <div class="flex items-center justify-between gap-3 py-3">
                        <span class="text-sm">{{ task.title }}</span>
                        <form method="post" action="{% url 'tasks:task_archive' task.pk %}" hx-post="{% url 'tasks:task_archive' task.pk %}" hx-target="#board-settings-content" hx-swap="outerHTML">
                            {% csrf_token %}
                            <input type="hidden" name="archived" value="0">
                            <input type="hidden" name="next" value="{% url 'tasks:board_settings' board.pk %}">
                            <button class="btn btn-ghost btn-xs text-success">Restaureaz&#259;</button>
                        </form>
                    </div>
                {% endfor %}
            </div>
        </section>
    {% endif %}
</section>
```

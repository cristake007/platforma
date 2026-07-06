# Source snapshot

## `core/templates/includes/sidebar.html`

Size: 5.6 KB

```html
{% load bootstrap_icons %}
<div class="drawer-side z-40 h-full min-h-0 is-drawer-close:overflow-visible">
    <label for="ops-sidebar" aria-label="Închide bara laterală" class="drawer-overlay"></label>
    <aside class="ops-sidebar flex h-full flex-col overflow-visible transition-[width] duration-200 is-drawer-close:w-14 is-drawer-open:w-72">
        <nav class="ops-sidebar-nav min-h-0 flex-1 overflow-y-auto py-4 is-drawer-close:overflow-visible" aria-label="Navigare principală" tabindex="0">
            <div class="space-y-4">
                {% for section in app_navigation %}
                    <section>
                        <h2 class="ops-sidebar-heading mb-2 px-3 text-[11px] font-semibold uppercase tracking-[0.2em] is-drawer-close:hidden">{{ section.label }}</h2>
                        <ul class="menu p-0">
                            {% for item in section.items %}
                                <li>
                                    {% if item.children %}
                                        <details class="ops-nav-group" data-sidebar-flyout {% if item.is_active %}open{% endif %}>
                                            <summary class="is-drawer-close:tooltip is-drawer-close:tooltip-right is-drawer-close:justify-center transition-none" data-sidebar-flyout-trigger data-tip="{{ item.label }}" aria-haspopup="true" aria-controls="ops-submenu-{{ forloop.parentloop.counter }}-{{ forloop.counter }}" aria-expanded="{% if item.is_active %}true{% else %}false{% endif %}">
                                                <span class="ops-nav-icon">
                                                    {% if item.icon_set == "mdi" %}{% md_icon item.icon extra_classes="ops-nav-glyph" %}{% else %}{% bs_icon item.icon extra_classes="ops-nav-glyph bi-valign-default" %}{% endif %}
                                                </span>
                                                <span class="is-drawer-close:hidden">{{ item.label }}</span>
                                                <svg class="ops-nav-chevron is-drawer-close:hidden" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="m9 6 6 6-6 6" /></svg>
                                            </summary>
                                            <ul id="ops-submenu-{{ forloop.parentloop.counter }}-{{ forloop.counter }}" class="ops-submenu" data-sidebar-flyout-panel>
                                                {% for child in item.children %}
                                                    <li>
                                                        {% if child.url_name %}
                                                            <a href="{% url child.url_name %}" class="transition-none{% if child.is_active %} active font-semibold{% endif %}" {% if child.is_active %}aria-current="page"{% endif %}><span class="ops-submenu-label">{{ child.label }}</span></a>
                                                        {% else %}
                                                            <a href="#" class="transition-none"><span class="ops-submenu-label">{{ child.label }}</span></a>
                                                        {% endif %}
                                                    </li>
                                                {% endfor %}
                                            </ul>
                                        </details>
                                    {% else %}
                                        {% if item.url_name %}
                                            <a href="{% url item.url_name %}" class="is-drawer-close:tooltip is-drawer-close:tooltip-right is-drawer-close:justify-center transition-none{% if item.is_active %} active font-semibold{% endif %}" data-tip="{{ item.label }}" {% if item.is_active %}aria-current="page"{% endif %}>
                                        {% else %}
                                            <a href="#" class="is-drawer-close:tooltip is-drawer-close:tooltip-right is-drawer-close:justify-center transition-none" data-tip="{{ item.label }}">
                                        {% endif %}
                                            <span class="ops-nav-icon">{% bs_icon item.icon extra_classes="ops-nav-glyph bi-valign-default" %}</span>
                                            <span class="is-drawer-close:hidden">{{ item.label }}</span>
                                        </a>
                                    {% endif %}
                                </li>
                            {% endfor %}
                        </ul>
                    </section>
                {% endfor %}
            </div>
        </nav>
        <div class="border-t border-[var(--sidebar-footer-divider)] p-3 is-drawer-close:hidden">
            <div class="ops-sidebar-note p-3">
                <div class="flex items-center justify-between gap-3">
                    <div>
                        <p class="text-sm font-semibold text-[var(--sidebar-footer-heading-text)]">Platformă în dezvoltare</p>
                        <p class="text-xs text-[var(--sidebar-footer-text)]">Modulele vor fi activate treptat</p>
                    </div>
                    <span class="badge border border-[var(--sidebar-footer-border)] bg-[var(--sidebar-footer-bg)] text-[var(--sidebar-item-text)]">Local</span>
                </div>
                <div class="mt-3 flex items-center justify-between text-xs text-[var(--sidebar-footer-text)]">
                    <span>Mediu</span>
                    <span>Dezvoltare</span>
                </div>
            </div>
        </div>
    </aside>
</div>
```

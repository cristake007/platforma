# Source snapshot

## `docs/frontend/table-patterns.md`

Size: 4.0 KB

````markdown
# Frontend Table Patterns

Guidance for Django templates, HTMX, Alpine.js, Tailwind, and daisyUI table/list screens.

## Preferred default

Use ordinary Django pagination first unless the workflow clearly benefits from lazy loading.

For internal operations, tables must stay:

- readable;
- filterable;
- debuggable;
- safe with permissions;
- usable after refresh;
- friendly to browser memory.

## Template structure

A good list page usually has:

```text
templates/<app>/<model>_list.html
templates/<app>/partials/<model>_table.html
templates/<app>/partials/<model>_rows.html
templates/<app>/partials/<model>_empty.html
```

Use partials for repeated page sections, but do not make a generic table engine too early.

Different tables may have different columns. That is normal.

Extract common pieces only when they are truly shared:

- table wrapper;
- empty state;
- pagination controls;
- loading indicator;
- bulk action toolbar;
- row action button style.

Keep business columns explicit in the app template.

## HTMX table refresh

Good for:

- search;
- filters;
- sorting;
- pagination;
- local list refresh after create/edit/delete;
- row archive/restore.

Pattern:

```html
<form
  hx-get="{% url 'app:list' %}"
  hx-target="#table-region"
  hx-trigger="change, keyup delay:300ms from:input[name='q']"
>
  <!-- filters -->
</form>

<div id="table-region">
  {% include "app/partials/table.html" %}
</div>
```

In the view:

```python
def list_view(request):
    context = build_context(request)
    if getattr(request, "htmx", False):
        return render(request, "app/partials/table.html", context)
    return render(request, "app/list.html", context)
```

## Fixed-height lazy rows

Use this when the user wants the table to stay fixed size and load more rows while scrolling.

Recommended behavior:

- table wrapper has fixed height and `overflow-y-auto`;
- first request loads the first chunk;
- a sentinel row at the bottom triggers the next chunk;
- server returns only more rows and the next sentinel;
- filters/search reset the region;
- ordering is stable.

Example shape:

```html
<div id="table-scroll" class="max-h-[70vh] overflow-y-auto">
  <table class="table table-zebra w-full">
    <thead class="sticky top-0 z-10 bg-base-100">
      <!-- headings -->
    </thead>
    <tbody id="rows">
      {% include "app/partials/rows.html" %}
    </tbody>
  </table>
</div>
```

Sentinel idea:

```html
<tr
  hx-get="{% url 'app:list_rows' %}?page={{ next_page }}{{ current_querystring }}"
  hx-trigger="revealed"
  hx-swap="outerHTML"
>
  <td colspan="99">Loading more...</td>
</tr>
```

The server should include a next sentinel only while more results exist.

## When not to use infinite scroll

Avoid it when users need:

- exact page numbers;
- bookmarking a result page;
- easy browser back/forward behavior;
- exporting exact filtered result sets;
- comparing items across many pages;
- very large result sets that would stay in the browser for a long session.

For those cases, use normal pagination with HTMX partial refresh.

## Alpine usage in tables

Good Alpine uses:

- selected row visual state;
- bulk action toolbar visibility;
- filter drawer open/close;
- column help/tooltips;
- local loading indicator;
- mobile details expansion.

Do not use Alpine for:

- ownership checks;
- permissions;
- deciding which rows the user may see;
- saving selected records to the database without a POST;
- replacing Django form validation.

## Codex prompt for table work

```text
Work only on this table/list page.

Target app:
- apps/<app>

Target page:
- <template path>

Goal:
[describe: HTMX filter refresh / fixed-height lazy rows / selected row UI]

Rules:
- Keep Django as source of truth.
- Use HTMX only for server-rendered partial updates.
- Use Alpine only for local UI state.
- Preserve full-page fallback where practical.
- Preserve permissions and filters.
- Do not touch unrelated apps.
- Return a minimal diff.
```
````

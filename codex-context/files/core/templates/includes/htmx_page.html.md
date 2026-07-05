# Source snapshot

## `core/templates/includes/htmx_page.html`

Size: 293 B

```html
<title>{{ shell_page_title }}</title>
<div
    id="page-content"
    class="mx-auto w-full max-w-[1600px] px-4 py-4 sm:px-5 sm:py-5 lg:px-6 lg:py-5"
    data-active-nav-url="{{ shell_active_nav_url }}"
    hx-history-elt
    hx-history="false"
>
    {% include htmx_content_template %}
</div>
```

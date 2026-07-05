# Source snapshot

## `core/mixins.py`

Size: 1.5 KB

```python
from django.http import HttpResponse
from django.urls import reverse


class HtmxPageMixin:
    """Return a page fragment for explicit HTMX navigation requests."""

    htmx_template_name = "includes/htmx_page.html"
    htmx_content_template = None
    shell_page_title = "Platforma TUVTK"
    shell_nav_url_name = None

    def is_htmx_fragment_request(self):
        headers = self.request.headers
        return (
            headers.get("HX-Request") == "true"
            and headers.get("HX-History-Restore-Request") != "true"
        )

    def get_template_names(self):
        if self.is_htmx_fragment_request():
            return [self.htmx_template_name]
        return super().get_template_names()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "htmx_content_template": self.htmx_content_template,
                "shell_page_title": self.shell_page_title,
                "shell_active_nav_url": reverse(self.shell_nav_url_name),
            }
        )
        return context

    def handle_no_permission(self):
        response = super().handle_no_permission()
        if (
            self.request.headers.get("HX-Request") == "true"
            and response.status_code in {301, 302}
            and response.get("Location")
        ):
            return HttpResponse(
                status=204,
                headers={"HX-Redirect": response["Location"]},
            )
        return response
```

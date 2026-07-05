# Source snapshot

## `apps/dashboard/views.py`

Size: 419 B

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from core.mixins import HtmxPageMixin


class DashboardView(HtmxPageMixin, LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'
    htmx_content_template = "dashboard/_content.html"
    shell_page_title = "Operations Dashboard | Platforma TUVTK"
    shell_nav_url_name = "dashboard:index"
```

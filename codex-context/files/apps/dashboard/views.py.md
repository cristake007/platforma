# Source snapshot

## `apps/dashboard/views.py`

Size: 204 B

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'
```

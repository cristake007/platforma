# apps/dashboard/views.py

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `apps/dashboard/views.py`
- App: `dashboard`
- App guide: `codex-context/apps/dashboard.md`
- Role: `backend`
- Size: 204 bytes
- Source SHA-256: `8c8203ed49b5a616621d0463a7c96fb1f023a7ddd322e00eabaed94b0d11f9b6`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'
```

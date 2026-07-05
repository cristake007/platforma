# apps/dashboard/urls.py

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `apps/dashboard/urls.py`
- App: `dashboard`
- App guide: `codex-context/apps/dashboard.md`
- Role: `backend`
- Size: 159 bytes
- Source SHA-256: `f400b1da0522b29ae28b719712e7251b8e642795fb2a4226c1c341a8623476a3`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from django.urls import path

from .views import DashboardView

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardView.as_view(), name='index'),
]
```

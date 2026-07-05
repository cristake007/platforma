# Source snapshot

## `apps/dashboard/urls.py`

Size: 159 B

```python
from django.urls import path

from .views import DashboardView

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardView.as_view(), name='index'),
]
```

# platforma_tuvtk/urls.py

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `platforma_tuvtk/urls.py`
- App: none
- Role: `project-config`
- Size: 1567 bytes
- Source SHA-256: `8a0525fc6f820a6d78713b49047cde471b781f7aa9d2732057aadab7081e1322`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
"""
URL configuration for platforma_tuvtk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('apps.dashboard.urls')),
    path('planificator/', include('apps.planificator.urls')),
    path('diplome/', include('apps.diplome.urls')),
    path('biblioteca-media/', include('apps.media_library.urls')),
    path('tasks/', include('apps.tasks.urls')),
    path('flota/', include('apps.flota.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if getattr(settings, "HAS_DJANGO_BROWSER_RELOAD", False):
    # Include django_browser_reload URLs only in DEBUG mode
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
```

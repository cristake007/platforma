# core/middleware.py

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `core/middleware.py`
- App: none
- Role: `core`
- Size: 1079 bytes
- Source SHA-256: `692286b6c0c7485a7db2f94077aa74912c5e006a118ccd2263d7259c451832c5`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from .context_processors import build_application_shell
from .models import UserProfile


class ApplicationShellMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request._application_shell_profile = None
        request._application_shell_permissions = set()
        if request.user.is_authenticated:
            request._application_shell_profile = (
                UserProfile.objects.only("avatar", "user_id").filter(user_id=request.user.pk).first()
            )
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated and not request.user.is_superuser:
            request._application_shell_permissions = request.user.get_all_permissions()
        request.application_shell = build_application_shell(
            request,
            getattr(request, "_application_shell_profile", None),
            getattr(request, "_application_shell_permissions", set()),
        )
        return None
```

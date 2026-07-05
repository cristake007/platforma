# Source snapshot

## `core/middleware.py`

Size: 1.1 KB

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

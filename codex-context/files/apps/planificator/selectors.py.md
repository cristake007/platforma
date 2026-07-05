# apps/planificator/selectors.py

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `apps/planificator/selectors.py`
- App: `planificator`
- App guide: `codex-context/apps/planificator.md`
- Role: `backend`
- Size: 986 bytes
- Source SHA-256: `c23bc0da74e0c39be81730260040c6e0ec0aaa2380a42ecd18879e9ab0fa534f`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import ScheduleGeneration


def list_owned_generations(*, user):
    return (
        ScheduleGeneration.objects.filter(
            owner=user,
            expires_at__gt=timezone.now(),
        )
        .only(
            "id",
            "year",
            "selected_months",
            "source_course_count",
            "generated_entry_count",
            "source_file_name",
            "source_file_digest",
            "created_at",
            "expires_at",
        )
        .order_by("-created_at")
    )


def get_owned_generation(*, generation_id, user) -> ScheduleGeneration:
    generation = get_object_or_404(
        ScheduleGeneration.objects.select_related("owner"),
        pk=generation_id,
        owner=user,
    )
    if generation.expires_at <= timezone.now():
        raise Http404("Generarea a expirat.")
    return generation
```

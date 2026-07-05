# Source snapshot

## `apps/planificator/selectors.py`

Size: 986 B

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

# Source snapshot

## `apps/planificator/management/commands/purge_expired_schedule_generations.py`

Size: 462 B

```python
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.planificator.models import ScheduleGeneration


class Command(BaseCommand):
    help = "Șterge generările de program expirate."

    def handle(self, *args, **options):
        deleted, _ = ScheduleGeneration.objects.filter(expires_at__lte=timezone.now()).delete()
        self.stdout.write(self.style.SUCCESS(f"Au fost sterse {deleted} inregistrari expirate."))
```

# apps/planificator/management/commands/purge_expired_schedule_generations.py

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `apps/planificator/management/commands/purge_expired_schedule_generations.py`
- App: `planificator`
- App guide: `codex-context/apps/planificator.md`
- Role: `backend`
- Size: 462 bytes
- Source SHA-256: `34f1eadf8c3a0b4496050f8a0831755514e83586c3967f4ac2a154a5639f55d6`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

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

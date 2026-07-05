# apps/planificator/models.py

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `apps/planificator/models.py`
- App: `planificator`
- App guide: `codex-context/apps/planificator.md`
- Role: `backend`
- Size: 2612 bytes
- Source SHA-256: `a520453710d73fd45b71d40532b63801ba1f1cb96b9088b5b7fd83016d7a4bbc`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
import uuid

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone


class AppSetting(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="planificator_settings",
        blank=True,
        null=True,
    )
    scope = models.CharField(max_length=100)
    payload = models.JSONField(default=dict)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ("use_course_planning", "Can use schedule generator"),
            ("use_word_matcher", "Can use Word date matcher"),
            ("use_xml_export", "Can use XML export"),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=("scope",),
                condition=Q(user__isnull=True),
                name="unique_global_planificator_setting",
            ),
            models.UniqueConstraint(
                fields=("user", "scope"),
                condition=Q(user__isnull=False),
                name="unique_user_planificator_setting",
            ),
        ]

    def __str__(self) -> str:
        owner = self.user.get_username() if self.user_id else "global"
        return f"{self.scope} ({owner})"


class ScheduleGeneration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="schedule_generations",
    )
    year = models.PositiveSmallIntegerField()
    selected_months = models.JSONField(default=list)
    holidays = models.JSONField(default=list)
    random_seed = models.PositiveBigIntegerField()
    schedule = models.JSONField(default=list)
    source_course_count = models.PositiveIntegerField()
    generated_entry_count = models.PositiveIntegerField()
    source_file_name = models.CharField(max_length=255)
    source_file_digest = models.CharField(max_length=64)
    source_file_data = models.BinaryField(default=bytes, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(db_index=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=("owner", "created_at"), name="plan_gen_owner_created"),
        ]

    @property
    def is_expired(self) -> bool:
        return self.expires_at <= timezone.now()

    def __str__(self) -> str:
        return f"{self.source_file_name} — {self.owner} — {self.year}"
```

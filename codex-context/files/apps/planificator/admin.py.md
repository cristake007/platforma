# apps/planificator/admin.py

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `apps/planificator/admin.py`
- App: `planificator`
- App guide: `codex-context/apps/planificator.md`
- Role: `backend`
- Size: 1146 bytes
- Source SHA-256: `5f10530dc702b7533fd879dd26c2431ebfac609417341db06a0ca69e7bb1856a`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from django.contrib import admin

from .models import AppSetting, ScheduleGeneration


@admin.register(AppSetting)
class AppSettingAdmin(admin.ModelAdmin):
    list_display = ("scope", "user", "updated_at")
    list_filter = ("scope",)
    search_fields = ("scope", "user__username")


@admin.register(ScheduleGeneration)
class ScheduleGenerationAdmin(admin.ModelAdmin):
    exclude = ("schedule",)
    list_display = (
        "source_file_name",
        "owner",
        "year",
        "source_course_count",
        "generated_entry_count",
        "created_at",
        "expires_at",
    )
    list_filter = ("year", "created_at", "expires_at")
    search_fields = ("source_file_name", "source_file_digest", "owner__username")
    readonly_fields = (
        "id",
        "owner",
        "year",
        "selected_months",
        "holidays",
        "random_seed",
        "source_course_count",
        "generated_entry_count",
        "source_file_name",
        "source_file_digest",
        "created_at",
        "expires_at",
    )

    def get_queryset(self, request):
        return super().get_queryset(request).defer("schedule")
```

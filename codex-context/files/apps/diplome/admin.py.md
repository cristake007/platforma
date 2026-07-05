# apps/diplome/admin.py

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `apps/diplome/admin.py`
- App: `diplome`
- App guide: `codex-context/apps/diplome.md`
- Role: `backend`
- Size: 3652 bytes
- Source SHA-256: `4b103d54d83f3782f0b76df952decd641d44200de34c981a75ae6ab134cc8b44`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from django.contrib import admin

from .models import (
    DiplomaGenerationBatch,
    DiplomaTemplate,
    GeneratedDiploma,
    Participant,
    ParticipantImportDraft,
    ParticipantList,
)


@admin.register(DiplomaTemplate)
class DiplomaTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "owner", "page_size", "orientation", "is_active", "updated_at")
    list_filter = ("category", "is_active", "page_size", "orientation", "updated_at")
    search_fields = (
        "name",
        "category",
        "description",
        "owner__username",
        "owner__first_name",
        "owner__last_name",
    )
    readonly_fields = ("id", "created_at", "updated_at")
    list_select_related = ("owner",)


@admin.register(ParticipantList)
class ParticipantListAdmin(admin.ModelAdmin):
    list_display = ("name", "course_name", "owner", "participant_count", "updated_at")
    search_fields = ("name", "course_name", "source_file_name", "owner__username")
    readonly_fields = ("id", "participant_count", "created_at", "updated_at")
    list_select_related = ("owner",)


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "certificate_number",
        "participant_list",
        "owner",
        "source_row",
    )
    search_fields = (
        "full_name",
        "certificate_number",
        "participant_list__name",
        "owner__username",
    )
    readonly_fields = ("id", "created_at", "updated_at")
    list_select_related = ("owner", "participant_list")


@admin.register(ParticipantImportDraft)
class ParticipantImportDraftAdmin(admin.ModelAdmin):
    list_display = ("list_name", "source_file_name", "owner", "created_at", "expires_at")
    search_fields = ("list_name", "source_file_name", "owner__username")
    readonly_fields = ("id", "created_at")
    list_select_related = ("owner",)


@admin.register(GeneratedDiploma)
class GeneratedDiplomaAdmin(admin.ModelAdmin):
    list_display = (
        "participant_name",
        "certificate_number",
        "participant_list_display_name",
        "template_display_name",
        "owner",
        "created_at",
    )
    search_fields = (
        "participant_name",
        "certificate_number",
        "participant_list_name",
        "template_name",
        "participant_list__name",
        "template__name",
        "owner__username",
    )
    readonly_fields = (
        "id",
        "certificate_number",
        "participant_name",
        "participant_list_name",
        "template_name",
        "pdf_file",
        "created_at",
        "updated_at",
    )
    list_select_related = ("owner", "participant_list", "participant", "template", "batch")


@admin.register(DiplomaGenerationBatch)
class DiplomaGenerationBatchAdmin(admin.ModelAdmin):
    list_display = (
        "participant_list_display_name",
        "template_display_name",
        "owner",
        "status",
        "success_count",
        "failed_count",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = (
        "participant_list_name",
        "template_name",
        "participant_list__name",
        "template__name",
        "owner__username",
    )
    readonly_fields = (
        "id",
        "status",
        "total_count",
        "success_count",
        "failed_count",
        "participant_list_name",
        "template_name",
        "output_folder",
        "error_summary",
        "created_at",
        "updated_at",
        "started_at",
        "completed_at",
    )
    list_select_related = ("owner", "participant_list", "template")
```

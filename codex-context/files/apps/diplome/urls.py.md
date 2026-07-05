# apps/diplome/urls.py

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `apps/diplome/urls.py`
- App: `diplome`
- App guide: `codex-context/apps/diplome.md`
- Role: `backend`
- Size: 3645 bytes
- Source SHA-256: `621e353c5d973916ceb6a67049fc19b9f9574e0eb75af9732a8b8dc1d005e828`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from django.urls import path

from .views import (
    BulkDiplomaGenerationCreateView,
    DiplomaGenerationBatchDetailView,
    DiplomaGenerationBatchResumeView,
    DiplomaGenerationBatchZipDownloadView,
    DiplomaGenerationCreateView,
    DiplomaGenerationDownloadView,
    DiplomaGenerationHistoryView,
    DiplomaGenerationIndexView,
    DiplomaGenerationPreviewView,
    DiplomaTemplateCreateView,
    DiplomaTemplateDeleteView,
    DiplomaTemplateEditorView,
    DiplomaTemplateListView,
    DiplomaTemplatePreviewView,
    ParticipantImportConfirmView,
    ParticipantImportMappingView,
    ParticipantImportPreviewView,
    ParticipantImportSheetView,
    ParticipantImportView,
    ParticipantListDeleteView,
    ParticipantListDetailView,
    ParticipantListView,
)


app_name = "diplome"

urlpatterns = [
    path("generare/", DiplomaGenerationIndexView.as_view(), name="generation_index"),
    path(
        "generare/preview/",
        DiplomaGenerationPreviewView.as_view(),
        name="generation_preview",
    ),
    path(
        "generare/creeaza/",
        DiplomaGenerationCreateView.as_view(),
        name="generation_create",
    ),
    path(
        "generare/lot/",
        BulkDiplomaGenerationCreateView.as_view(),
        name="generation_bulk_create",
    ),
    path(
        "generare/<uuid:generated_diploma_id>/download/",
        DiplomaGenerationDownloadView.as_view(),
        name="generation_download",
    ),
    path("liste/", ParticipantListView.as_view(), name="list_index"),
    path("liste/nou/", ParticipantImportView.as_view(), name="participant_import"),
    path(
        "liste/import/<uuid:draft_id>/foaie/",
        ParticipantImportSheetView.as_view(),
        name="participant_import_sheet",
    ),
    path(
        "liste/import/<uuid:draft_id>/coloane/",
        ParticipantImportMappingView.as_view(),
        name="participant_import_mapping",
    ),
    path(
        "liste/import/<uuid:draft_id>/",
        ParticipantImportPreviewView.as_view(),
        name="participant_import_preview",
    ),
    path(
        "liste/import/<uuid:draft_id>/confirma/",
        ParticipantImportConfirmView.as_view(),
        name="participant_import_confirm",
    ),
    path(
        "liste/<uuid:participant_list_id>/",
        ParticipantListDetailView.as_view(),
        name="participant_list_detail",
    ),
    path(
        "liste/<uuid:participant_list_id>/sterge/",
        ParticipantListDeleteView.as_view(),
        name="participant_list_delete",
    ),
    path("template-uri/", DiplomaTemplateListView.as_view(), name="template_list"),
    path("template-uri/nou/", DiplomaTemplateCreateView.as_view(), name="template_create"),
    path(
        "template-uri/<uuid:template_id>/editor/",
        DiplomaTemplateEditorView.as_view(),
        name="template_editor",
    ),
    path(
        "template-uri/<uuid:template_id>/preview/",
        DiplomaTemplatePreviewView.as_view(),
        name="template_preview",
    ),
    path(
        "template-uri/<uuid:template_id>/sterge/",
        DiplomaTemplateDeleteView.as_view(),
        name="template_delete",
    ),
    path("istoric/", DiplomaGenerationHistoryView.as_view(), name="history_index"),
    path(
        "istoric/<uuid:batch_id>/",
        DiplomaGenerationBatchDetailView.as_view(),
        name="batch_detail",
    ),
    path(
        "istoric/<uuid:batch_id>/zip/",
        DiplomaGenerationBatchZipDownloadView.as_view(),
        name="batch_zip_download",
    ),
    path(
        "istoric/<uuid:batch_id>/reia/",
        DiplomaGenerationBatchResumeView.as_view(),
        name="batch_resume",
    ),
]
```

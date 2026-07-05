# apps/planificator/urls.py

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `apps/planificator/urls.py`
- App: `planificator`
- App guide: `codex-context/apps/planificator.md`
- Role: `backend`
- Size: 2332 bytes
- Source SHA-256: `b7b45bccdc778465c38fda3ca014317eaa1cacde378f8389c140d31e58d30634`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from django.urls import path

from .views import (
    CourseRefreshView,
    CourseRefreshConnectView,
    CourseRefreshFetchDatesView,
    CourseRefreshPreviewView,
    CourseRefreshResolveView,
    CourseRefreshUpdateRowView,
    PeriodGeneratorView,
    ScheduleExportView,
    ScheduleHistoryDetailView,
    ScheduleHistoryView,
    ScheduleResultView,
    ScheduleSampleCsvView,
    WordConverterView,
    WordMatchGenerateView,
    WordMatchPreviewView,
    XmlExportView,
    XmlFormatterView,
)

app_name = 'planificator'

urlpatterns = [
    path('generator-perioade/', PeriodGeneratorView.as_view(), name='generator_perioade'),
    path(
        'generator-perioade/rezultat/<uuid:generation_id>/',
        ScheduleResultView.as_view(),
        name='generator_perioade_result',
    ),
    path('generator-perioade/model-csv/', ScheduleSampleCsvView.as_view(), name='generator_perioade_sample_csv'),
    path('generator-perioade/export/', ScheduleExportView.as_view(), name='generator_perioade_export'),
    path('actualizeaza-cursuri/', CourseRefreshView.as_view(), name='actualizeaza_cursuri'),
    path('actualizeaza-cursuri/preview/', CourseRefreshPreviewView.as_view(), name='actualizeaza_cursuri_preview'),
    path('actualizeaza-cursuri/connect/', CourseRefreshConnectView.as_view(), name='actualizeaza_cursuri_connect'),
    path('actualizeaza-cursuri/resolve-post-id/', CourseRefreshResolveView.as_view(), name='actualizeaza_cursuri_resolve'),
    path('actualizeaza-cursuri/fetch-current-dates/', CourseRefreshFetchDatesView.as_view(), name='actualizeaza_cursuri_fetch_dates'),
    path('actualizeaza-cursuri/update-row/', CourseRefreshUpdateRowView.as_view(), name='actualizeaza_cursuri_update_row'),
    path('convertor-xml/', XmlFormatterView.as_view(), name='xml_formatter'),
    path('convertor-xml/generate/', XmlExportView.as_view(), name='xml_export'),
    path('convertor-word/', WordConverterView.as_view(), name='word_converter'),
    path('convertor-word/preview/', WordMatchPreviewView.as_view(), name='word_match_preview'),
    path('convertor-word/generate/', WordMatchGenerateView.as_view(), name='word_match_generate'),
    path('istoric/', ScheduleHistoryView.as_view(), name='istoric'),
    path('istoric/<uuid:generation_id>/', ScheduleHistoryDetailView.as_view(), name='istoric_detail'),
]
```

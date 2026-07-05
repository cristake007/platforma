# apps/planificator/presentation.py

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `apps/planificator/presentation.py`
- App: `planificator`
- App guide: `codex-context/apps/planificator.md`
- Role: `backend`
- Size: 1665 bytes
- Source SHA-256: `246ac9242b0d6badd60524d9676519c6519fbba55af06b663d311fc7ee6693a3`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from collections import OrderedDict

from .constants import ROMANIAN_MONTH_NAMES


def build_preview_rows(schedule: list[dict], months: list[int]) -> list[dict]:
    preview: OrderedDict[int, dict] = OrderedDict()
    for item in sorted(schedule, key=lambda row: (row.get("original_order", 0), row["month"])):
        identity = int(item["source_row"])
        if identity not in preview:
            preview[identity] = {
                "source_row": identity,
                "Title": item["Title"],
                "Permalink": item.get("Permalink", ""),
                "duration_label": item.get("Durata Curs", ""),
                "investitie": item.get("investitie", ""),
                "months_map": {month: "" for month in months},
            }
        preview[identity]["months_map"][int(item["month"])] = item["date_range"]
    return [
        {**row, "months": [row["months_map"][month] for month in months]}
        for row in preview.values()
    ]


def build_source_preview(schedule: list[dict]) -> list[dict]:
    rows: OrderedDict[int, dict] = OrderedDict()
    for item in sorted(schedule, key=lambda row: row.get("original_order", 0)):
        identity = int(item["source_row"])
        rows.setdefault(
            identity,
            {
                "title": item["Title"],
                "duration_label": item.get("Durata Curs", ""),
                "investitie": item.get("investitie", ""),
                "permalink": item.get("Permalink", ""),
            },
        )
    return list(rows.values())[:10]


def selected_month_headers(months: list[int]) -> list[str]:
    return [ROMANIAN_MONTH_NAMES[month] for month in months]
```

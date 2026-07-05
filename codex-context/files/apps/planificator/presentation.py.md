# Source snapshot

## `apps/planificator/presentation.py`

Size: 1.6 KB

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

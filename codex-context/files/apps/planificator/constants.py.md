# apps/planificator/constants.py

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `apps/planificator/constants.py`
- App: `planificator`
- App guide: `codex-context/apps/planificator.md`
- Role: `backend`
- Size: 301 bytes
- Source SHA-256: `9a369c09a6aa04efc7b4bc5b742777f3178959f747d6225ac784fe233bcb96d3`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
ROMANIAN_MONTH_NAMES = {
    1: "Ianuarie",
    2: "Februarie",
    3: "Martie",
    4: "Aprilie",
    5: "Mai",
    6: "Iunie",
    7: "Iulie",
    8: "August",
    9: "Septembrie",
    10: "Octombrie",
    11: "Noiembrie",
    12: "Decembrie",
}

MONTH_CHOICES = tuple(ROMANIAN_MONTH_NAMES.items())
```

# apps/tasks/signals.py

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `apps/tasks/signals.py`
- App: `tasks`
- App guide: `codex-context/apps/tasks.md`
- Role: `backend`
- Size: 90 bytes
- Source SHA-256: `c3563b8f2bb322452a8afde128087ada4a208ec01b13010a15ff43b7be8a8a31`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from django.dispatch import Signal


task_assigned = Signal()
task_reassigned = Signal()
```

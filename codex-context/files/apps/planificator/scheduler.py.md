# apps/planificator/scheduler.py

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `apps/planificator/scheduler.py`
- App: `planificator`
- App guide: `codex-context/apps/planificator.md`
- Role: `backend`
- Size: 2796 bytes
- Source SHA-256: `e0c1d554e3ae827228a92bf30121188cf6bbbf052346d2c44ffb0cf57dc0678d`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
import calendar
from datetime import datetime, timedelta


class CourseScheduler:
    def __init__(self, year: int, holidays: list[str]):
        self.year = year
        self.holidays = {datetime.strptime(holiday, "%d.%m.%Y").date() for holiday in holidays}
        self._available_dates_cache: dict[tuple[int, int], tuple[datetime, ...]] = {}
        self.available_date_calculations = 0

    def is_holiday(self, date: datetime) -> bool:
        return date.date() in self.holidays

    def is_business_day(self, date: datetime) -> bool:
        if date.weekday() >= 5:
            return False
        return not self.is_holiday(date)

    def can_schedule_course(self, start_date: datetime, duration: int) -> bool:
        if not self.is_business_day(start_date):
            return False

        current_date = start_date
        business_days = 0
        allow_cross_period = duration > 5
        week_start = start_date - timedelta(days=start_date.weekday())

        while business_days < duration:
            if self.is_holiday(current_date):
                return False

            if not allow_cross_period:
                if current_date - week_start >= timedelta(days=5):
                    return False
                if current_date.month != start_date.month:
                    return False

            if self.is_business_day(current_date):
                business_days += 1
            current_date += timedelta(days=1)

        return True

    def get_available_start_days(self, month: int, duration: int) -> tuple[datetime, ...]:
        cache_key = (month, duration)
        if cache_key in self._available_dates_cache:
            return self._available_dates_cache[cache_key]

        self.available_date_calculations += 1
        available_dates = []
        _, last_day = calendar.monthrange(self.year, month)
        current_date = datetime(self.year, month, 1)
        end_date = datetime(self.year, month, last_day)

        while current_date <= end_date:
            if self.can_schedule_course(current_date, duration):
                available_dates.append(current_date)
            current_date += timedelta(days=1)

        result = tuple(available_dates)
        self._available_dates_cache[cache_key] = result
        return result

    def format_date_range(self, start_date: datetime, duration: int) -> str:
        if duration == 1:
            return start_date.strftime("%d.%m.%Y")

        business_days = 0
        current_date = start_date
        while business_days < duration:
            if self.is_business_day(current_date):
                business_days += 1
            if business_days < duration:
                current_date += timedelta(days=1)

        return f"{start_date.strftime('%d')}-{current_date.strftime('%d.%m.%Y')}"
```

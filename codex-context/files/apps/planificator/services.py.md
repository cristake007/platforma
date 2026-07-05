# Source snapshot

## `apps/planificator/services.py`

Size: 8.0 KB

```python
import hashlib
import random
import secrets
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path

from django.utils import timezone

from .constants import ROMANIAN_MONTH_NAMES
from .file_handlers import CourseInputRow, read_input_file
from .models import ScheduleGeneration
from .scheduler import CourseScheduler
from .selectors import get_owned_generation
from .settings_store import save_settings
from .validators import ClientInputError


@dataclass
class ScheduleGenerationResult:
    schedule: list[dict]
    unscheduled_courses: dict[int, list[str]]
    source_courses: list[CourseInputRow]
    random_seed: int
    calendar_calculations: int


@dataclass(frozen=True)
class GenerationWorkflowResult:
    source_file_name: str
    generation: ScheduleGeneration | None = None
    unscheduled_courses: dict[int, list[str]] | None = None


class GenerationSourceUnavailable(ClientInputError):
    pass


class GenerationWorkflowError(ClientInputError):
    def __init__(self, message: str, *, source_file_name: str, status: int = 400):
        super().__init__(message, status=status)
        self.source_file_name = source_file_name


def create_schedule_generation(
    *,
    owner,
    upload,
    source_generation_id,
    year: int,
    months: list[int],
    randomness: int,
    holidays: list[str],
) -> GenerationWorkflowResult:
    if upload:
        file_bytes = upload.read()
        source_file_name = upload.name
    else:
        source_generation = get_owned_generation(
            generation_id=source_generation_id,
            user=owner,
        )
        file_bytes = bytes(source_generation.source_file_data)
        source_file_name = source_generation.source_file_name
        if not file_bytes:
            raise GenerationSourceUnavailable(
                "Fișierul original nu mai este disponibil. Încarcă-l din nou."
            )

    save_settings(
        "schedule_generator",
        owner,
        {
            "year": year,
            "months": months,
            "randomness": randomness,
            "holidays": holidays,
        },
    )

    try:
        result = generate_schedule_from_upload(
            file_bytes=file_bytes,
            file_extension=Path(source_file_name).suffix.lower(),
            year=year,
            months=months,
            randomness=randomness,
            holidays=holidays,
            random_seed=secrets.randbits(63),
        )
        if result.unscheduled_courses:
            return GenerationWorkflowResult(
                source_file_name=source_file_name,
                unscheduled_courses=result.unscheduled_courses,
            )
        generation = persist_generation(
            owner=owner,
            result=result,
            year=year,
            months=months,
            holidays=holidays,
            source_file_name=source_file_name,
            file_bytes=file_bytes,
        )
    except ClientInputError as exc:
        raise GenerationWorkflowError(
            exc.message,
            source_file_name=source_file_name,
            status=exc.status,
        ) from exc

    return GenerationWorkflowResult(
        source_file_name=source_file_name,
        generation=generation,
    )


def generate_schedule_from_upload(
    *,
    file_bytes: bytes,
    file_extension: str,
    year: int,
    months: list[int],
    randomness: int,
    holidays: list[str],
    random_seed: int,
) -> ScheduleGenerationResult:
    source_courses = read_input_file(file_bytes, file_extension)
    scheduler = CourseScheduler(year, holidays)
    rng = random.Random(random_seed)
    schedule: list[dict] = []
    unscheduled_courses: dict[int, list[str]] = {}

    for month in months:
        scheduled_dates: set = set()
        missing: list[str] = []
        for course in source_courses:
            available_dates = scheduler.get_available_start_days(month, course.duration)
            if not available_dates:
                missing.append(f"{course.title} (rândul {course.source_row})")
                continue
            start_date = choose_start_date(
                available_dates=available_dates,
                scheduled_dates=scheduled_dates,
                randomness=randomness,
                duration=course.duration,
                rng=rng,
            )
            schedule.append(
                {
                    "source_row": course.source_row,
                    "original_order": course.original_order,
                    "Title": course.title,
                    "Permalink": course.permalink,
                    "Durata Curs": course.duration_label,
                    "duration_label": course.duration_label,
                    "investitie": course.investment,
                    "date_range": scheduler.format_date_range(start_date, course.duration),
                    "month": month,
                    "month_name": ROMANIAN_MONTH_NAMES[month],
                }
            )
            scheduled_dates.add(start_date)
        if missing:
            unscheduled_courses[month] = missing

    schedule.sort(key=lambda item: (item["original_order"], item["month"]))
    if not unscheduled_courses:
        validate_schedule_completeness(schedule, source_courses, months)
    return ScheduleGenerationResult(
        schedule=schedule,
        unscheduled_courses=unscheduled_courses,
        source_courses=source_courses,
        random_seed=random_seed,
        calendar_calculations=scheduler.available_date_calculations,
    )


def validate_schedule_completeness(
    schedule: list[dict], source_courses: list[CourseInputRow], months: list[int]
) -> None:
    expected = {(course.source_row, month) for course in source_courses for month in months}
    actual = {(int(item["source_row"]), int(item["month"])) for item in schedule}
    if len(schedule) != len(expected) or actual != expected:
        raise ClientInputError("Programul generat este incomplet; niciun rezultat parțial nu a fost salvat.")
    if any(not str(item.get("date_range", "")).strip() for item in schedule):
        raise ClientInputError("Programul generat conține perioade goale.")


def persist_generation(
    *, owner, result: ScheduleGenerationResult, year: int, months: list[int], holidays: list[str],
    source_file_name: str, file_bytes: bytes,
) -> ScheduleGeneration:
    if result.unscheduled_courses:
        raise ClientInputError("Programul incomplet nu poate fi salvat.")
    validate_schedule_completeness(result.schedule, result.source_courses, months)
    now = timezone.now()
    ScheduleGeneration.objects.filter(expires_at__lte=now).delete()
    return ScheduleGeneration.objects.create(
        owner=owner,
        year=year,
        selected_months=months,
        holidays=holidays,
        random_seed=result.random_seed,
        schedule=result.schedule,
        source_course_count=len(result.source_courses),
        generated_entry_count=len(result.schedule),
        source_file_name=Path(source_file_name).name[:255],
        source_file_digest=hashlib.sha256(file_bytes).hexdigest(),
        source_file_data=file_bytes,
        expires_at=now + timedelta(hours=24),
    )


def choose_start_date(*, available_dates, scheduled_dates: set, randomness: int, duration: int, rng=None):
    rng = rng or random
    min_gap = max(1, 11 - randomness)
    filtered_dates = [
        date for date in available_dates
        if not any(abs((date - scheduled).days) < min_gap for scheduled in scheduled_dates)
    ]
    dates_to_use = filtered_dates if filtered_dates else list(available_dates)
    if duration > 5:
        return min(dates_to_use)
    if randomness > 7:
        return rng.choice(dates_to_use)

    number_of_dates = len(dates_to_use)
    weights = []
    for index in range(number_of_dates):
        if randomness <= 3:
            weight = 0.5 if index < 5 else 1.0
        elif randomness <= 6:
            midpoint = number_of_dates // 2
            weight = 1.0 - (abs(index - midpoint) / number_of_dates) * 0.5
        else:
            weight = 0.8 + rng.random() * 0.4
        weights.append(weight)
    return rng.choices(dates_to_use, weights=weights, k=1)[0]
```

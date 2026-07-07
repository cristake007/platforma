# Django app: planificator

Migrations are excluded by default. Tests are included unless `--no-tests` is used.

## `apps/planificator/__init__.py`

Size: 1 B

```python

```

## `apps/planificator/admin.py`

Size: 1.1 KB

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

## `apps/planificator/AGENTS.md`

Size: 3.2 KB

````markdown
# Planificator App Instructions

## Scope and workflows

This app owns schedule generation/history/export, Word matching, XML export, and WordPress course-date updates.

These are separate workflows sharing permissions, input utilities, settings, and app navigation.

## Read before editing

- Root `AGENTS.md`.
- `coding-standards.md`.
- `frontend.md` for UI/template work.
- This file.
- Only the files for the selected workflow.

Use `codex-context/apps/planificator.md` only when a path is unknown.

Do not read every converter and updater file for a task confined to one workflow.

## Minimal routing

- Schedule generation/history/export: `forms.py`, `file_handlers.py`, `scheduler.py`, `services.py`, `selectors.py`, `presentation.py`, affected views/templates/static, then `tests.py` or `tests_scheduler.py`.
- Word matching/conversion: `word_matching.py`, relevant forms/views/template/JavaScript, then `tests_word_converter.py`.
- XML conversion: `xml_export.py`, relevant forms/views/template/JavaScript, then `tests_xml_export.py`.
- WordPress course updater: `wp_course_updater.py`, validators, affected views/template/JavaScript, then `tests_course_updater.py`.
- Persisted settings or generation models: `models.py`, `settings_store.py` or selectors/services, focused tests, then relevant migrations.
- Expiry cleanup: the model plus `management/commands/purge_expired_schedule_generations.py` and cleanup tests.

## Domain and security contracts

- Enforce workflow-specific permissions already represented by view mixins and model permissions.
- Persisted generations and settings are owner-scoped.
- Foreign or expired generation access must follow existing 404/error behavior.
- Uploaded CSV/XLSX/DOCX and JSON are untrusted.
- Keep size, extension, schema, date, and index validation server-side.
- Preserve schedule constraints and stable export contracts.
- Neutralize spreadsheet formulas in generated files.
- WordPress URL handling must keep the existing public HTTP(S), DNS, redirect, and bounded-network protections.
- Do not persist secrets from the updater.
- Store only non-secret settings explicitly supported by `settings_store.py`.
- Use services for generation/persistence.
- Keep JSON endpoints method-restricted, CSRF-protected, and consistent in error shape.

## Reuse and UI standards

- Reuse existing generator includes before adding markup to the main template.
- Reuse existing message, action, table, and upload patterns.
- Large result and matching tables must remain horizontally usable on narrow screens.
- Preserve sticky columns/headers and native scrolling where present.
- Use sharp bordered panels and compact settings rows.
- Avoid rounded card-heavy generator/settings layouts.
- JavaScript coordinates uploads, previews, and downloads only; server validation remains authoritative.

## Focused checks

```powershell
python manage.py test apps.planificator.tests_scheduler
python manage.py test apps.planificator.tests_word_converter
python manage.py test apps.planificator.tests_xml_export
python manage.py test apps.planificator.tests_course_updater
python manage.py test apps.planificator
```

Use the smallest matching module. Use the full app command only for cross-workflow changes.
````

## `apps/planificator/apps.py`

Size: 104 B

```python
from django.apps import AppConfig


class PlanificatorConfig(AppConfig):
    name = 'apps.planificator'
```

## `apps/planificator/constants.py`

Size: 301 B

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

## `apps/planificator/file_handlers.py`

Size: 7.4 KB

```python
import csv
import io
import math
import re
from dataclasses import dataclass

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from openpyxl import Workbook, load_workbook
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
from openpyxl.utils import get_column_letter

from .constants import ROMANIAN_MONTH_NAMES
from .validators import ClientInputError, MAX_COURSE_ROWS, MAX_TABULAR_COLUMNS

REQUIRED_COLUMNS = {
    "title": "Title",
    "durata curs": "Durata Curs",
    "permalink": "Permalink",
}
URL_VALIDATOR = URLValidator(schemes=("http", "https"))
FORMULA_PREFIXES = ("=", "+", "-", "@")


@dataclass(frozen=True)
class CourseInputRow:
    source_row: int
    original_order: int
    title: str
    duration_label: str
    duration: int
    permalink: str
    investment: str = ""


def _detect_csv_delimiter(text: str) -> str:
    sample = text[:8192]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;|\t@")
        return str(dialect.delimiter)
    except csv.Error:
        for delimiter in ("@", ";", "\t", "|", ","):
            if delimiter in sample.partition("\n")[0]:
                return delimiter
        return ","


def _stringify(value) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and math.isnan(value):
        return ""
    return str(value).strip()


def read_tabular_rows(file_data: bytes, file_extension: str) -> list[list]:
    if file_extension == ".csv":
        try:
            text = file_data.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            raise ClientInputError("Fișierul CSV trebuie să folosească UTF-8.") from exc
        return list(csv.reader(io.StringIO(text, newline=""), delimiter=_detect_csv_delimiter(text)))

    if file_extension != ".xlsx" or not file_data.startswith(b"PK"):
        raise ClientInputError("Fișierul XLSX nu are o structură validă.")
    try:
        workbook = load_workbook(io.BytesIO(file_data), read_only=True, data_only=True)
        sheet = workbook.active
        rows = [list(row) for row in sheet.iter_rows(values_only=True)]
        workbook.close()
        return rows
    except Exception as exc:
        raise ClientInputError("Fișierul XLSX nu a putut fi citit.") from exc


def read_input_file(file_data: bytes, file_extension: str) -> list[CourseInputRow]:
    raw_rows = read_tabular_rows(file_data, file_extension.lower())
    if not raw_rows:
        raise ClientInputError("Fișierul nu conține un antet.")

    header = [_stringify(value) for value in raw_rows[0]]
    if len(header) > MAX_TABULAR_COLUMNS:
        raise ClientInputError(f"Fișierul poate avea cel mult {MAX_TABULAR_COLUMNS} coloane.")
    normalized = {name.strip().lower(): index for index, name in enumerate(header) if name.strip()}
    missing = [canonical for source, canonical in REQUIRED_COLUMNS.items() if source not in normalized]
    if missing:
        raise ClientInputError("Lipsesc coloanele obligatorii: " + ", ".join(missing))

    column_indexes = {canonical: normalized[source] for source, canonical in REQUIRED_COLUMNS.items()}
    investment_index = normalized.get("investitie")
    courses: list[CourseInputRow] = []

    for source_row, raw_row in enumerate(raw_rows[1:], start=2):
        if len(raw_row) > MAX_TABULAR_COLUMNS:
            raise ClientInputError(f"Rândul {source_row} depășește limita de coloane.")
        if not any(_stringify(value) for value in raw_row):
            continue
        if len(courses) >= MAX_COURSE_ROWS:
            raise ClientInputError(f"Fișierul poate conține cel mult {MAX_COURSE_ROWS} cursuri.", status=413)

        def cell(index: int | None) -> str:
            return _stringify(raw_row[index]) if index is not None and index < len(raw_row) else ""

        title = cell(column_indexes["Title"])
        duration_label = cell(column_indexes["Durata Curs"])
        permalink = cell(column_indexes["Permalink"])
        if not title:
            raise ClientInputError(f"Rândul {source_row}: Title este obligatoriu.")
        if not duration_label:
            raise ClientInputError(f"Rândul {source_row}: Durata Curs este obligatorie.")
        if not permalink:
            raise ClientInputError(f"Rândul {source_row}: Permalink este obligatoriu.")

        duration_match = re.search(r"(\d+)", duration_label)
        if not duration_match:
            raise ClientInputError(f"Rândul {source_row}: Durata Curs nu conține un număr valid.")
        duration = int(duration_match.group(1))
        if not 1 <= duration <= 366:
            raise ClientInputError(f"Rândul {source_row}: durata trebuie să fie între 1 și 366 zile.")
        try:
            URL_VALIDATOR(permalink)
        except ValidationError as exc:
            raise ClientInputError(f"Rândul {source_row}: Permalink trebuie să fie un URL HTTP(S) valid.") from exc

        courses.append(
            CourseInputRow(
                source_row=source_row,
                original_order=len(courses),
                title=title,
                duration_label=duration_label,
                duration=duration,
                permalink=permalink,
                investment=cell(investment_index),
            )
        )

    if not courses:
        raise ClientInputError("Fișierul nu conține niciun curs valid.")
    return courses


def safe_excel_text(value) -> str:
    clean = ILLEGAL_CHARACTERS_RE.sub("", _stringify(value))
    if clean.startswith(FORMULA_PREFIXES):
        return "'" + clean
    return clean


def create_excel_export(schedule: list[dict], year: int, holidays: list[str] | None = None) -> bytes:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Program"
    month_headers = [ROMANIAN_MONTH_NAMES[month] for month in range(1, 13)]
    headers = ["Title", "Permalink", "Durata Curs", "investitie", *month_headers]
    sheet.append(headers)

    course_rows: dict[int, dict] = {}
    for item in sorted(schedule, key=lambda row: (int(row.get("original_order", 0)), int(row["month"]))):
        identity = int(item.get("source_row", item.get("original_order", 0)))
        if identity not in course_rows:
            course_rows[identity] = {
                "original_order": int(item.get("original_order", 0)),
                "Title": item.get("Title", ""),
                "Permalink": item.get("Permalink", ""),
                "Durata Curs": item.get("Durata Curs", ""),
                "investitie": item.get("investitie", ""),
                **{month_name: "" for month_name in month_headers},
            }
        course_rows[identity][ROMANIAN_MONTH_NAMES[int(item["month"])]] = item.get("date_range", "")

    for course in sorted(course_rows.values(), key=lambda row: row["original_order"]):
        sheet.append([safe_excel_text(course[header]) for header in headers])

    if holidays:
        holiday_sheet = workbook.create_sheet("Zile nelucrătoare")
        holiday_sheet.append(["Data"])
        for holiday in holidays:
            holiday_sheet.append([safe_excel_text(holiday)])

    for workbook_sheet in workbook.worksheets:
        for index, column in enumerate(workbook_sheet.iter_cols(), start=1):
            maximum = max((len(str(cell.value or "")) for cell in column), default=0)
            workbook_sheet.column_dimensions[get_column_letter(index)].width = min(maximum + 2, 60)

    output = io.BytesIO()
    workbook.save(output)
    output.seek(0)
    return output.getvalue()
```

## `apps/planificator/forms.py`

Size: 9.4 KB

```python
from django import forms
from django.utils import timezone

from .constants import MONTH_CHOICES
from .validators import (
    MAX_TABULAR_UPLOAD_BYTES,
    MAX_WORD_UPLOAD_BYTES,
    TABULAR_EXTENSIONS,
    WORD_EXTENSIONS,
    ClientInputError,
    validate_holiday_list,
    validate_upload,
)
from .word_matching import decode_word_base64, validate_matches, validate_schedule_options


def schedule_year_bounds() -> tuple[int, int]:
    current_year = timezone.localdate().year
    return current_year - 1, current_year + 5


def normalize_schedule_initial(settings: dict) -> dict:
    minimum_year, maximum_year = schedule_year_bounds()
    current_year = timezone.localdate().year
    try:
        year = int(settings.get("year", current_year))
    except (TypeError, ValueError):
        year = current_year
    if not minimum_year <= year <= maximum_year:
        year = current_year

    raw_months = settings.get("months", [])
    months = []
    if isinstance(raw_months, (list, tuple)):
        for value in raw_months:
            try:
                month = int(value)
            except (TypeError, ValueError):
                continue
            if 1 <= month <= 12 and month not in months:
                months.append(month)

    try:
        randomness = int(settings.get("randomness", 5))
    except (TypeError, ValueError):
        randomness = 5
    if not 1 <= randomness <= 10:
        randomness = 5

    raw_holidays = settings.get("holidays", [])
    valid_holidays = []
    if isinstance(raw_holidays, (list, tuple)):
        for value in raw_holidays:
            try:
                valid_holidays.extend(validate_holiday_list([value]))
            except ClientInputError:
                continue

    return {
        "year": year,
        "months": months,
        "randomness": randomness,
        "holidays": "\n".join(valid_holidays),
    }


class ScheduleGeneratorForm(forms.Form):
    input_file = forms.FileField(
        label="Fișier sursă",
        help_text="CSV sau XLSX cu Title, Durata Curs, Permalink și, opțional, investitie.",
        required=False,
    )
    source_generation_id = forms.UUIDField(required=False, widget=forms.HiddenInput)
    year = forms.IntegerField()
    months = forms.TypedMultipleChoiceField(
        choices=MONTH_CHOICES,
        coerce=int,
        widget=forms.CheckboxSelectMultiple(
            attrs={"class": "checkbox checkbox-primary checkbox-xs"}
        ),
    )
    randomness = forms.IntegerField(
        min_value=1,
        max_value=10,
        initial=5,
        widget=forms.NumberInput(attrs={"type": "range"}),
    )
    holidays = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 3, "class": "textarea textarea-bordered w-full"}),
        help_text="Optional holiday dates in DD.MM.YYYY format, separated by commas or new lines.",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        minimum_year, maximum_year = schedule_year_bounds()
        self.fields["year"].widget = forms.Select(
            choices=[(year, year) for year in range(minimum_year, maximum_year + 1)],
            attrs={"class": "select select-primary select-sm w-full"},
        )
        self.fields["input_file"].widget.attrs.update(
            {"class": "file-input file-input-primary file-input-sm w-full", "accept": ".csv,.xlsx"}
        )
        self.fields["randomness"].widget.attrs.update({"class": "range range-primary range-xs w-full"})

    def clean_input_file(self):
        upload = self.cleaned_data.get("input_file")
        if upload is None:
            return None
        try:
            validate_upload(
                upload,
                allowed_extensions=TABULAR_EXTENSIONS,
                max_bytes=MAX_TABULAR_UPLOAD_BYTES,
                label="Fișierul sursă",
            )
        except ClientInputError as exc:
            self.upload_error_status = exc.status
            raise forms.ValidationError(exc.message) from exc
        return upload

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get("input_file") and not cleaned_data.get("source_generation_id"):
            self.add_error("input_file", "Selectează un fișier CSV sau XLSX pentru a continua.")
        return cleaned_data

    def clean_year(self):
        year = self.cleaned_data["year"]
        minimum_year, maximum_year = schedule_year_bounds()
        if not minimum_year <= year <= maximum_year:
            raise forms.ValidationError(f"Anul trebuie să fie între {minimum_year} și {maximum_year}.")
        return year

    def clean_holidays(self):
        raw_value = self.cleaned_data["holidays"]
        values = [
            item.strip()
            for item in raw_value.replace("\r", "\n").replace(",", "\n").split("\n")
            if item.strip()
        ]
        try:
            return validate_holiday_list(values)
        except ClientInputError as exc:
            raise forms.ValidationError(exc.message) from exc


class ScheduleExportForm(forms.Form):
    generation_id = forms.UUIDField(widget=forms.HiddenInput)


class SafeCoursePreviewForm(forms.Form):
    input_file = forms.FileField(
        label="Program sursă",
        widget=forms.ClearableFileInput(
            attrs={
                "class": "sr-only",
                "accept": ".csv,.xlsx",
            }
        ),
    )

    def clean_input_file(self):
        upload = self.cleaned_data["input_file"]
        try:
            self.file_extension = validate_upload(
                upload,
                allowed_extensions=TABULAR_EXTENSIONS,
                max_bytes=MAX_TABULAR_UPLOAD_BYTES,
                label="Fișierul de program",
            )
        except ClientInputError as exc:
            self.upload_error_status = exc.status
            raise forms.ValidationError(exc.message) from exc
        return upload


class XmlExportForm(forms.Form):
    input_file = forms.FileField(
        label="Program generat",
        widget=forms.ClearableFileInput(
            attrs={
                "class": "sr-only",
                "accept": ".csv,.xlsx",
            }
        ),
    )
    start_post_id = forms.IntegerField(
        label="Primul Post ID",
        min_value=1,
        max_value=2_147_483_647,
        initial=20000,
        widget=forms.NumberInput(
            attrs={
                "class": "input input-primary input-sm w-full",
                "inputmode": "numeric",
            }
        ),
    )

    def clean_input_file(self):
        upload = self.cleaned_data["input_file"]
        try:
            self.file_extension = validate_upload(
                upload,
                allowed_extensions=TABULAR_EXTENSIONS,
                max_bytes=MAX_TABULAR_UPLOAD_BYTES,
                label="Fișierul de program",
            )
        except ClientInputError as exc:
            self.upload_error_status = exc.status
            raise forms.ValidationError(exc.message) from exc
        return upload


class WordMatchUploadForm(forms.Form):
    word_file = forms.FileField(
        label="Document Word",
        widget=forms.ClearableFileInput(
            attrs={
                "class": "sr-only",
                "accept": ".docx",
            }
        ),
    )
    schedule_file = forms.FileField(
        label="Program generat",
        widget=forms.ClearableFileInput(
            attrs={
                "class": "sr-only",
                "accept": ".csv,.xlsx",
            }
        ),
    )

    def _validate_file(self, field_name, *, allowed_extensions, max_bytes, label):
        upload = self.cleaned_data[field_name]
        try:
            validate_upload(
                upload,
                allowed_extensions=allowed_extensions,
                max_bytes=max_bytes,
                label=label,
            )
        except ClientInputError as exc:
            self.upload_error_status = exc.status
            raise forms.ValidationError(exc.message) from exc
        return upload

    def clean_word_file(self):
        return self._validate_file(
            "word_file",
            allowed_extensions=WORD_EXTENSIONS,
            max_bytes=MAX_WORD_UPLOAD_BYTES,
            label="Documentul Word",
        )

    def clean_schedule_file(self):
        return self._validate_file(
            "schedule_file",
            allowed_extensions=TABULAR_EXTENSIONS,
            max_bytes=MAX_TABULAR_UPLOAD_BYTES,
            label="Fișierul de program",
        )


class WordMatchGenerationForm(forms.Form):
    word_file_b64 = forms.CharField(
        max_length=(MAX_WORD_UPLOAD_BYTES * 4 // 3) + 8,
        strip=True,
    )
    schedule_options = forms.JSONField()
    matches = forms.JSONField()

    def clean_word_file_b64(self):
        try:
            return decode_word_base64(self.cleaned_data["word_file_b64"])
        except ClientInputError as exc:
            self.validation_status = exc.status
            raise forms.ValidationError(exc.message) from exc

    def clean_schedule_options(self):
        try:
            return validate_schedule_options(self.cleaned_data["schedule_options"])
        except ClientInputError as exc:
            self.validation_status = exc.status
            raise forms.ValidationError(exc.message) from exc

    def clean_matches(self):
        try:
            return validate_matches(self.cleaned_data["matches"])
        except ClientInputError as exc:
            self.validation_status = exc.status
            raise forms.ValidationError(exc.message) from exc
```

## `apps/planificator/management/__init__.py`

Size: 1 B

```python

```

## `apps/planificator/management/commands/__init__.py`

Size: 1 B

```python

```

## `apps/planificator/management/commands/purge_expired_schedule_generations.py`

Size: 462 B

```python
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.planificator.models import ScheduleGeneration


class Command(BaseCommand):
    help = "Șterge generările de program expirate."

    def handle(self, *args, **options):
        deleted, _ = ScheduleGeneration.objects.filter(expires_at__lte=timezone.now()).delete()
        self.stdout.write(self.style.SUCCESS(f"Au fost sterse {deleted} inregistrari expirate."))
```

## `apps/planificator/models.py`

Size: 2.6 KB

```python
import uuid

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone


class AppSetting(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="planificator_settings",
        blank=True,
        null=True,
    )
    scope = models.CharField(max_length=100)
    payload = models.JSONField(default=dict)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ("use_course_planning", "Can use schedule generator"),
            ("use_word_matcher", "Can use Word date matcher"),
            ("use_xml_export", "Can use XML export"),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=("scope",),
                condition=Q(user__isnull=True),
                name="unique_global_planificator_setting",
            ),
            models.UniqueConstraint(
                fields=("user", "scope"),
                condition=Q(user__isnull=False),
                name="unique_user_planificator_setting",
            ),
        ]

    def __str__(self) -> str:
        owner = self.user.get_username() if self.user_id else "global"
        return f"{self.scope} ({owner})"


class ScheduleGeneration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="schedule_generations",
    )
    year = models.PositiveSmallIntegerField()
    selected_months = models.JSONField(default=list)
    holidays = models.JSONField(default=list)
    random_seed = models.PositiveBigIntegerField()
    schedule = models.JSONField(default=list)
    source_course_count = models.PositiveIntegerField()
    generated_entry_count = models.PositiveIntegerField()
    source_file_name = models.CharField(max_length=255)
    source_file_digest = models.CharField(max_length=64)
    source_file_data = models.BinaryField(default=bytes, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(db_index=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=("owner", "created_at"), name="plan_gen_owner_created"),
        ]

    @property
    def is_expired(self) -> bool:
        return self.expires_at <= timezone.now()

    def __str__(self) -> str:
        return f"{self.source_file_name} — {self.owner} — {self.year}"
```

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

## `apps/planificator/scheduler.py`

Size: 2.7 KB

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

## `apps/planificator/selectors.py`

Size: 986 B

```python
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import ScheduleGeneration


def list_owned_generations(*, user):
    return (
        ScheduleGeneration.objects.filter(
            owner=user,
            expires_at__gt=timezone.now(),
        )
        .only(
            "id",
            "year",
            "selected_months",
            "source_course_count",
            "generated_entry_count",
            "source_file_name",
            "source_file_digest",
            "created_at",
            "expires_at",
        )
        .order_by("-created_at")
    )


def get_owned_generation(*, generation_id, user) -> ScheduleGeneration:
    generation = get_object_or_404(
        ScheduleGeneration.objects.select_related("owner"),
        pk=generation_id,
        owner=user,
    )
    if generation.expires_at <= timezone.now():
        raise Http404("Generarea a expirat.")
    return generation
```

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

## `apps/planificator/settings_store.py`

Size: 1.7 KB

```python
import logging

from django.db import DatabaseError

from .models import AppSetting

logger = logging.getLogger(__name__)


DEFAULT_SETTINGS = {
    "schedule_generator": {
        "year": 2026,
        "months": [],
        "randomness": 5,
        "holidays": [],
        "xml_start_post_id": 20000,
    },
    "word_converter": {
        "min_match_score": 88,
        "min_token_coverage": 70,
        "min_match_gap": 8,
    },
    "safe_course_date_updater": {
        "wp_base_url": "",
        "wp_username": "",
    },
}


def get_settings(scope: str, user) -> dict:
    defaults = DEFAULT_SETTINGS.get(scope, {})
    try:
        global_setting = AppSetting.objects.filter(scope=scope, user__isnull=True).first()
        user_setting = AppSetting.objects.filter(scope=scope, user=user).first()
    except DatabaseError:
        logger.exception("Unable to load settings", extra={"scope": scope, "user_id": user.pk})
        raise

    global_payload = global_setting.payload if global_setting and isinstance(global_setting.payload, dict) else {}
    user_payload = user_setting.payload if user_setting and isinstance(user_setting.payload, dict) else {}
    return {**defaults, **global_payload, **user_payload}


def save_settings(scope: str, user, payload: dict) -> dict:
    current = get_settings(scope, user)
    merged = {**DEFAULT_SETTINGS.get(scope, {}), **current, **payload}
    try:
        AppSetting.objects.update_or_create(
            scope=scope,
            user=user,
            defaults={"payload": merged},
        )
    except DatabaseError:
        logger.exception("Unable to save settings", extra={"scope": scope, "user_id": user.pk})
        raise
    return merged
```

## `apps/planificator/static/planificator/course_updater.js`

Size: 16.4 KB

```javascript
(() => {
    const form = document.getElementById('course-updater-form');
    if (!form) {
        return;
    }

    const fileInput = document.getElementById('id_input_file');
    const fileSelect = document.getElementById('course-file-select');
    const fileName = document.getElementById('course-file-name');
    const fileError = document.getElementById('course-file-error');
    const previewButton = document.getElementById('course-preview-button');
    const errorAlert = document.getElementById('course-updater-error');
    const successAlert = document.getElementById('course-updater-success');
    const previewContainer = document.getElementById('course-preview-container');
    const previewCount = document.getElementById('course-preview-count');
    const table = document.getElementById('course-preview-table');
    const tableBody = document.getElementById('course-preview-table-body');
    const tableScroll = document.getElementById('course-preview-table-scroll');
    const topScroll = document.getElementById('course-preview-top-scroll');
    const topScrollInner = document.getElementById('course-preview-top-scroll-inner');
    const baseUrlInput = document.getElementById('wp-base-url');
    const usernameInput = document.getElementById('wp-username');
    const passwordInput = document.getElementById('wp-app-password');
    const connectButton = document.getElementById('wp-connect-button');
    const disconnectButton = document.getElementById('wp-disconnect-button');
    const connectionStatus = document.getElementById('wp-connection-status');

    let connected = false;
    let previewRows = [];
    let busy = false;

    function setHidden(element, hidden) {
        element.classList.toggle('hidden', hidden);
    }

    function clearMessages() {
        errorAlert.textContent = '';
        successAlert.textContent = '';
        setHidden(errorAlert, true);
        setHidden(successAlert, true);
    }

    function showError(message) {
        errorAlert.textContent = message;
        setHidden(errorAlert, false);
    }

    function showSuccess(message) {
        successAlert.textContent = message;
        setHidden(successAlert, false);
    }

    function setFileError(message) {
        fileError.textContent = message;
        setHidden(fileError, !message);
        fileInput.setAttribute('aria-invalid', message ? 'true' : 'false');
    }

    function csrfToken() {
        return form.querySelector('[name="csrfmiddlewaretoken"]')?.value || '';
    }

    function credentials() {
        return {
            wp_base_url: baseUrlInput.value.trim(),
            wp_username: usernameInput.value.trim(),
            wp_app_password: passwordInput.value.trim(),
        };
    }

    async function jsonRequest(url, payload) {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken(),
            },
            body: JSON.stringify(payload),
        });
        const data = await response.json().catch(() => ({}));
        if (!response.ok || !data.success) {
            throw new Error(data.error || 'Cererea nu a putut fi finalizată.');
        }
        return data;
    }

    function setConnectionState(isConnected, message = '') {
        connected = isConnected;
        connectButton.disabled = false;
        setHidden(connectButton, isConnected);
        setHidden(disconnectButton, !isConnected);
        connectionStatus.textContent = message || (isConnected ? 'Conectat' : 'Neconectat');
        connectionStatus.removeAttribute('title');
        connectionStatus.className = isConnected
            ? 'badge badge-outline badge-sm whitespace-nowrap border-success/40 bg-success/5 text-success'
            : 'badge badge-outline badge-sm whitespace-nowrap';
        if (previewRows.length) {
            renderRows();
        }
    }

    function setConnectionError(message) {
        connected = false;
        connectButton.disabled = false;
        setHidden(connectButton, false);
        setHidden(disconnectButton, true);
        connectionStatus.textContent = 'Conectarea a eșuat';
        connectionStatus.title = message || 'Conectarea a eșuat';
        connectionStatus.className = 'badge badge-outline badge-sm whitespace-nowrap border-error/40 bg-error/5 text-error';
        if (previewRows.length) {
            renderRows();
        }
    }

    function appendDateList(container, values, variant = 'neutral') {
        container.replaceChildren();
        if (!values?.length) {
            const empty = document.createElement('span');
            empty.className = 'text-xs text-muted';
            empty.textContent = '—';
            container.appendChild(empty);
            return;
        }
        const list = document.createElement('div');
        list.className = 'grid grid-cols-2 items-start gap-x-1 gap-y-0.5';
        values.forEach((value) => {
            const item = document.createElement('span');
            item.className = variant === 'primary'
                ? 'whitespace-nowrap rounded-field bg-primary/10 px-1 py-0 text-[11px] font-medium leading-4 text-primary'
                : 'whitespace-nowrap rounded-field bg-base-200 px-1 py-0 text-[11px] leading-4 text-base-content';
            item.textContent = value;
            list.appendChild(item);
        });
        container.appendChild(list);
    }

    function wpRequired() {
        const text = document.createElement('span');
        text.className = 'text-xs leading-5 text-muted';
        text.textContent = 'Necesită conexiune WordPress.';
        return text;
    }

    function actionButton(action, label, icon, style = 'outline') {
        const button = document.createElement('button');
        button.type = 'button';
        button.dataset.action = action;
        button.className = style === 'primary'
            ? 'btn btn-primary btn-xs'
            : 'btn btn-outline btn-xs';
        if (icon) {
            const iconElement = document.createElement('i');
            iconElement.className = `bi ${icon}`;
            iconElement.setAttribute('aria-hidden', 'true');
            button.appendChild(iconElement);
        }
        button.append(label);
        return button;
    }

    function renderCourseCell(cell, row) {
        const title = document.createElement('p');
        title.className = 'font-semibold leading-5 text-base-content';
        title.textContent = row.title || 'Curs fără titlu';
        cell.appendChild(title);
        if (row.slug) {
            const slug = document.createElement('code');
            slug.className = 'mt-1 block text-[11px] text-muted';
            slug.textContent = row.slug;
            cell.appendChild(slug);
        }
        const postId = document.createElement('span');
        postId.className = 'mt-1 block text-[11px] text-muted';
        postId.textContent = `Post ID: ${row.post_id || '—'}`;
        cell.appendChild(postId);
        if (row.permalink) {
            const link = document.createElement('a');
            link.className = 'link link-primary mt-1 block truncate text-xs';
            link.textContent = row.permalink;
            link.target = '_blank';
            link.rel = 'noopener noreferrer';
            try {
                const parsed = new URL(row.permalink);
                if (['http:', 'https:'].includes(parsed.protocol)) {
                    link.href = parsed.href;
                }
            } catch (_error) {
                link.removeAttribute('href');
            }
            cell.appendChild(link);
        }
    }

    function renderStatus(cell, row) {
        const status = document.createElement('span');
        const hasError = Boolean(row.error) || String(row.status || '').startsWith('error:');
        const succeeded = ['success', 'no changes', 'date preluate'].includes(row.status);
        status.className = hasError
            ? 'badge badge-outline badge-sm h-auto min-h-5 whitespace-normal border-error/40 bg-error/5 py-1 text-left text-error'
            : succeeded
                ? 'badge badge-outline badge-sm h-auto min-h-5 whitespace-normal border-success/40 bg-success/5 py-1 text-left text-success'
                : 'badge badge-outline badge-sm h-auto min-h-5 whitespace-normal py-1 text-left';
        status.textContent = row.error ? `eroare: ${row.error}` : (row.status || 'pregătit');
        cell.appendChild(status);
    }

    function renderRows() {
        tableBody.replaceChildren();
        previewRows.forEach((row, index) => {
            const tr = document.createElement('tr');
            tr.dataset.index = String(index);

            const courseCell = document.createElement('td');
            renderCourseCell(courseCell, row);

            const excelDatesCell = document.createElement('td');
            appendDateList(excelDatesCell, row.excel_dates, 'primary');

            const currentDatesCell = document.createElement('td');
            if (connected && row.current_dates_loaded) {
                appendDateList(currentDatesCell, row.existing_valid_dates);
            } else {
                currentDatesCell.appendChild(wpRequired());
            }

            const finalDatesCell = document.createElement('td');
            appendDateList(finalDatesCell, row.final_dates, 'primary');
            const details = document.createElement('details');
            details.className = 'mt-1 text-xs';
            const summary = document.createElement('summary');
            summary.className = 'cursor-pointer text-primary';
            summary.textContent = 'Payload';
            const payload = document.createElement('pre');
            payload.className = 'mt-1 max-h-40 overflow-auto rounded-field bg-base-200 p-2 text-[10px] leading-4';
            payload.textContent = JSON.stringify(row.payload, null, 2);
            details.append(summary, payload);
            finalDatesCell.appendChild(details);

            const statusCell = document.createElement('td');
            renderStatus(statusCell, row);

            const actionCell = document.createElement('td');
            if (!connected) {
                actionCell.appendChild(wpRequired());
            } else {
                const actions = document.createElement('div');
                actions.className = 'flex flex-wrap gap-1.5';
                const fetchDates = actionButton('fetch', 'Preia datele', 'bi-download');
                fetchDates.disabled = !(row.slug || row.permalink);
                const update = actionButton('update', 'Actualizează', 'bi-pencil', 'primary');
                update.disabled = !row.can_update || row.status === 'success' || row.status === 'no changes';
                actions.append(fetchDates, update);
                actionCell.appendChild(actions);
            }

            tr.append(
                courseCell,
                excelDatesCell,
                currentDatesCell,
                finalDatesCell,
                statusCell,
                actionCell,
            );
            tableBody.appendChild(tr);
        });
        previewCount.textContent = `${previewRows.length} ${previewRows.length === 1 ? 'rând' : 'rânduri'}`;
        setHidden(previewContainer, false);
        requestAnimationFrame(updateTopScrollWidth);
    }

    function updateTopScrollWidth() {
        topScrollInner.style.width = `${table.scrollWidth}px`;
    }

    let syncingScroll = false;
    topScroll.addEventListener('scroll', () => {
        if (syncingScroll) return;
        syncingScroll = true;
        tableScroll.scrollLeft = topScroll.scrollLeft;
        syncingScroll = false;
    });
    tableScroll.addEventListener('scroll', () => {
        if (syncingScroll) return;
        syncingScroll = true;
        topScroll.scrollLeft = tableScroll.scrollLeft;
        syncingScroll = false;
    });
    window.addEventListener('resize', updateTopScrollWidth);

    fileSelect.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', () => {
        const selected = fileInput.files[0];
        fileName.textContent = selected?.name || 'Niciun fișier selectat';
        fileName.classList.toggle('text-muted', !selected);
        setFileError('');
        clearMessages();
    });

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        if (busy) return;
        if (!fileInput.files.length) {
            setFileError('Selectează un fișier CSV sau XLSX.');
            return;
        }
        busy = true;
        previewButton.disabled = true;
        clearMessages();
        setFileError('');
        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: new FormData(form),
            });
            const data = await response.json().catch(() => ({}));
            if (!response.ok || !data.success) {
                throw new Error(data.error || 'Previzualizarea nu a putut fi construită.');
            }
            previewRows = data.rows || [];
            renderRows();
            showSuccess('Previzualizarea a fost construită. Verifică fiecare rând înainte de actualizare.');
        } catch (error) {
            showError(error.message);
        } finally {
            busy = false;
            previewButton.disabled = false;
        }
    });

    connectButton.addEventListener('click', async () => {
        connectButton.disabled = true;
        clearMessages();
        connectionStatus.textContent = 'Se conectează…';
        connectionStatus.className = 'badge badge-ghost badge-sm whitespace-nowrap';
        try {
            const data = await jsonRequest(form.dataset.connectUrl, credentials());
            const name = data.user?.name ? `Conectat ca ${data.user.name}` : 'Conectat';
            setConnectionState(true, name);
            showSuccess('Conexiunea WordPress a fost verificată.');
        } catch (error) {
            setConnectionError(error.message);
            showError(error.message);
        }
    });

    disconnectButton.addEventListener('click', () => {
        passwordInput.value = '';
        clearMessages();
        setConnectionState(false, 'Deconectat');
    });

    [baseUrlInput, usernameInput, passwordInput].forEach((input) => {
        input.addEventListener('input', () => {
            if (connected) {
                setConnectionState(false, 'Date modificate. Reconectează.');
            }
        });
    });

    tableBody.addEventListener('click', async (event) => {
        const button = event.target.closest('button[data-action]');
        if (!button || button.disabled) return;
        const tr = button.closest('tr[data-index]');
        const row = previewRows[Number(tr.dataset.index)];
        if (!row) return;

        button.disabled = true;
        clearMessages();
        const common = {
            ...credentials(),
            post_id: row.post_id,
            permalink: row.permalink,
            slug: row.slug,
        };
        try {
            if (button.dataset.action === 'fetch') {
                row.status = 'se preiau datele…';
                renderRows();
                const data = await jsonRequest(form.dataset.fetchDatesUrl, {
                    ...common,
                    excel_dates: row.excel_dates || [],
                });
                row.post_id = data.post_id;
                row.existing_valid_dates = data.existing_valid_dates || [];
                row.final_dates = data.final_dates || [];
                row.payload = data.payload || row.payload;
                row.can_update = Boolean(data.can_update);
                row.current_dates_loaded = true;
                row.status = 'date preluate';
            } else if (button.dataset.action === 'update') {
                row.status = 'se actualizează…';
                renderRows();
                const data = await jsonRequest(form.dataset.updateUrl, {
                    ...common,
                    final_dates: row.final_dates || [],
                });
                row.post_id = data.post_id;
                row.final_dates = data.final_dates || row.final_dates;
                row.status = data.status || 'success';
                showSuccess(data.updated ? `Cursul "${row.title}" a fost actualizat.` : `Cursul "${row.title}" nu necesită modificări.`);
            }
            row.error = null;
        } catch (error) {
            row.status = `error: ${error.message}`;
            row.error = null;
            showError(error.message);
        } finally {
            renderRows();
        }
    });

    setConnectionState(false);
})();
```

## `apps/planificator/static/planificator/generator.js`

Size: 8.9 KB

```javascript
(() => {
    const slider = document.getElementById("id_randomness");
    const yearInput = document.getElementById("id_year");
    const monthInputs = Array.from(document.querySelectorAll('input[name="months"]'));
    const fileInput = document.getElementById("id_input_file");
    const uploadDropzone = document.getElementById("ops-upload-dropzone");
    const holidayStore = document.getElementById("id_holidays");
    const holidayInput = document.getElementById("ops-holiday-date");
    const holidayList = document.getElementById("ops-holiday-list");
    const holidayLive = document.getElementById("ops-holiday-live");
    const workflow = document.getElementById("generator-workflow");
    const generatorForm = document.getElementById("generator-form");
    const sourceGenerationInput = document.getElementById("id_source_generation_id");
    const uploadPrompt = document.getElementById("ops-upload-prompt");
    const uploadState = document.getElementById("ops-upload-state");
    const uploadStatus = document.getElementById("ops-upload-status");
    const replaceUpload = document.getElementById("ops-replace-upload");
    const clearUpload = document.getElementById("ops-clear-upload");
    const clearProcessedUpload = document.getElementById("ops-clear-processed-upload");
    const uploadWarning = document.getElementById("ops-upload-warning");
    const uploadWarningText = document.getElementById("ops-upload-warning-text");

    const setText = (id, value) => {
        const element = document.getElementById(id);
        if (element) element.textContent = String(value);
    };
    const holidayItems = () => holidayStore ? holidayStore.value.split(/[\n,]+/).map((item) => item.trim()).filter(Boolean) : [];
    const writeHolidays = (items) => {
        if (holidayStore) holidayStore.value = items.join("\n");
        setText("ops-holiday-count", items.length);
    };
    const setWorkflowStep = (currentStep) => {
        document.querySelectorAll("[data-generator-step]").forEach((step) => {
            const stepNumber = Number(step.dataset.generatorStep);
            step.classList.toggle("step-primary", stepNumber < currentStep);
            step.classList.toggle("step-secondary", stepNumber === currentStep);
        });
        document.querySelectorAll("[data-generator-card]").forEach((card) => {
            const stepNumber = Number(card.dataset.generatorCard);
            card.classList.toggle("generator-card-complete", stepNumber < currentStep);
        });
        if (workflow) workflow.dataset.currentStep = String(currentStep);
    };
    const showUploadWarning = (message) => {
        if (uploadWarningText) uploadWarningText.textContent = message;
        uploadWarning?.classList.remove("hidden");
    };
    const hideUploadWarning = () => uploadWarning?.classList.add("hidden");
    const markSettingsDirty = () => {
        if (Number(workflow?.dataset.currentStep || 1) > 2) setWorkflowStep(2);
    };
    const selectedHoliday = () => {
        if (!holidayInput?.value) {
            holidayInput?.classList.add("input-error");
            return "";
        }
        holidayInput.classList.remove("input-error");
        const [year, month, day] = holidayInput.value.split("-");
        return `${day}.${month}.${year}`;
    };
    const renderHolidays = () => {
        if (!holidayList) return;
        holidayList.replaceChildren();
        holidayItems().forEach((item, index) => {
            const chip = document.createElement("span");
            chip.className = "join";
            const text = document.createElement("span");
            text.textContent = item;
            text.className = "btn btn-outline btn-primary btn-xs join-item pointer-events-none font-normal";
            const remove = document.createElement("button");
            remove.type = "button";
            remove.textContent = "×";
            remove.className = "btn btn-outline btn-primary btn-square btn-xs join-item";
            remove.setAttribute("aria-label", `Șterge data ${item}`);
            remove.addEventListener("click", () => {
                const next = holidayItems().filter((_, itemIndex) => itemIndex !== index);
                writeHolidays(next);
                renderHolidays();
                markSettingsDirty();
                if (holidayLive) holidayLive.textContent = `Data ${item} a fost ștearsă.`;
            });
            chip.append(text, remove);
            holidayList.append(chip);
        });
        setText("ops-holiday-count", holidayItems().length);
    };
    const syncMonths = () => {
        const selected = monthInputs.filter((input) => input.checked).length;
        setText("ops-month-count", selected);
        setText("ops-month-count-summary", selected);
        const submit = document.getElementById("ops-preview-submit");
        if (submit) submit.disabled = selected === 0;
        const toggle = document.getElementById("ops-toggle-months");
        if (toggle) toggle.textContent = selected === monthInputs.length ? "Deselectează toate" : "Selectează toate";
    };
    const syncSlider = () => {
        if (!slider) return;
        setText("ops-randomness-value", slider.value);
        setText("ops-randomness-summary", slider.value);
    };

    slider?.addEventListener("input", () => {
        syncSlider();
        markSettingsDirty();
    });
    yearInput?.addEventListener("change", () => {
        setText("ops-year-display", yearInput.value);
        markSettingsDirty();
    });
    monthInputs.forEach((input) => input.addEventListener("change", () => {
        syncMonths();
        markSettingsDirty();
    }));
    document.getElementById("ops-toggle-months")?.addEventListener("click", () => {
        const selectAll = monthInputs.some((input) => !input.checked);
        monthInputs.forEach((input) => { input.checked = selectAll; });
        syncMonths();
        markSettingsDirty();
    });
    document.getElementById("ops-add-holiday")?.addEventListener("click", () => {
        const formatted = selectedHoliday();
        if (!formatted) {
            holidayInput?.focus();
            if (holidayLive) holidayLive.textContent = "Data selectată nu este validă.";
            return;
        }
        const items = holidayItems();
        if (!items.includes(formatted)) items.push(formatted);
        writeHolidays(items);
        renderHolidays();
        markSettingsDirty();
        if (holidayLive) holidayLive.textContent = `Data ${formatted} a fost adăugată.`;
    });
    fileInput?.addEventListener("change", () => {
        const file = fileInput.files?.[0];
        if (!file) return;
        if (sourceGenerationInput) sourceGenerationInput.value = "";
        hideUploadWarning();
        uploadDropzone?.classList.remove("border-secondary", "border-dashed", "bg-base-200");
        uploadPrompt?.classList.add("hidden");
        uploadState?.classList.remove("hidden");
        replaceUpload?.classList.add("hidden");
        clearProcessedUpload?.classList.add("hidden");
        clearUpload?.classList.remove("hidden");
        setText("ops-upload-file-name", file.name);
        if (uploadStatus) uploadStatus.textContent = "Pregătit pentru validare";
        setWorkflowStep(2);
    });
    generatorForm?.addEventListener("submit", (event) => {
        const hasNewUpload = Boolean(fileInput?.files?.length);
        const hasProcessedUpload = Boolean(sourceGenerationInput?.value.trim());
        if (hasNewUpload || hasProcessedUpload) {
            hideUploadWarning();
            return;
        }
        event.preventDefault();
        showUploadWarning("Selectează un fișier CSV sau XLSX pentru a continua.");
        setWorkflowStep(1);
        uploadWarning?.scrollIntoView({ behavior: "smooth", block: "center" });
        fileInput?.focus({ preventScroll: true });
    });
    ["dragenter", "dragover"].forEach((eventName) => {
        uploadDropzone?.addEventListener(eventName, (event) => {
            event.preventDefault();
            uploadDropzone.classList.add("border-secondary", "bg-base-200");
        });
    });
    ["dragleave", "drop"].forEach((eventName) => {
        uploadDropzone?.addEventListener(eventName, (event) => {
            event.preventDefault();
            uploadDropzone.classList.remove("border-secondary", "bg-base-200");
        });
    });
    uploadDropzone?.addEventListener("drop", (event) => {
        const files = event.dataTransfer?.files;
        if (!fileInput || !files?.length) return;
        fileInput.files = files;
        fileInput.dispatchEvent(new Event("change", { bubbles: true }));
    });
    clearUpload?.addEventListener("click", () => {
        if (fileInput) fileInput.value = "";
        uploadState?.classList.add("hidden");
        uploadPrompt?.classList.remove("hidden");
        uploadDropzone?.classList.add("border-dashed");
        hideUploadWarning();
        setWorkflowStep(1);
    });

    setWorkflowStep(Number(workflow?.dataset.currentStep || 1));
    syncSlider();
    syncMonths();
    renderHolidays();
})();
```

## `apps/planificator/static/planificator/word_converter.js`

Size: 13.4 KB

```javascript
(() => {
    const form = document.getElementById('word-converter-form');
    if (!form) {
        return;
    }

    const elements = {
        wordFile: document.getElementById('id_word_file'),
        scheduleFile: document.getElementById('id_schedule_file'),
        wordFileSelect: document.getElementById('word-file-select'),
        scheduleFileSelect: document.getElementById('schedule-file-select'),
        wordFileName: document.getElementById('word-file-name'),
        scheduleFileName: document.getElementById('schedule-file-name'),
        wordFileError: document.getElementById('word-file-error'),
        scheduleFileError: document.getElementById('schedule-file-error'),
        error: document.getElementById('word-converter-error'),
        success: document.getElementById('word-converter-success'),
        preview: document.getElementById('word-match-preview'),
        summary: document.getElementById('word-match-summary'),
        tableBody: document.getElementById('word-match-table-body'),
        previewButton: document.getElementById('word-preview-button'),
        generateButton: document.getElementById('word-generate-button'),
        loading: document.getElementById('word-converter-loading'),
        loadingText: document.getElementById('word-converter-loading-text'),
    };
    const state = { wordFileB64: '', scheduleOptions: [], rows: [] };
    let busy = false;

    function csrfToken() {
        return form.querySelector('[name="csrfmiddlewaretoken"]')?.value || '';
    }

    function setHidden(element, hidden) {
        element.classList.toggle('hidden', hidden);
        if (element === elements.loading) {
            element.classList.toggle('flex', !hidden);
        }
    }

    function showMessage(element, message) {
        element.textContent = message;
        setHidden(element, false);
    }

    function clearMessages() {
        elements.error.textContent = '';
        elements.success.textContent = '';
        setHidden(elements.error, true);
        setHidden(elements.success, true);
    }

    function setBusy(value, message) {
        busy = value;
        elements.previewButton.disabled = value;
        elements.generateButton.disabled = value;
        if (message) {
            elements.loadingText.textContent = message;
        }
        setHidden(elements.loading, !value);
    }

    function setFieldError(control, errorElement, message) {
        errorElement.textContent = message;
        setHidden(errorElement, !message);
        control.classList.toggle('file-input-error', Boolean(message));
        control.setAttribute('aria-invalid', message ? 'true' : 'false');
    }

    function resetPreview() {
        state.wordFileB64 = '';
        state.scheduleOptions = [];
        state.rows = [];
        elements.tableBody.replaceChildren();
        setHidden(elements.preview, true);
        clearMessages();
    }

    function updateFileName(control, target) {
        target.textContent = control.files[0]?.name || 'Niciun fișier selectat';
        target.classList.toggle('text-muted', !control.files.length);
    }

    function compactOptionLabel(title, maximumLength = 42) {
        return title.length > maximumLength
            ? `${title.slice(0, maximumLength - 1).trimEnd()}…`
            : title;
    }

    function selectedOption(row) {
        return state.scheduleOptions.find((option) => option.row_index === row.selected_row_index);
    }

    function appendDates(container, dates, emptyText) {
        container.replaceChildren();
        const values = (dates || []).filter(Boolean);
        if (!values.length) {
            const empty = document.createElement('span');
            empty.className = 'text-muted';
            empty.textContent = emptyText;
            container.appendChild(empty);
            return;
        }
        values.forEach((value) => {
            const line = document.createElement('div');
            line.className = 'whitespace-nowrap';
            line.textContent = value;
            container.appendChild(line);
        });
    }

    function updateSummary() {
        const selected = state.rows.filter((row) => row.selected_row_index !== null).length;
        elements.summary.textContent = `${selected} rânduri vor fi completate. ${state.rows.length - selected} rânduri vor rămâne neschimbate.`;
    }

    function updateRow(row, tableRow, statusCell, datesCell, select) {
        const option = selectedOption(row);
        const selected = Boolean(option);
        statusCell.textContent = selected ? 'Selectat' : 'Neschimbat';
        statusCell.className = selected ? 'font-semibold text-success' : 'text-muted';
        select.title = option ? option.title : 'Lasă rândul neschimbat';
        tableRow.classList.toggle('bg-warning/10', !selected);
        appendDates(datesCell, option?.dates, selected ? 'Fără perioade' : 'Neschimbat');
        updateSummary();
    }

    function renderPreview(payload) {
        state.wordFileB64 = payload.word_file_b64;
        state.scheduleOptions = payload.schedule_options || [];
        state.rows = payload.rows || [];
        elements.tableBody.replaceChildren();

        state.rows.forEach((row) => {
            const tableRow = document.createElement('tr');
            const titleCell = document.createElement('th');
            titleCell.scope = 'row';
            titleCell.className = 'ops-word-match-course break-words whitespace-normal font-medium';
            titleCell.textContent = row.word_title;

            const statusCell = document.createElement('td');
            statusCell.className = 'align-top';
            const selectCell = document.createElement('td');
            selectCell.className = 'min-w-0 align-middle';
            const selectClip = document.createElement('div');
            selectClip.className = 'ops-word-select-clip w-full min-w-0 max-w-full';
            const select = document.createElement('select');
            select.className = 'select select-sm w-full min-w-0 max-w-full bg-base-100';
            select.setAttribute('aria-label', `Selectează programul pentru ${row.word_title}`);
            const unchanged = document.createElement('option');
            unchanged.value = '';
            unchanged.textContent = 'Lasă rândul neschimbat';
            select.appendChild(unchanged);
            state.scheduleOptions.forEach((option) => {
                const optionElement = document.createElement('option');
                optionElement.value = String(option.row_index);
                optionElement.textContent = compactOptionLabel(option.title);
                optionElement.title = option.title;
                optionElement.selected = option.row_index === row.selected_row_index;
                select.appendChild(optionElement);
            });
            selectClip.appendChild(select);
            selectCell.appendChild(selectClip);

            const candidateCell = document.createElement('td');
            const candidateList = document.createElement('div');
            candidateList.className = 'grid min-w-0 gap-1.5';
            (row.candidates || []).forEach((candidate) => {
                const button = document.createElement('button');
                button.type = 'button';
                button.className = 'btn btn-outline btn-primary btn-xs h-auto min-h-7 w-full min-w-0 max-w-full justify-between gap-2 overflow-hidden whitespace-normal py-1 text-left';
                button.dataset.rowIndex = String(candidate.row_index);
                const candidateTitle = document.createElement('span');
                candidateTitle.className = 'min-w-0 flex-1 break-words text-left';
                candidateTitle.textContent = candidate.title;
                button.appendChild(candidateTitle);
                const score = document.createElement('span');
                score.className = 'badge badge-sm badge-neutral shrink-0';
                score.textContent = String(candidate.score);
                button.appendChild(score);
                button.addEventListener('click', () => {
                    select.value = button.dataset.rowIndex;
                    select.dispatchEvent(new Event('change'));
                });
                candidateList.appendChild(button);
            });
            if (!candidateList.childElementCount) {
                candidateList.textContent = 'Nu există sugestii';
                candidateList.classList.add('text-muted');
            }
            candidateCell.appendChild(candidateList);

            const datesCell = document.createElement('td');
            datesCell.className = 'ops-word-match-periods break-words';
            tableRow.append(titleCell, statusCell, selectCell, candidateCell, datesCell);
            select.addEventListener('change', () => {
                row.selected_row_index = select.value === '' ? null : Number(select.value);
                updateRow(row, tableRow, statusCell, datesCell, select);
            });
            elements.tableBody.appendChild(tableRow);
            updateRow(row, tableRow, statusCell, datesCell, select);
        });

        setHidden(elements.preview, false);
        elements.preview.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    async function jsonResponse(response) {
        const contentType = response.headers.get('Content-Type') || '';
        if (!contentType.includes('application/json')) {
            throw new Error('Serverul a returnat un răspuns neașteptat.');
        }
        return response.json();
    }

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        if (busy) {
            return;
        }
        clearMessages();
        setFieldError(elements.wordFile, elements.wordFileError, '');
        setFieldError(elements.scheduleFile, elements.scheduleFileError, '');
        if (!elements.wordFile.files.length) {
            setFieldError(elements.wordFile, elements.wordFileError, 'Selectați un document DOCX.');
            showMessage(elements.error, 'Documentul Word este obligatoriu.');
            return;
        }
        if (!elements.scheduleFile.files.length) {
            setFieldError(elements.scheduleFile, elements.scheduleFileError, 'Selectați un program CSV sau XLSX.');
            showMessage(elements.error, 'Programul generat este obligatoriu.');
            return;
        }

        setBusy(true, 'Se analizează documentele…');
        try {
            const response = await fetch(form.dataset.previewUrl, {
                method: 'POST',
                headers: { 'X-CSRFToken': csrfToken() },
                body: new FormData(form),
            });
            const payload = await jsonResponse(response);
            if (!response.ok || !payload.success) {
                throw new Error(payload.error || 'Previzualizarea nu a putut fi creată.');
            }
            renderPreview(payload);
        } catch (error) {
            showMessage(elements.error, error.message || 'Previzualizarea nu a putut fi creată.');
        } finally {
            setBusy(false);
        }
    });

    elements.generateButton.addEventListener('click', async () => {
        if (busy || !state.wordFileB64) {
            return;
        }
        clearMessages();
        setBusy(true, 'Se generează documentul Word…');
        try {
            const matches = state.rows
                .filter((row) => row.selected_row_index !== null)
                .map((row) => ({
                    word_row_index: row.word_row_index,
                    schedule_row_index: row.selected_row_index,
                }));
            const response = await fetch(form.dataset.generateUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken(),
                },
                body: JSON.stringify({
                    word_file_b64: state.wordFileB64,
                    schedule_options: state.scheduleOptions,
                    matches,
                }),
            });
            if (!response.ok) {
                const payload = await jsonResponse(response);
                throw new Error(payload.error || 'Documentul Word nu a putut fi generat.');
            }
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = form.dataset.downloadFilename;
            document.body.appendChild(link);
            link.click();
            link.remove();
            URL.revokeObjectURL(url);
            const matched = response.headers.get('X-Matched-Course-Rows') || '0';
            const skipped = response.headers.get('X-Skipped-Course-Rows') || '0';
            showMessage(elements.success, `Documentul a fost generat. Rânduri completate: ${matched}. Rânduri neschimbate: ${skipped}.`);
        } catch (error) {
            showMessage(elements.error, error.message || 'Documentul Word nu a putut fi generat.');
        } finally {
            setBusy(false);
        }
    });

    elements.wordFileSelect.addEventListener('click', () => elements.wordFile.click());
    elements.scheduleFileSelect.addEventListener('click', () => elements.scheduleFile.click());
    elements.wordFile.addEventListener('change', () => {
        updateFileName(elements.wordFile, elements.wordFileName);
        resetPreview();
    });
    elements.scheduleFile.addEventListener('change', () => {
        updateFileName(elements.scheduleFile, elements.scheduleFileName);
        resetPreview();
    });
})();
```

## `apps/planificator/static/planificator/xml_formatter.js`

Size: 4.3 KB

```javascript
(() => {
    const form = document.getElementById('xml-export-form');
    if (!form) {
        return;
    }

    const fileInput = document.getElementById('id_input_file');
    const fileSelect = document.getElementById('xml-file-select');
    const fileName = document.getElementById('xml-file-name');
    const fileError = document.getElementById('xml-file-error');
    const postIdInput = document.getElementById('id_start_post_id');
    const postIdError = document.getElementById('xml-post-id-error');
    const errorAlert = document.getElementById('xml-export-error');
    const successAlert = document.getElementById('xml-export-success');
    const generateButton = document.getElementById('xml-generate-button');
    const loading = document.getElementById('xml-export-loading');
    let busy = false;

    function setHidden(element, hidden) {
        element.classList.toggle('hidden', hidden);
        if (element === loading) {
            element.classList.toggle('flex', !hidden);
        }
    }

    function clearMessages() {
        errorAlert.textContent = '';
        successAlert.textContent = '';
        setHidden(errorAlert, true);
        setHidden(successAlert, true);
    }

    function setFieldError(message) {
        fileError.textContent = message;
        setHidden(fileError, !message);
        fileInput.setAttribute('aria-invalid', message ? 'true' : 'false');
    }

    function setPostIdError(message) {
        postIdError.textContent = message;
        setHidden(postIdError, !message);
        postIdInput.classList.toggle('input-error', Boolean(message));
        postIdInput.setAttribute('aria-invalid', message ? 'true' : 'false');
    }

    function responseFilename(response) {
        const disposition = response.headers.get('Content-Disposition') || '';
        const match = disposition.match(/filename="?([^";]+)"?/i);
        return match?.[1] || form.dataset.downloadFilename;
    }

    function downloadBlob(blob, filename) {
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        link.remove();
        URL.revokeObjectURL(url);
    }

    fileSelect.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', () => {
        const selected = fileInput.files[0];
        fileName.textContent = selected?.name || 'Niciun fișier selectat';
        fileName.classList.toggle('text-muted', !selected);
        setFieldError('');
        clearMessages();
    });

    postIdInput.addEventListener('input', () => setPostIdError(''));

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        if (busy) {
            return;
        }
        if (!fileInput.files.length) {
            setFieldError('Selectează un fișier CSV sau XLSX.');
            return;
        }
        const postId = Number(postIdInput.value);
        if (!Number.isInteger(postId) || postId < 1 || postId > 2147483647) {
            setPostIdError('Introdu un Post ID întreg între 1 și 2147483647.');
            return;
        }

        busy = true;
        generateButton.disabled = true;
        clearMessages();
        setFieldError('');
        setPostIdError('');
        setHidden(loading, false);

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: new FormData(form),
            });
            if (!response.ok) {
                const payload = await response.json().catch(() => ({}));
                throw new Error(payload.error || 'Fișierul XML nu a putut fi generat.');
            }
            downloadBlob(await response.blob(), responseFilename(response));
            successAlert.textContent = 'Fișierul XML a fost generat.';
            setHidden(successAlert, false);
            form.reset();
            fileName.textContent = 'Niciun fișier selectat';
            fileName.classList.add('text-muted');
        } catch (error) {
            errorAlert.textContent = error.message;
            setHidden(errorAlert, false);
        } finally {
            busy = false;
            generateButton.disabled = false;
            setHidden(loading, true);
        }
    });
})();
```

## `apps/planificator/templates/planificator/actualizeaza_cursuri.html`

Size: 9.0 KB

```html
{% extends "layouts/base.html" %}
{% load static %}

{% block title %}Actualizează cursuri | Platforma TUVTK{% endblock %}

{% block content %}
    <section class="mx-auto w-full min-w-0 max-w-[1500px] space-y-5">
        <div class="space-y-2">
            <div class="breadcrumbs p-0 text-sm text-muted">
                <ul>
                    <li>Planificator</li>
                    <li>Actualizează cursuri</li>
                </ul>
            </div>
            <div>
                <h1 class="ops-title text-2xl font-bold sm:text-[2rem]">Actualizează cursuri</h1>
                <p class="mt-1 max-w-4xl text-sm leading-6 text-muted">
                    Încarcă programul, verifică datele existente din WordPress și aplică actualizările individual, numai după previzualizare.
                </p>
            </div>
        </div>

        <div class="alert items-start border border-secondary/40 bg-secondary/5 py-3 text-sm text-base-content shadow-none" role="note">
            <i class="bi bi-shield-exclamation mt-0.5 text-base text-secondary" aria-hidden="true"></i>
            <div>
                <p class="font-semibold">Accesul WordPress depinde de rețeaua serverului.</p>
                <p class="mt-0.5 leading-5 opacity-90">
                    Conectarea trebuie rulată din mediul cu acces VPN autorizat. Cloudflare poate afișa o provocare și respinge cererile provenite de la alte adrese IP.
                </p>
            </div>
        </div>

        <div id="course-updater-error" class="alert hidden border border-error/40 bg-error/5 py-2 text-sm text-error shadow-none" role="alert" aria-live="assertive"></div>
        <div id="course-updater-success" class="alert hidden border border-success/40 bg-success/5 py-2 text-sm text-success shadow-none" role="status" aria-live="polite"></div>

        <form
            id="course-updater-form"
            method="post"
            action="{% url 'planificator:actualizeaza_cursuri_preview' %}"
            enctype="multipart/form-data"
            class="grid min-w-0 gap-4 lg:grid-cols-[minmax(0,0.9fr)_minmax(0,1.35fr)]"
            data-connect-url="{% url 'planificator:actualizeaza_cursuri_connect' %}"
            data-fetch-dates-url="{% url 'planificator:actualizeaza_cursuri_fetch_dates' %}"
            data-update-url="{% url 'planificator:actualizeaza_cursuri_update_row' %}"
            novalidate
        >
            {% csrf_token %}
            <section class="card card-border min-w-0 border-base-300 bg-base-100 shadow-none">
                <div class="card-body gap-4 p-4 sm:p-5">
                    <div class="border-b border-base-300 pb-3">
                        <h2 class="text-lg font-semibold text-base-content">Program sursă</h2>
                        <p class="mt-1 text-sm leading-5 text-muted">Previzualizarea locală nu necesită conexiune la WordPress.</p>
                    </div>

                    <fieldset class="fieldset min-w-0 rounded-field border border-base-300 bg-base-200 p-3">
                        <label class="fieldset-legend" for="{{ form.input_file.id_for_label }}">{{ form.input_file.label }}</label>
                        {{ form.input_file }}
                        <div class="flex min-w-0 flex-col gap-2 sm:flex-row sm:items-center">
                            <button id="course-file-select" type="button" class="btn btn-outline btn-primary btn-sm shrink-0">Alege CSV/XLSX</button>
                            <span id="course-file-name" class="min-w-0 truncate text-sm text-muted">Niciun fișier selectat</span>
                        </div>
                        <p class="label block whitespace-normal text-xs leading-5 text-muted">Coloane obligatorii: Title și Permalink. Dimensiune maximă: 20 MB.</p>
                        <p id="course-file-error" class="label hidden text-error" role="alert"></p>
                    </fieldset>

                    <div class="mt-auto border-t border-base-300 pt-4">
                        <button id="course-preview-button" type="submit" class="btn btn-primary btn-sm w-full sm:w-auto">
                            <i class="bi bi-table" aria-hidden="true"></i>
                            Construiește previzualizarea
                        </button>
                    </div>
                </div>
            </section>

            <section class="card card-border min-w-0 border-base-300 bg-base-100 shadow-none">
                <div class="card-body gap-4 p-4 sm:p-5">
                    <div class="flex flex-col justify-between gap-2 border-b border-base-300 pb-3 sm:flex-row sm:items-start">
                        <div>
                            <h2 class="text-lg font-semibold text-base-content">Conexiune WordPress</h2>
                            <p class="mt-1 text-sm leading-5 text-muted">Parola de aplicație este folosită numai pentru cererea curentă și nu este salvată.</p>
                        </div>
                        <span id="wp-connection-status" class="badge badge-outline badge-sm whitespace-nowrap" role="status" aria-live="polite">Neconectat</span>
                    </div>

                    <div class="grid gap-3 md:grid-cols-2">
                        <fieldset class="fieldset md:col-span-2">
                            <label class="fieldset-legend" for="wp-base-url">URL WordPress</label>
                            <input id="wp-base-url" type="url" class="input input-primary input-sm w-full" value="{{ updater_settings.wp_base_url }}" placeholder="https://tuvkarpat.ro" autocomplete="url">
                        </fieldset>
                        <fieldset class="fieldset">
                            <label class="fieldset-legend" for="wp-username">Utilizator</label>
                            <input id="wp-username" type="text" class="input input-primary input-sm w-full" value="{{ updater_settings.wp_username }}" autocomplete="username">
                        </fieldset>
                        <fieldset class="fieldset">
                            <label class="fieldset-legend" for="wp-app-password">Parolă de aplicație</label>
                            <input id="wp-app-password" type="password" class="input input-primary input-sm w-full" autocomplete="off">
                        </fieldset>
                    </div>

                    <div class="mt-auto flex flex-wrap gap-2 border-t border-base-300 pt-4">
                        <button id="wp-connect-button" type="button" class="btn btn-primary btn-sm">
                            <i class="bi bi-plug" aria-hidden="true"></i>
                            Conectează
                        </button>
                        <button id="wp-disconnect-button" type="button" class="btn btn-outline btn-sm hidden">
                            Deconectează
                        </button>
                    </div>
                </div>
            </section>
        </form>

        <section id="course-preview-container" class="card card-border hidden min-w-0 border-base-300 bg-base-100 shadow-none">
            <div class="flex flex-col justify-between gap-2 border-b border-base-300 px-4 py-3 sm:flex-row sm:items-center sm:px-5">
                <div>
                    <h2 class="text-lg font-semibold text-base-content">Rezultate</h2>
                    <p id="course-preview-count" class="mt-0.5 text-xs text-muted"></p>
                </div>
                <p class="text-xs leading-5 text-muted">Fiecare actualizare este aplicată separat.</p>
            </div>
            <div class="min-w-0 p-4 pt-3 sm:p-5 sm:pt-3">
                <div id="course-preview-top-scroll" class="ops-course-updater-top-scroll" aria-hidden="true">
                    <div id="course-preview-top-scroll-inner"></div>
                </div>
                <div id="course-preview-table-scroll" class="ops-course-updater-scroll ops-scrollbar">
                    <table id="course-preview-table" class="table table-zebra table-sm ops-course-updater-table">
                        <colgroup>
                            <col class="w-[17.5rem]">
                            <col class="w-[12.5rem]">
                            <col class="w-[11.5rem]">
                            <col class="w-[14rem]">
                            <col class="w-[8rem]">
                            <col class="w-[9rem]">
                        </colgroup>
                        <thead>
                            <tr>
                                <th>Curs</th>
                                <th>Date din fișier</th>
                                <th>Date existente</th>
                                <th>Program final</th>
                                <th>Stare</th>
                                <th>Acțiuni</th>
                            </tr>
                        </thead>
                        <tbody id="course-preview-table-body"></tbody>
                    </table>
                </div>
            </div>
        </section>
    </section>
{% endblock %}

{% block page_scripts %}
    <script src="{% static 'planificator/course_updater.js' %}" defer></script>
{% endblock %}
```

## `apps/planificator/templates/planificator/generator_perioade.html`

Size: 2.6 KB

```html
{% extends "layouts/base.html" %}
{% load static %}

{% block title %}{% if history_read_only %}Program generat{% else %}Generator perioade{% endif %} | Platforma TUVTK{% endblock %}

{% block content %}
    <section id="generator-workflow" data-current-step="{% if generation %}3{% else %}1{% endif %}" class="mx-auto w-full max-w-[1360px] space-y-12" style="max-width:1360px">
        <div class="space-y-2">
            <div class="breadcrumbs p-0 text-sm text-muted">
                <ul>
                    <li>Planificator</li>
                    {% if history_read_only %}<li><a href="{% url 'planificator:istoric' %}">Istoric</a></li><li>Program generat</li>{% else %}<li>Generator perioade</li>{% endif %}
                </ul>
            </div>
            <div>
                <h1 class="text-xl font-bold text-primary sm:text-[1.75rem]">{% if history_read_only %}Program generat{% else %}Planifică seriile de curs{% endif %}</h1>
                <p class="mt-1 max-w-3xl text-sm text-muted">{% if history_read_only %}Vizualizare în mod citire a unei generări din istoric.{% else %}Încarcă oferta de cursuri, configurează programarea și verifică rezultatul.{% endif %}</p>
            </div>
        </div>

        {% if history_read_only %}
            <div class="alert alert-info py-2 text-sm" role="status">
                <span>Acest program este deschis din istoric. Fișierul sursă și setările nu pot fi modificate.</span>
            </div>
        {% endif %}

        {% include "planificator/includes/messages.html" %}

        <form id="generator-form" method="post" action="{% url 'planificator:generator_perioade' %}" enctype="multipart/form-data" class="space-y-5">
            {% csrf_token %}
            <fieldset class="contents"{% if history_read_only %} disabled aria-disabled="true"{% endif %}>
                <div class="space-y-12">
                    {{ form.source_generation_id }}
                    {% include "planificator/includes/upload.html" %}

                    {% include "planificator/includes/settings.html" %}
                </div>
            </fieldset>
        </form>

        {% if generation %}
            <form id="export-form" method="post" action="{% url 'planificator:generator_perioade_export' %}">
                {% csrf_token %}
                {{ export_form.generation_id }}
            </form>
        {% endif %}

        {% include "planificator/includes/result_table.html" %}
    </section>
{% endblock %}

{% block page_scripts %}
    <script src="{% static 'planificator/generator.js' %}" defer></script>
{% endblock %}
```

## `apps/planificator/templates/planificator/includes/actions.html`

Size: 998 B

```html
<div class="card-actions items-center justify-between gap-3 border-t border-base-300 bg-base-200 p-4">
    <p class="text-xs font-semibold text-base-content">
        <span id="ops-month-count-summary">{{ selected_month_count }}</span> luni ·
        <span id="ops-holiday-count">{{ holiday_count }}</span> zile nelucrătoare · variație
        <span id="ops-randomness-summary">{{ form.randomness.value }}</span>/10
    </p>
    <button type="submit" id="ops-preview-submit" class="btn btn-outline btn-primary btn-sm">Generează programul</button>
</div>

{% if generation_error %}
    <div class="p-4 pt-0">
        <div class="alert alert-error" role="alert">
            <div>
                <p class="font-semibold">{{ generation_error }}</p>
                {% for month, courses in unscheduled_courses.items %}
                    <p class="mt-1 text-sm">Luna {{ month }}: {{ courses|join:", " }}</p>
                {% endfor %}
            </div>
        </div>
    </div>
{% endif %}
```

## `apps/planificator/templates/planificator/includes/messages.html`

Size: 773 B

```html
{% if page_messages %}
    <div class="space-y-2" aria-live="polite">
        {% for message in page_messages %}
            <div class="alert border-primary/20 bg-base-200 py-2 text-base-content {% if message.level == 'error' %}border-error/30{% endif %}" role="{% if message.level == 'error' %}alert{% else %}status{% endif %}">
                <span class="badge badge-outline" aria-hidden="true">{% if message.level == 'error' %}!{% else %}✓{% endif %}</span>
                <div><h2 class="font-semibold">{{ message.title }}</h2><p class="text-sm">{{ message.body }}</p></div>
            </div>
        {% endfor %}
    </div>
{% endif %}
{% if form.non_field_errors %}
    <div class="alert alert-error" role="alert">{{ form.non_field_errors }}</div>
{% endif %}
```

## `apps/planificator/templates/planificator/includes/result_table.html`

Size: 4.7 KB

```html
<section id="generator-result" class="card generator-step-card overflow-hidden bg-base-100 shadow-none" data-generator-card="3">
    <div class="card-body gap-0 p-0">
        <header class="generator-card-header flex flex-col gap-3 bg-base-200 px-4 py-3 sm:flex-row sm:items-center sm:px-5">
            <div class="generator-card-step min-w-0 flex-1">
                <ul class="steps steps-vertical w-full text-xs font-semibold text-primary">
                    <li class="step {% if generation %}step-secondary{% endif %}" data-generator-step="3" data-content="3">
                        <div class="generator-card-step-copy">
                            <h2 class="card-title text-base text-primary">Program generat</h2>
                            <p class="mt-0.5 text-xs font-normal text-muted">Fiecare curs primește o perioadă pentru fiecare lună selectată.</p>
                        </div>
                    </li>
                </ul>
            </div>
            {% if generation %}
                <button type="submit" form="export-form" class="btn btn-outline btn-primary btn-sm self-start sm:self-auto">
                    Descarcă XLSX
                </button>
            {% endif %}
        </header>
        {% if preview_rows %}
            <div id="ops-preview-table-wrap" class="max-h-[32rem] overflow-auto border-t border-base-300" tabindex="0" aria-label="Tabel generat; derulează pentru a vedea toate rândurile și coloanele">
                <table class="ops-schedule-table table table-zebra table-sm [--course-width:9rem] [--duration-width:4rem] [--investment-width:5rem] sm:[--course-width:16rem] sm:[--duration-width:6rem] sm:[--investment-width:7rem] lg:[--course-width:20rem] lg:[--duration-width:7rem]">
                    <caption class="sr-only">Perioadele generate pentru cursuri</caption>
                    <thead>
                        <tr>
                            <th scope="col" class="ops-schedule-course-column z-[4] bg-base-200">Curs</th>
                            <th scope="col" class="ops-schedule-duration-column z-[4] bg-base-200">Durată</th>
                            <th scope="col" class="ops-schedule-investment-column z-[4] bg-base-200">Investiție</th>
                            {% for month_name in selected_month_headers %}
                                <th scope="col" class="z-[3] whitespace-nowrap bg-base-200 text-center">
                                    {{ month_name }}
                                </th>
                            {% endfor %}
                        </tr>
                    </thead>
                    <tbody>
                        {% for row in preview_rows %}
                            <tr>
                                <th scope="row" class="ops-schedule-course-column z-[2] whitespace-normal break-words bg-base-100 text-left">
                                    {{ row.Title }}
                                </th>
                                <td class="ops-schedule-duration-column z-[2] whitespace-nowrap bg-base-100">
                                    {{ row.duration_label }}
                                </td>
                                <td class="ops-schedule-investment-column z-[2] whitespace-nowrap bg-base-100">
                                    {{ row.investitie|default:"-" }}
                                </td>
                                {% for value in row.months %}
                                    <td class="whitespace-nowrap text-center">{{ value }}</td>
                                {% endfor %}
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        {% else %}
            <div class="hero min-h-44 border-t border-base-300 bg-base-100" role="status">
                <div class="hero-content px-4 py-8 text-center">
                    <div class="max-w-lg">
                        <svg xmlns="http://www.w3.org/2000/svg" class="mx-auto h-9 w-9 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 5.5h16M4 10h16M4 14.5h16M8 5.5v13m8-13v13M5.5 19h13a1.5 1.5 0 0 0 1.5-1.5v-12A1.5 1.5 0 0 0 18.5 4h-13A1.5 1.5 0 0 0 4 5.5v12A1.5 1.5 0 0 0 5.5 19Z" />
                        </svg>
                        <h3 class="mt-3 text-base font-semibold text-primary">Programul este pregătit pentru generare</h3>
                        <p class="mt-1 text-sm text-muted">Încarcă fișierul, verifică setările și folosește butonul „Generează programul”. Rezultatele vor fi afișate în acest tabel.</p>
                    </div>
                </div>
            </div>
        {% endif %}
    </div>
</section>
```

## `apps/planificator/templates/planificator/includes/settings.html`

Size: 4.3 KB

```html
<section id="generator-settings" class="card generator-step-card bg-base-100 shadow-none" data-generator-card="2">
    <div class="card-body gap-0 p-0">
        <header class="generator-card-header bg-base-200 px-4 py-3 sm:px-5">
            <div class="generator-card-step min-w-0">
                <ul class="steps steps-vertical w-full text-xs font-semibold text-primary">
                    <li class="step {% if generation %}step-primary{% endif %}" data-generator-step="2" data-content="2">
                        <div class="generator-card-step-copy">
                            <h2 class="card-title text-base text-primary">Setări programare</h2>
                            <p class="mt-0.5 text-xs font-normal text-muted">Configurează anul, lunile, variația și zilele nelucrătoare.</p>
                        </div>
                    </li>
                </ul>
            </div>
        </header>

        <div class="space-y-4 p-4">
            <div class="grid gap-4 md:grid-cols-3 md:items-start">
                <fieldset class="fieldset text-center">
                    <legend class="fieldset-legend mx-auto">An</legend>
                    {{ form.year }}
                    {% if form.year.errors %}<p class="label text-error" role="alert">{{ form.year.errors|join:", " }}</p>{% endif %}
                </fieldset>
                <fieldset class="fieldset relative text-center">
                    <label class="fieldset-legend mx-auto" for="{{ form.randomness.id_for_label }}">Nivel de variație</label>
                    <span id="ops-randomness-value" class="badge badge-primary badge-outline badge-sm absolute right-0 top-0">{{ form.randomness.value }}</span>
                    {{ form.randomness }}
                    <div class="flex justify-between text-[11px] text-muted">
                        <span>Predictibil</span>
                        <span>Variat</span>
                    </div>
                    {% if form.randomness.errors %}<p class="label text-error" role="alert">{{ form.randomness.errors|join:", " }}</p>{% endif %}
                </fieldset>
                <fieldset class="fieldset text-center">
                    <legend class="fieldset-legend mx-auto">Zile nelucrătoare</legend>
                    <div class="join w-full" aria-label="Selectează data nelucrătoare">
                        <label class="sr-only" for="ops-holiday-date">Dată nelucrătoare</label>
                        <input type="date" id="ops-holiday-date" lang="ro" class="input input-primary input-sm join-item min-w-0 flex-1" aria-label="Dată nelucrătoare">
                        <button type="button" id="ops-add-holiday" class="btn btn-outline btn-primary btn-sm join-item">Adaugă</button>
                    </div>
                    <div id="ops-holiday-list" class="mt-1 flex flex-wrap justify-start gap-1.5"></div>
                    <div class="hidden">{{ form.holidays }}</div>
                    <p id="ops-holiday-live" class="sr-only" aria-live="polite"></p>
                    {% if form.holidays.errors %}<p class="label text-error" role="alert">{{ form.holidays.errors|join:", " }}</p>{% endif %}
                </fieldset>
            </div>

            <fieldset class="fieldset border-t border-base-300 pt-4">
                <div class="flex items-center justify-between gap-3">
                    <legend class="fieldset-legend">Luni incluse</legend>
                    <button type="button" id="ops-toggle-months" class="btn btn-outline btn-primary btn-sm">Selectează toate</button>
                </div>
                <div class="grid gap-2 sm:grid-cols-3 xl:grid-cols-6">
                    {% for checkbox in form.months %}
                        <label class="label cursor-pointer justify-start gap-2 rounded-field border border-base-300 bg-base-200 px-2 py-1.5 hover:border-primary hover:bg-base-100">
                            {{ checkbox.tag }}
                            <span class="text-xs">{{ checkbox.choice_label }}</span>
                        </label>
                    {% endfor %}
                </div>
                {% if form.months.errors %}<p class="label text-error" role="alert">{{ form.months.errors|join:", " }}</p>{% endif %}
            </fieldset>
        </div>

        {% include "planificator/includes/actions.html" %}
    </div>
</section>
```

## `apps/planificator/templates/planificator/includes/upload.html`

Size: 4.7 KB

```html
<section id="generator-upload" class="card generator-step-card bg-base-100 shadow-none" data-generator-card="1">
    <div class="card-body gap-0 p-0">
        <header class="generator-card-header flex flex-col gap-3 bg-base-200 px-4 py-3 sm:flex-row sm:items-center sm:px-5">
            <div class="generator-card-step min-w-0 flex-1">
                <ul class="steps steps-vertical w-full text-xs font-semibold text-primary">
                    <li class="step {% if generation %}step-primary{% else %}step-secondary{% endif %}" data-generator-step="1" data-content="1">
                        <div class="generator-card-step-copy">
                            <h2 class="card-title text-base text-primary">Fișier sursă</h2>
                            <p class="mt-0.5 text-xs font-normal text-muted">Încarcă lista de cursuri în format CSV sau XLSX.</p>
                        </div>
                    </li>
                </ul>
            </div>
            {% if not history_read_only %}<a href="{% url 'planificator:generator_perioade_sample_csv' %}" class="btn btn-outline btn-secondary btn-sm self-start sm:self-auto">Descarcă modelul CSV</a>{% endif %}
        </header>

        <div class="p-4">
            <div class="sr-only">
                <label for="{{ form.input_file.id_for_label }}">Selectează fișierul</label>
                {{ form.input_file }}
            </div>

            <div id="ops-upload-dropzone" class="card card-border {% if not generation %}border-dashed{% endif %} border-base-300 bg-base-100 shadow-none">
                <label id="ops-upload-prompt" for="{{ form.input_file.id_for_label }}" class="card-body cursor-pointer items-center gap-1.5 px-4 py-6 text-center hover:bg-base-200 {% if generation %}hidden{% endif %}">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 16V4m0 0L7.5 8.5M12 4l4.5 4.5M5 15v3a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-3" />
                    </svg>
                    <span class="text-sm font-semibold text-base-content">Trage fișierul aici</span>
                    <span class="link link-primary text-sm font-semibold">sau alege de pe dispozitiv</span>
                    <span class="text-xs text-muted">CSV sau XLSX · maximum 20 MB</span>
                </label>

                <div id="ops-upload-state" class="card-body flex-col items-stretch justify-between gap-3 px-4 py-3 sm:flex-row sm:items-center {% if not generation %}hidden{% endif %}" aria-live="polite">
                    <div class="min-w-0">
                        <p id="ops-upload-file-name" class="truncate text-sm font-semibold text-primary">{{ uploaded_file_name }}</p>
                        <p id="ops-upload-status" class="text-xs text-muted">
                            {% if generation %}Fișier procesat · {{ source_course_count }} cursuri · SHA-256 {{ source_file_digest }}{% else %}Pregătit pentru validare{% endif %}
                        </p>
                    </div>
                    {% if not history_read_only %}<div class="card-actions flex-wrap sm:shrink-0">
                        <label id="ops-replace-upload" for="{{ form.input_file.id_for_label }}" class="btn btn-outline btn-primary btn-sm {% if not generation %}hidden{% endif %}">Alege alt fișier</label>
                        {% if generation %}<a id="ops-clear-processed-upload" href="{% url 'planificator:generator_perioade' %}" class="btn btn-outline btn-secondary btn-sm">Șterge fișierul</a>{% endif %}
                        <button type="button" id="ops-clear-upload" class="btn btn-outline btn-secondary btn-sm {% if generation %}hidden{% endif %}">Șterge fișierul</button>
                    </div>{% endif %}
                </div>
            </div>

            <p class="mt-2 text-xs text-muted">Coloane necesare: Title, Durata Curs, Permalink și, opțional, investitie.</p>
            <div id="ops-upload-warning" class="alert alert-warning mt-3 py-2 text-sm {% if not form.input_file.errors %}hidden{% endif %}" role="alert" aria-live="assertive">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M12 9v4m0 4h.01M10.3 4.4 2.8 17.5A1 1 0 0 0 3.7 19h16.6a1 1 0 0 0 .9-1.5L13.7 4.4a1 1 0 0 0-1.7 0Z" /></svg>
                <span id="ops-upload-warning-text">{% if form.input_file.errors %}{{ form.input_file.errors|join:", " }}{% else %}Selectează un fișier CSV sau XLSX pentru a continua.{% endif %}</span>
            </div>
        </div>
    </div>
</section>
```

## `apps/planificator/templates/planificator/istoric.html`

Size: 8.3 KB

```html
{% extends "layouts/base.html" %}

{% block title %}Istoric generări | Platforma TUVTK{% endblock %}

{% block content %}
    <section class="mx-auto w-full max-w-[1360px] space-y-5" style="max-width:1360px">
        <div class="space-y-2">
            <div class="breadcrumbs p-0 text-sm text-muted">
                <ul>
                    <li>Planificator</li>
                    <li>Istoric</li>
                </ul>
            </div>
            <div class="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
                <div>
                    <h1 class="text-xl font-bold text-primary sm:text-[1.75rem]">Istoric generări</h1>
                    <p class="mt-1 max-w-3xl text-sm text-muted">Consultă programele generate în ultimele 24 de ore și descarcă din nou fișierele XLSX.</p>
                </div>
                <a href="{% url 'planificator:generator_perioade' %}" class="btn btn-outline btn-primary btn-sm self-start sm:self-auto">Generează program nou</a>
            </div>
        </div>

        <section class="card generator-step-card bg-base-100 shadow-none" aria-labelledby="history-list-title">
            <header class="generator-card-header bg-base-200 px-4 py-4 sm:px-5">
                <h2 id="history-list-title" class="text-base font-semibold text-primary">Programe disponibile</h2>
                <p class="mt-1 text-xs text-muted">Fișierele expirate nu mai pot fi descărcate și sunt eliminate automat.</p>
            </header>

            {% if generations %}
                <div class="divide-y divide-base-300 md:hidden">
                    {% for generation in generations %}
                        <article class="space-y-3 p-4">
                            <div>
                                <a href="{% url 'planificator:istoric_detail' generation.pk %}" class="link link-primary font-semibold">{{ generation.source_file_name }}</a>
                                <span class="mt-0.5 block font-mono text-[11px] text-muted">SHA-256 {{ generation.source_file_digest|slice:":12" }}</span>
                            </div>
                            <dl class="grid grid-cols-2 gap-x-4 gap-y-2 text-sm">
                                <div><dt class="text-xs text-muted">An</dt><dd class="font-semibold">{{ generation.year }}</dd></div>
                                <div><dt class="text-xs text-muted">Luni</dt><dd class="font-semibold">{{ generation.selected_months|join:", " }}</dd></div>
                                <div><dt class="text-xs text-muted">Cursuri</dt><dd class="font-semibold">{{ generation.source_course_count }}</dd></div>
                                <div><dt class="text-xs text-muted">Perioade</dt><dd class="font-semibold">{{ generation.generated_entry_count }}</dd></div>
                                <div><dt class="text-xs text-muted">Generat</dt><dd>{{ generation.created_at|date:"d.m.Y H:i" }}</dd></div>
                                <div><dt class="text-xs text-muted">Expiră</dt><dd>{{ generation.expires_at|date:"d.m.Y H:i" }}</dd></div>
                            </dl>
                            <div class="flex flex-wrap gap-2">
                                <a href="{% url 'planificator:istoric_detail' generation.pk %}" class="btn btn-outline btn-primary btn-sm">Vezi</a>
                                <form method="post" action="{% url 'planificator:generator_perioade_export' %}">
                                    {% csrf_token %}
                                    <input type="hidden" name="generation_id" value="{{ generation.pk }}">
                                    <button type="submit" class="btn btn-outline btn-secondary btn-sm">Descarcă XLSX</button>
                                </form>
                            </div>
                        </article>
                    {% endfor %}
                </div>

                <div class="hidden overflow-x-auto md:block">
                    <table class="table table-sm">
                        <thead>
                            <tr>
                                <th scope="col">Fișier sursă</th>
                                <th scope="col">An</th>
                                <th scope="col">Luni</th>
                                <th scope="col">Cursuri</th>
                                <th scope="col">Perioade</th>
                                <th scope="col">Generat</th>
                                <th scope="col">Expiră</th>
                                <th scope="col" class="text-right">Acțiuni</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for generation in generations %}
                                <tr>
                                    <th scope="row" class="min-w-48">
                                        <a href="{% url 'planificator:istoric_detail' generation.pk %}" class="link link-primary font-semibold">{{ generation.source_file_name }}</a>
                                        <span class="mt-0.5 block font-mono text-[11px] font-normal text-muted">SHA-256 {{ generation.source_file_digest|slice:":12" }}</span>
                                    </th>
                                    <td>{{ generation.year }}</td>
                                    <td>{{ generation.selected_months|join:", " }}</td>
                                    <td>{{ generation.source_course_count }}</td>
                                    <td>{{ generation.generated_entry_count }}</td>
                                    <td class="whitespace-nowrap">{{ generation.created_at|date:"d.m.Y H:i" }}</td>
                                    <td class="whitespace-nowrap">{{ generation.expires_at|date:"d.m.Y H:i" }}</td>
                                    <td>
                                        <div class="flex justify-end gap-2">
                                            <a href="{% url 'planificator:istoric_detail' generation.pk %}" class="btn btn-outline btn-primary btn-sm">Vezi</a>
                                            <form method="post" action="{% url 'planificator:generator_perioade_export' %}">
                                                {% csrf_token %}
                                                <input type="hidden" name="generation_id" value="{{ generation.pk }}">
                                                <button type="submit" class="btn btn-outline btn-secondary btn-sm">Descarcă XLSX</button>
                                            </form>
                                        </div>
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <div class="px-4 py-12 text-center sm:px-6">
                    <svg xmlns="http://www.w3.org/2000/svg" class="mx-auto h-10 w-10 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 6.5h16M6.5 3.5v3m11-3v3M5.5 20.5h13a1.5 1.5 0 0 0 1.5-1.5V6.5H4V19a1.5 1.5 0 0 0 1.5 1.5Zm2.5-10h3v3H8v-3Z" /></svg>
                    <h3 class="mt-3 text-base font-semibold text-primary">Nu există programe disponibile</h3>
                    <p class="mx-auto mt-1 max-w-md text-sm text-muted">Generează primul program pentru a-l putea consulta și descărca de aici.</p>
                    <a href="{% url 'planificator:generator_perioade' %}" class="btn btn-outline btn-primary btn-sm mt-4">Deschide generatorul</a>
                </div>
            {% endif %}
        </section>

        {% if is_paginated %}
            <nav class="flex items-center justify-between gap-3" aria-label="Paginare istoric">
                {% if page_obj.has_previous %}<a href="?page={{ page_obj.previous_page_number }}" class="btn btn-outline btn-primary btn-sm">Pagina anterioară</a>{% else %}<span></span>{% endif %}
                <span class="text-sm text-muted">Pagina {{ page_obj.number }} din {{ page_obj.paginator.num_pages }}</span>
                {% if page_obj.has_next %}<a href="?page={{ page_obj.next_page_number }}" class="btn btn-outline btn-primary btn-sm">Pagina următoare</a>{% else %}<span></span>{% endif %}
            </nav>
        {% endif %}
    </section>
{% endblock %}
```

## `apps/planificator/templates/planificator/word_converter.html`

Size: 7.9 KB

```html
{% extends "layouts/base.html" %}
{% load static %}

{% block title %}Convertor Word | Platforma TUVTK{% endblock %}

{% block content %}
    <section class="mx-auto w-full min-w-0 max-w-[1360px] space-y-5">
        <div class="space-y-2">
            <div class="breadcrumbs p-0 text-sm text-muted">
                <ul>
                    <li>Planificator</li>
                    <li>Convertor Word</li>
                </ul>
            </div>
            <div>
                <h1 class="ops-title text-2xl font-bold sm:text-[2rem]">Convertor planificare Word</h1>
                <p class="mt-1 max-w-3xl text-sm leading-6 text-muted">
                    Potrivește cursurile din documentul Word cu programul generat, verifică sugestiile și completează primele trei perioade într-o copie nouă a documentului.
                </p>
            </div>
        </div>

        <div id="word-converter-error" class="alert alert-error hidden py-2 text-sm" role="alert" aria-live="assertive"></div>
        <div id="word-converter-success" class="alert alert-success hidden py-2 text-sm" role="status" aria-live="polite"></div>

        <form
            id="word-converter-form"
            method="post"
            enctype="multipart/form-data"
            class="card card-border border-base-300 bg-base-100 shadow-none"
            data-preview-url="{% url 'planificator:word_match_preview' %}"
            data-generate-url="{% url 'planificator:word_match_generate' %}"
            data-download-filename="planificare_cursuri_actualizata.docx"
            novalidate
        >
            {% csrf_token %}
            <div class="card-body gap-5 p-4 sm:p-5">
                <div class="flex flex-col justify-between gap-2 border-b border-base-300 pb-3 sm:flex-row sm:items-start">
                    <div>
                        <p class="text-xs font-semibold uppercase tracking-[0.16em] text-primary">Fișiere sursă</p>
                        <h2 class="mt-1 text-lg font-semibold text-base-content">Pregătește potrivirile</h2>
                        <p class="mt-1 text-sm text-muted">Documentul Word trebuie să aibă titlul cursului în prima coloană și perioadele în coloanele 4–6.</p>
                    </div>
                    <span class="badge badge-outline badge-sm self-start whitespace-nowrap">Maximum 20 MB / fișier</span>
                </div>

                <div class="grid gap-4 md:grid-cols-2">
                    <fieldset class="fieldset min-w-0 rounded-field border border-base-300 bg-base-200 p-3">
                        <label class="fieldset-legend" for="{{ form.word_file.id_for_label }}">{{ form.word_file.label }}</label>
                        {{ form.word_file }}
                        <div class="flex min-w-0 items-center gap-2">
                            <button id="word-file-select" type="button" class="btn btn-outline btn-primary btn-sm shrink-0">Alege DOCX</button>
                            <span id="word-file-name" class="min-w-0 truncate text-sm text-muted">Niciun fișier selectat</span>
                        </div>
                        <p class="label block whitespace-normal break-words text-xs leading-5 text-muted">Format acceptat: DOCX.</p>
                        <p id="word-file-error" class="label hidden text-error" role="alert"></p>
                    </fieldset>
                    <fieldset class="fieldset min-w-0 rounded-field border border-base-300 bg-base-200 p-3">
                        <label class="fieldset-legend" for="{{ form.schedule_file.id_for_label }}">{{ form.schedule_file.label }}</label>
                        {{ form.schedule_file }}
                        <div class="flex min-w-0 items-center gap-2">
                            <button id="schedule-file-select" type="button" class="btn btn-outline btn-primary btn-sm shrink-0">Alege CSV/XLSX</button>
                            <span id="schedule-file-name" class="min-w-0 truncate text-sm text-muted">Niciun fișier selectat</span>
                        </div>
                        <p class="label block whitespace-normal break-words text-xs leading-5 text-muted">Formate acceptate: CSV sau XLSX, cu Title și coloane lunare.</p>
                        <p id="schedule-file-error" class="label hidden text-error" role="alert"></p>
                    </fieldset>
                </div>

                <div class="flex flex-col-reverse justify-between gap-3 border-t border-base-300 pt-4 sm:flex-row sm:items-center">
                    <p class="text-xs leading-5 text-muted">Fișierele sunt procesate doar pentru această previzualizare și nu sunt salvate în istoric.</p>
                    <button id="word-preview-button" type="submit" class="btn btn-outline btn-primary btn-sm">
                        Previzualizează potrivirile
                    </button>
                </div>
            </div>
        </form>

        <section id="word-match-preview" class="card card-border hidden min-w-0 max-w-full overflow-hidden border-base-300 bg-base-100 shadow-none" aria-labelledby="word-match-preview-title">
            <div class="card-body min-w-0 gap-0 p-0">
                <div class="flex flex-col justify-between gap-3 p-4 sm:flex-row sm:items-center sm:p-5">
                    <div>
                        <p class="text-xs font-semibold uppercase tracking-[0.16em] text-primary">Verificare</p>
                        <h2 id="word-match-preview-title" class="mt-1 text-lg font-semibold text-base-content">Potriviri propuse</h2>
                        <p id="word-match-summary" class="mt-1 text-sm text-muted" aria-live="polite"></p>
                    </div>
                    <button id="word-generate-button" type="button" class="btn btn-primary btn-sm self-start sm:self-auto">
                        Generează documentul Word
                    </button>
                </div>

                <p class="border-t border-base-300 bg-base-200 px-4 py-2 text-xs text-muted sm:hidden">Glisează orizontal pentru a vedea toate coloanele.</p>
                <div class="ops-word-match-scroll ops-scrollbar w-full min-w-0 max-w-full overflow-x-scroll overflow-y-auto border-t border-base-300" tabindex="0" aria-label="Tabel cu potrivirile cursurilor; glisează orizontal pentru toate coloanele">
                    <table class="ops-word-match-table table table-fixed table-zebra table-sm">
                        <colgroup>
                            <col class="w-[14.75rem]">
                            <col class="w-28">
                            <col class="w-80">
                            <col class="w-[22rem]">
                            <col class="w-40">
                        </colgroup>
                        <thead>
                            <tr class="bg-base-200">
                                <th scope="col">Curs în documentul Word</th>
                                <th scope="col">Stare</th>
                                <th scope="col">Rând selectat din program</th>
                                <th scope="col">Sugestii</th>
                                <th scope="col" class="ops-word-match-periods">Perioade completate</th>
                            </tr>
                        </thead>
                        <tbody id="word-match-table-body"></tbody>
                    </table>
                </div>
            </div>
        </section>
    </section>

    <div id="word-converter-loading" class="fixed inset-0 z-[70] hidden items-center justify-center bg-base-content/20 p-4" role="status" aria-live="polite">
        <div class="flex items-center gap-3 rounded-field border border-base-300 bg-base-100 px-4 py-3 shadow-lg">
            <span class="loading loading-spinner loading-md text-primary" aria-hidden="true"></span>
            <span id="word-converter-loading-text" class="text-sm font-medium">Se procesează fișierele…</span>
        </div>
    </div>
{% endblock %}

{% block page_scripts %}
    <script src="{% static 'planificator/word_converter.js' %}" defer></script>
{% endblock %}
```

## `apps/planificator/templates/planificator/xml_formatter.html`

Size: 4.9 KB

```html
{% extends "layouts/base.html" %}
{% load static %}

{% block title %}Convertor XML | Platforma TUVTK{% endblock %}

{% block content %}
    <section class="mx-auto w-full min-w-0 max-w-340 space-y-5">
        <div class="space-y-2">
            <div class="breadcrumbs p-0 text-sm text-muted">
                <ul>
                    <li>Planificator</li>
                    <li>Convertor XML</li>
                </ul>
            </div>
            <div>
                <h1 class="ops-title text-2xl font-bold sm:text-[2rem]">Generează exportul XML</h1>
                <p class="mt-1 max-w-3xl text-sm leading-6 text-muted">
                    Încarcă programul de cursuri și generează fișierul XML compatibil cu importul evenimentelor în WordPress.
                </p>
            </div>
        </div>

        <div id="xml-export-error" class="alert alert-error hidden py-2 text-sm" role="alert" aria-live="assertive"></div>
        <div id="xml-export-success" class="alert alert-success hidden py-2 text-sm" role="status" aria-live="polite"></div>

        <form
            id="xml-export-form"
            method="post"
            action="{% url 'planificator:xml_export' %}"
            enctype="multipart/form-data"
            class="card card-border border-base-300 bg-base-100 shadow-none"
            data-download-filename="formatted_courses.xml"
            novalidate
        >
            {% csrf_token %}
            <div class="card-body gap-5 p-4 sm:p-5">
                <div class="flex flex-col justify-between gap-2 border-b border-base-300 pb-3 sm:flex-row sm:items-start">
                    <div>
                        <p class="text-xs font-semibold uppercase tracking-[0.16em] text-primary">Fișier sursă</p>
                        <h2 class="mt-1 text-lg font-semibold text-base-content">Programul generat</h2>
                        <p class="mt-1 text-sm text-muted">Fișierul trebuie să conțină coloanele Title, Permalink și cel puțin o coloană lunară.</p>
                    </div>
                    <span class="badge badge-outline badge-sm self-start whitespace-nowrap">Maximum 20 MB</span>
                </div>

                <fieldset class="fieldset min-w-0 rounded-field border border-base-300 bg-base-200 p-3">
                    <label class="fieldset-legend" for="{{ form.input_file.id_for_label }}">{{ form.input_file.label }}</label>
                    {{ form.input_file }}
                    <div class="flex min-w-0 flex-col gap-2 sm:flex-row sm:items-center">
                        <button id="xml-file-select" type="button" class="btn btn-outline btn-primary btn-sm shrink-0">Alege CSV/XLSX</button>
                        <span id="xml-file-name" class="min-w-0 truncate text-sm text-muted">Niciun fișier selectat</span>
                    </div>
                    <p class="label block whitespace-normal wrap-break-word text-xs leading-5 text-muted">
                        Sunt acceptate CSV și XLSX. Coloanele lunare pot folosi denumiri în română, engleză sau formatul Luna 1–Luna 12.
                    </p>
                    <p id="xml-file-error" class="label hidden text-error" role="alert"></p>
                </fieldset>

                <fieldset class="fieldset max-w-sm rounded-field border border-base-300 bg-base-200 p-3">
                    <label class="fieldset-legend" for="{{ form.start_post_id.id_for_label }}">{{ form.start_post_id.label }}</label>
                    {{ form.start_post_id }}
                    <p class="label block whitespace-normal text-xs leading-5 text-muted">
                        Primul eveniment va primi exact acest ID. Evenimentele următoare vor fi numerotate consecutiv.
                    </p>
                    <p id="xml-post-id-error" class="label hidden text-error" role="alert"></p>
                </fieldset>

                <div class="flex flex-col-reverse justify-between gap-3 border-t border-base-300 pt-4 sm:flex-row sm:items-center">
                    <p class="text-xs leading-5 text-muted">Fișierul este procesat doar pentru export și nu este salvat în istoric.</p>
                    <button id="xml-generate-button" type="submit" class="btn btn-primary btn-sm">
                        Generează XML
                    </button>
                </div>
            </div>
        </form>
    </section>

    <div id="xml-export-loading" class="fixed inset-0 z-70 hidden items-center justify-center bg-base-content/20 p-4" role="status" aria-live="polite">
        <div class="flex items-center gap-3 rounded-field border border-base-300 bg-base-100 px-4 py-3 shadow-lg">
            <span class="loading loading-spinner loading-md text-primary" aria-hidden="true"></span>
            <span class="text-sm font-medium">Se generează fișierul XML…</span>
        </div>
    </div>
{% endblock %}

{% block page_scripts %}
    <script src="{% static 'planificator/xml_formatter.js' %}" defer></script>
{% endblock %}
```

## `apps/planificator/tests.py`

Size: 22.7 KB

```python
import io
from datetime import datetime, timedelta, timezone as datetime_timezone
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.db import DatabaseError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from openpyxl import Workbook, load_workbook

from .file_handlers import create_excel_export, read_input_file
from .models import AppSetting, ScheduleGeneration
from .settings_store import get_settings, save_settings


def csv_upload(name="courses.csv", rows=None):
    rows = rows or [
        "Alpha Upload,3 days,https://example.com/course-a,100",
        "Beta Upload,2 days,https://example.com/course-b,200",
    ]
    content = "Title,Durata Curs,Permalink,investitie\n" + "\n".join(rows) + "\n"
    return SimpleUploadedFile(name, content.encode("utf-8"), content_type="text/csv")


def generation_for(user, *, schedule=None, expired=False):
    schedule = schedule or [{
        "source_row": 2,
        "original_order": 0,
        "Title": "Course A",
        "Permalink": "https://example.com/course-a",
        "Durata Curs": "3 days",
        "investitie": "100",
        "date_range": "05-07.01.2026",
        "month": 1,
        "month_name": "Ianuarie",
    }]
    return ScheduleGeneration.objects.create(
        owner=user,
        year=2026,
        selected_months=[1],
        holidays=[],
        random_seed=42,
        schedule=schedule,
        source_course_count=1,
        generated_entry_count=len(schedule),
        source_file_name="courses.csv",
        source_file_digest="a" * 64,
        source_file_data=(
            b"Title,Durata Curs,Permalink,investitie\n"
            b"Course A,3 days,https://example.com/course-a,100\n"
        ),
        expires_at=timezone.now() + (-timedelta(hours=1) if expired else timedelta(hours=24)),
    )


class PlanificatorViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="planner", password="test-password", first_name="Plan", last_name="Operator"
        )
        cls.permission = Permission.objects.get(codename="use_course_planning")
        cls.user.user_permissions.add(cls.permission)

    def setUp(self):
        self.client.force_login(self.user)

    def test_planificator_routes_render_for_authorized_user(self):
        for route, template in (
            ("planificator:generator_perioade", "planificator/generator_perioade.html"),
            ("planificator:actualizeaza_cursuri", "planificator/actualizeaza_cursuri.html"),
            ("planificator:istoric", "planificator/istoric.html"),
        ):
            response = self.client.get(reverse(route))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template)

    def test_planificator_has_no_landing_page(self):
        response = self.client.get("/planificator/")

        self.assertEqual(response.status_code, 404)

    def test_generator_uses_daisyui_year_selector(self):
        response = self.client.get(reverse("planificator:generator_perioade"))

        self.assertContains(response, '<select name="year" class="select select-primary select-sm w-full" id="id_year">')
        self.assertContains(response, 'class="checkbox checkbox-primary checkbox-xs"', count=12)
        self.assertContains(response, 'type="date" id="ops-holiday-date"')
        self.assertContains(response, 'style="max-width:1360px"')
        self.assertContains(response, 'class="steps steps-vertical w-full text-xs font-semibold text-primary"', count=3)
        self.assertContains(response, 'class="generator-card-step min-w-0', count=3)
        self.assertContains(response, 'space-y-4 p-4', count=1)
        self.assertContains(response, 'data-current-step="1"')
        self.assertContains(response, 'step-secondary" data-generator-step="1"', count=1)
        self.assertNotContains(response, 'class="divider')
        self.assertContains(response, "<li>Planificator</li>")
        self.assertNotContains(response, 'href="/planificator/"')
        self.assertContains(response, 'id="generator-upload" class="card generator-step-card')
        self.assertContains(response, 'id="generator-settings" class="card generator-step-card')
        self.assertContains(response, 'id="generator-result" class="card generator-step-card')
        self.assertContains(response, 'data-generator-card="', count=3)
        self.assertContains(response, 'class="grid gap-4 md:grid-cols-3 md:items-start"')
        self.assertContains(response, 'id="ops-upload-dropzone"')
        self.assertContains(response, 'id="ops-upload-warning" class="alert alert-warning')
        self.assertFalse(response.context["form"].fields["input_file"].required)
        self.assertContains(response, "Programul este pregătit pentru generare")
        self.assertNotContains(response, "btn-xs")
        self.assertNotContains(response, 'class="btn btn-primary')
        self.assertNotContains(response, "ops-work-section")

    def test_result_table_has_its_own_scroll_area_and_three_sticky_columns(self):
        generation = generation_for(self.user)
        response = self.client.get(
            reverse("planificator:generator_perioade_result", kwargs={"generation_id": generation.pk})
        )

        self.assertContains(response, 'id="ops-preview-table-wrap" class="max-h-[32rem] overflow-auto')
        self.assertContains(response, "ops-schedule-table", count=1)
        self.assertContains(response, "ops-schedule-course-column", count=2)
        self.assertContains(response, "ops-schedule-duration-column", count=2)
        self.assertContains(response, "ops-schedule-investment-column", count=2)
        self.assertNotContains(response, "position:sticky!important")
        self.assertContains(response, 'data-current-step="3"')
        self.assertContains(response, 'step-secondary" data-generator-step="3"', count=1)
        self.assertContains(response, 'id="generator-result" class="card generator-step-card overflow-hidden')
        self.assertContains(response, f'value="{generation.pk}"')
        self.assertContains(response, "Fișier procesat · 1 cursuri")
        self.assertContains(response, "Alege alt fișier")
        self.assertContains(response, 'id="ops-clear-processed-upload"')
        self.assertContains(response, "Șterge fișierul")
        self.assertNotContains(response, "Programul a fost generat")

    def test_anonymous_user_is_redirected_to_login(self):
        self.client.logout()
        response = self.client.get(reverse("planificator:generator_perioade"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('planificator:generator_perioade')}")

    def test_authenticated_user_without_permission_receives_403(self):
        other = get_user_model().objects.create_user(username="no-access", password="x")
        self.client.force_login(other)
        self.assertEqual(self.client.get(reverse("planificator:generator_perioade")).status_code, 403)

    def test_staff_without_permission_receives_403_and_superuser_is_allowed(self):
        staff = get_user_model().objects.create_user(username="staff", password="x", is_staff=True)
        self.client.force_login(staff)
        self.assertEqual(self.client.get(reverse("planificator:generator_perioade")).status_code, 403)
        superuser = get_user_model().objects.create_superuser(username="root-user", password="x")
        self.client.force_login(superuser)
        self.assertEqual(self.client.get(reverse("planificator:generator_perioade")).status_code, 200)

    def test_generator_uses_post_redirect_get_and_complete_matrix(self):
        response = self.client.post(
            reverse("planificator:generator_perioade"),
            {"input_file": csv_upload(), "year": 2026, "months": ["1", "2"], "randomness": 5, "holidays": ""},
        )
        generation = ScheduleGeneration.objects.get()
        self.assertRedirects(
            response,
            reverse("planificator:generator_perioade_result", kwargs={"generation_id": generation.pk}),
        )
        self.assertEqual(generation.source_course_count, 2)
        self.assertEqual(generation.generated_entry_count, 4)
        self.assertEqual(
            {(row["source_row"], row["month"]) for row in generation.schedule},
            {(2, 1), (2, 2), (3, 1), (3, 2)},
        )
        self.assertTrue(generation.source_file_data)

    def test_result_can_regenerate_with_saved_upload_after_year_change(self):
        initial_response = self.client.post(
            reverse("planificator:generator_perioade"),
            {"input_file": csv_upload(), "year": 2026, "months": ["1"], "randomness": 5, "holidays": ""},
        )
        initial_generation = ScheduleGeneration.objects.get()
        self.assertEqual(initial_response.status_code, 302)

        response = self.client.post(
            reverse("planificator:generator_perioade"),
            {
                "source_generation_id": initial_generation.pk,
                "year": 2027,
                "months": ["1"],
                "randomness": 5,
                "holidays": "",
            },
        )

        self.assertEqual(response.status_code, 302)
        regenerated = ScheduleGeneration.objects.exclude(pk=initial_generation.pk).get()
        self.assertEqual(regenerated.year, 2027)
        self.assertEqual(regenerated.source_file_digest, initial_generation.source_file_digest)
        self.assertEqual(bytes(regenerated.source_file_data), bytes(initial_generation.source_file_data))

    def test_saved_upload_regeneration_rejects_foreign_and_expired_sources(self):
        other = get_user_model().objects.create_user(username="regeneration-other")
        foreign = generation_for(other)
        expired = generation_for(self.user, expired=True)

        for generation in (foreign, expired):
            with self.subTest(generation=generation.pk):
                response = self.client.post(
                    reverse("planificator:generator_perioade"),
                    {
                        "source_generation_id": generation.pk,
                        "year": 2027,
                        "months": ["1"],
                        "randomness": 5,
                        "holidays": "",
                    },
                )

                self.assertEqual(response.status_code, 404)

    def test_missing_upload_uses_inline_warning_instead_of_required_file_input(self):
        response = self.client.post(
            reverse("planificator:generator_perioade"),
            {"year": 2026, "months": ["1"], "randomness": 5, "holidays": ""},
        )

        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "alert alert-warning", status_code=400)
        self.assertContains(response, "Selectează un fișier CSV sau XLSX", status_code=400)

    def test_result_export_form_contains_only_generation_identifier(self):
        generation = generation_for(self.user)
        response = self.client.get(
            reverse("planificator:generator_perioade_result", kwargs={"generation_id": generation.pk})
        )
        self.assertContains(response, 'id="export-form"')
        self.assertContains(response, 'name="generation_id"')
        self.assertNotContains(response, "schedule_payload")

    def test_history_lists_only_owned_active_generations_with_download_actions(self):
        owned = generation_for(self.user)
        owned.source_file_name = "owned.csv"
        owned.save(update_fields=["source_file_name"])
        expired = generation_for(self.user, expired=True)
        expired.source_file_name = "expired.csv"
        expired.save(update_fields=["source_file_name"])
        other = get_user_model().objects.create_user(username="history-other")
        foreign = generation_for(other)
        foreign.source_file_name = "foreign.csv"
        foreign.save(update_fields=["source_file_name"])

        response = self.client.get(reverse("planificator:istoric"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "planificator/istoric.html")
        self.assertContains(response, "owned.csv")
        self.assertNotContains(response, "expired.csv")
        self.assertNotContains(response, "foreign.csv")
        self.assertContains(response, f'name="generation_id" value="{owned.pk}"')
        self.assertContains(response, reverse("planificator:generator_perioade_export"))
        self.assertContains(response, reverse("planificator:istoric_detail", kwargs={"generation_id": owned.pk}))
        self.assertContains(response, "Descarcă XLSX")

    def test_history_displays_generation_time_in_bucharest(self):
        generation = generation_for(self.user)
        ScheduleGeneration.objects.filter(pk=generation.pk).update(
            created_at=datetime(2026, 7, 3, 8, 7, tzinfo=datetime_timezone.utc),
            expires_at=datetime(2099, 7, 4, 8, 7, tzinfo=datetime_timezone.utc),
        )

        response = self.client.get(reverse("planificator:istoric"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "03.07.2026 11:07", count=2)

    def test_history_has_empty_state(self):
        response = self.client.get(reverse("planificator:istoric"))

        self.assertContains(response, "Nu există programe disponibile")
        self.assertContains(response, "Deschide generatorul")

    def test_history_detail_is_read_only_but_keeps_export_available(self):
        generation = generation_for(self.user)

        response = self.client.get(
            reverse("planificator:istoric_detail", kwargs={"generation_id": generation.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "planificator/generator_perioade.html")
        self.assertTrue(response.context["history_read_only"])
        self.assertContains(response, 'class="contents" disabled aria-disabled="true"')
        self.assertContains(response, "Fișierul sursă și setările nu pot fi modificate")
        self.assertNotContains(response, "Alege alt fișier")
        self.assertNotContains(response, "Șterge fișierul")
        self.assertNotContains(response, "Descarcă modelul CSV")
        self.assertContains(response, 'id="export-form"')
        self.assertContains(response, "Descarcă XLSX")

    def test_history_detail_cannot_open_another_users_generation(self):
        other = get_user_model().objects.create_user(username="history-detail-other")
        generation = generation_for(other)

        response = self.client.get(
            reverse("planificator:istoric_detail", kwargs={"generation_id": generation.pk})
        )

        self.assertEqual(response.status_code, 404)

    def test_export_reads_owned_server_side_generation(self):
        generation = generation_for(self.user)
        response = self.client.post(
            reverse("planificator:generator_perioade_export"), {"generation_id": generation.pk}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Type"],
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        self.assertIn("Program", load_workbook(io.BytesIO(response.content)).sheetnames)

    def test_other_users_and_expired_generations_are_not_exportable(self):
        other = get_user_model().objects.create_user(username="other", password="x")
        other.user_permissions.add(self.permission)
        foreign = generation_for(other)
        expired = generation_for(self.user, expired=True)
        for generation in (foreign, expired):
            response = self.client.post(
                reverse("planificator:generator_perioade_export"), {"generation_id": generation.pk}
            )
            self.assertEqual(response.status_code, 404)

    def test_invalid_month_is_a_form_error_not_server_error(self):
        response = self.client.post(
            reverse("planificator:generator_perioade"),
            {"input_file": csv_upload(), "year": 2026, "months": ["bogus"], "randomness": 5, "holidays": ""},
        )
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "Select a valid choice", status_code=400)

    def test_invalid_upload_extension_is_a_form_error(self):
        upload = SimpleUploadedFile("courses.xls", b"not-an-xls", content_type="application/octet-stream")
        response = self.client.post(
            reverse("planificator:generator_perioade"),
            {"input_file": upload, "year": 2026, "months": ["1"], "randomness": 5, "holidays": ""},
        )
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, ".csv", status_code=400)

    def test_invalid_year_randomness_and_holiday_markup_are_form_errors(self):
        response = self.client.post(
            reverse("planificator:generator_perioade"),
            {
                "input_file": csv_upload(),
                "year": 1900,
                "months": ["1"],
                "randomness": 11,
                "holidays": '<img src=x onerror="alert(1)">',
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertNotContains(response, '<img src=x onerror="alert(1)">', status_code=400)

    def test_corrupt_saved_settings_are_safely_normalized(self):
        AppSetting.objects.create(
            user=self.user,
            scope="schedule_generator",
            payload={"year": "bad", "months": ["bad", 13], "randomness": 99, "holidays": ["not-a-date"]},
        )
        response = self.client.get(reverse("planificator:generator_perioade"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["selected_months"], [])

    def test_incomplete_schedule_is_not_persisted(self):
        holidays = "\n".join(
            f"{day:02d}.01.2026" for day in range(1, 32)
            if datetime(2026, 1, day).weekday() < 5
        )
        response = self.client.post(
            reverse("planificator:generator_perioade"),
            {
                "input_file": csv_upload(rows=["Blocked,2 days,https://example.com/blocked,100"]),
                "year": 2026,
                "months": ["1"],
                "randomness": 5,
                "holidays": holidays,
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "Program incomplet", status_code=400)
        self.assertFalse(ScheduleGeneration.objects.exists())

    def test_sample_csv_is_permission_protected_and_downloadable(self):
        response = self.client.get(reverse("planificator:generator_perioade_sample_csv"))
        self.assertEqual(response.status_code, 200)
        self.assertIn('filename="model_cursuri.csv"', response["Content-Disposition"])


class SettingsStoreTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first = get_user_model().objects.create_user(username="first")
        cls.second = get_user_model().objects.create_user(username="second")
        AppSetting.objects.create(scope="schedule_generator", payload={"year": 2027, "randomness": 2})

    def test_global_defaults_and_user_overrides_are_merged(self):
        save_settings("schedule_generator", self.first, {"year": 2028, "months": [1]})
        self.assertEqual(get_settings("schedule_generator", self.first)["year"], 2028)
        self.assertEqual(get_settings("schedule_generator", self.first)["randomness"], 2)
        self.assertEqual(get_settings("schedule_generator", self.second)["year"], 2027)

    def test_users_cannot_overwrite_each_other(self):
        save_settings("schedule_generator", self.first, {"months": [1]})
        save_settings("schedule_generator", self.second, {"months": [2]})
        self.assertEqual(get_settings("schedule_generator", self.first)["months"], [1])
        self.assertEqual(get_settings("schedule_generator", self.second)["months"], [2])

    def test_database_errors_are_not_silenced(self):
        with self.assertLogs("apps.planificator.settings_store", level="ERROR"):
            with patch("apps.planificator.settings_store.AppSetting.objects.filter", side_effect=DatabaseError("down")):
                with self.assertRaises(DatabaseError):
                    get_settings("schedule_generator", self.first)


class FileHandlerTests(TestCase):
    def test_at_delimited_csv_returns_typed_rows(self):
        content = (
            'Title@"Durata Curs"@investitie@Permalink\n'
            '"Curs real unu"@"1 zi"@"200 euro"@https://example.com/unu/\n'
            '"Curs real doi"@"2 zile"@"300 euro"@https://example.com/doi/\n'
        ).encode()
        rows = read_input_file(content, ".csv")
        self.assertEqual(rows[0].title, "Curs real unu")
        self.assertEqual(rows[1].duration, 2)

    def test_xlsx_is_read_in_read_only_compatible_shape(self):
        workbook = Workbook()
        sheet = workbook.active
        sheet.append(["Title", "Durata Curs", "Permalink", "investitie"])
        sheet.append(["Curs", "3 zile", "https://example.com/curs", None])
        output = io.BytesIO()
        workbook.save(output)
        rows = read_input_file(output.getvalue(), ".xlsx")
        self.assertEqual(rows[0].investment, "")

    def test_blank_required_value_has_row_specific_error(self):
        with self.assertRaisesRegex(Exception, "Rândul 2: Permalink"):
            read_input_file(b"Title,Durata Curs,Permalink\nCurs,2 zile,\n", ".csv")

    def test_excel_export_preserves_duplicate_titles_and_neutralizes_formulas(self):
        schedule = []
        for source_row, investment in ((2, "+2"), (3, "@cmd")):
            schedule.append({
                "source_row": source_row,
                "original_order": source_row - 2,
                "Title": "=1+1",
                "Permalink": "https://example.com",
                "Durata Curs": "-3 zile",
                "investitie": investment,
                "date_range": "05.01.2026",
                "month": 1,
            })
        workbook = load_workbook(io.BytesIO(create_excel_export(schedule, 2026)))
        sheet = workbook["Program"]
        self.assertEqual(sheet.max_row, 3)
        self.assertEqual(sheet["A2"].data_type, "s")
        self.assertEqual(sheet["A2"].value, "'=1+1")
        self.assertEqual(sheet["D2"].value, "'+2")
        self.assertEqual(sheet["E1"].value, "Ianuarie")


class GenerationCleanupTests(TestCase):
    def test_cleanup_command_removes_only_expired_generations(self):
        user = get_user_model().objects.create_user(username="cleanup")
        expired = generation_for(user, expired=True)
        active = generation_for(user)
        call_command("purge_expired_schedule_generations", verbosity=0)
        self.assertFalse(ScheduleGeneration.objects.filter(pk=expired.pk).exists())
        self.assertTrue(ScheduleGeneration.objects.filter(pk=active.pk).exists())
```

## `apps/planificator/tests_course_updater.py`

Size: 9.8 KB

Redacted secret-like assignments: 1

```python
from datetime import date
import json
import socket
from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase, TestCase
from django.urls import reverse
import requests

from .models import AppSetting
from .validators import ClientInputError, validate_public_http_url
from .wp_course_updater import (
    WPCourseClient,
    WordPressRequestError,
    build_final_program,
    expand_date_token,
    extract_slug_from_permalink,
    parse_effective_end_date,
    parse_excel_dates_from_row,
    valid_existing_program,
)


def resolved(address: str, port: int = 443):
    family = socket.AF_INET6 if ":" in address else socket.AF_INET
    return [(family, socket.SOCK_STREAM, 6, "", (address, port))]


def http_response(
    status: int,
    *,
    location: str | None = None,
    body: bytes = b"{}",
    headers: dict | None = None,
):
    result = requests.Response()
    result.status_code = status
    result.headers = headers or {}
    if location:
        result.headers["Location"] = location
    result._content = body
    result._content_consumed = True
    return result


class CourseUpdaterDomainTests(SimpleTestCase):
    def test_slug_and_supported_date_formats_are_parsed(self):
        self.assertEqual(
            extract_slug_from_permalink("https://example.test/cursuri/test-course/?x=1"),
            "test-course",
        )
        self.assertEqual(parse_effective_end_date("05.01.2026"), date(2026, 1, 5))
        self.assertEqual(parse_effective_end_date("05-07.01.2026"), date(2026, 1, 7))
        self.assertIsNone(parse_effective_end_date("31.02.2026"))

    def test_date_token_expansion_preserves_the_old_supported_formats(self):
        self.assertEqual(
            expand_date_token("14-16.04.2026"),
            ["14.04.2026", "15.04.2026", "16.04.2026"],
        )
        self.assertEqual(expand_date_token("2026-04-08 00:00:00"), ["08.04.2026"])
        self.assertEqual(expand_date_token("16-14.04.2026"), [])

    def test_month_values_support_old_english_and_current_romanian_exports(self):
        self.assertEqual(
            parse_excel_dates_from_row(
                {
                    "January": "08.01.2026",
                    "Martie": "05-06.03.2026",
                    "Title": "Ignored",
                }
            ),
            ["08.01.2026", "05-06.03.2026"],
        )

    def test_program_merge_filters_expired_rows_and_deduplicates_exact_text(self):
        today = date(2026, 1, 10)
        existing = [
            {"data": "09.01.2026"},
            {"data": "10.01.2026"},
            {"data": "10.01.2026"},
            {"data": "11-12.01.2026"},
            {"data": "invalid"},
        ]
        self.assertEqual(
            valid_existing_program(existing, today),
            [{"data": "10.01.2026"}, {"data": "11-12.01.2026"}],
        )
        self.assertEqual(
            build_final_program(existing, ["10.01.2026", "13.01.2026"], today),
            [
                {"data": "10.01.2026"},
                {"data": "11-12.01.2026"},
                {"data": "13.01.2026"},
            ],
        )


class CourseUpdaterNetworkSafetyTests(SimpleTestCase):
    @patch(
        "apps.planificator.validators.socket.getaddrinfo",
        return_value=resolved("93.184.216.34"),
    )
    def test_public_url_is_allowed(self, _getaddrinfo):
        self.assertEqual(validate_public_http_url("https://example.com"), "https://example.com")

    @patch(
        "apps.planificator.validators.socket.getaddrinfo",
        return_value=resolved("127.0.0.1", 80),
    )
    def test_private_destination_is_blocked(self, _getaddrinfo):
        with self.assertRaises(ClientInputError):
            validate_public_http_url("http://example.test")

    @patch("apps.planificator.validators.socket.getaddrinfo")
    def test_redirect_to_private_destination_is_blocked(self, getaddrinfo):
        getaddrinfo.side_effect = lambda host, port, **kwargs: resolved(
            "127.0.0.1" if host == "127.0.0.1" else "93.184.216.34",
            port,
        )
        client = WPCourseClient("https://example.com", "user", "password")
        client.min_interval_seconds = 0
        client.session.request = Mock(
            return_value=http_response(302, location="http://127.0.0.1/admin")
        )
        with self.assertRaises(ClientInputError):
            client._send_with_safe_redirects("GET", "https://example.com/start")
        self.assertEqual(client.session.request.call_count, 1)

    def test_cloudflare_challenge_has_a_safe_specific_error(self):
        response = http_response(
            403,
            body=b"<title>Just a moment...</title>",
            headers={"cf-mitigated": "challenge"},
        )
        with self.assertRaisesRegex(WordPressRequestError, "browser challenge"):
            WPCourseClient._raise_for_response(response)


class CourseUpdaterWorkflowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="wp-updater",
            password=<redacted>
        )
        cls.user.user_permissions.add(
            Permission.objects.get(codename="use_course_planning")
        )

    def setUp(self):
        self.client.force_login(self.user)

    def json_post(self, route_name: str, payload: dict):
        return self.client.post(
            reverse(f"planificator:{route_name}"),
            data=json.dumps(payload),
            content_type="application/json",
        )

    def credentials(self, **extra):
        return {
            "wp_base_url": "https://example.com",
            "wp_username": "user",
            "wp_app_password": "password",
            **extra,
        }

    def test_page_uses_existing_route_and_exposes_updater_endpoints(self):
        response = self.client.get(reverse("planificator:actualizeaza_cursuri"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "planificator/actualizeaza_cursuri.html")
        self.assertContains(response, reverse("planificator:actualizeaza_cursuri_preview"))
        self.assertContains(response, "Conexiune WordPress")
        self.assertNotContains(response, "<th>Post ID</th>", html=True)
        self.assertNotContains(response, "Identifică")

    def test_preview_is_local_and_accepts_the_current_romanian_export(self):
        upload = SimpleUploadedFile(
            "program.csv",
            (
                "Title,Permalink,Ianuarie,Februarie\n"
                "Course,https://example.com/course/test,09.01.2026,12-13.02.2026\n"
            ).encode("utf-8"),
            content_type="text/csv",
        )
        with patch("apps.planificator.views.WPCourseClient") as client_class:
            response = self.client.post(
                reverse("planificator:actualizeaza_cursuri_preview"),
                {"input_file": upload},
            )
        self.assertEqual(response.status_code, 200)
        row = response.json()["rows"][0]
        self.assertEqual(row["slug"], "test")
        self.assertEqual(row["excel_dates"], ["09.01.2026", "12-13.02.2026"])
        client_class.assert_not_called()

    @patch("apps.planificator.views.WPCourseClient")
    def test_connect_saves_non_secret_settings_only(self, client_class):
        client_class.return_value.test_connection.return_value = {
            "id": 7,
            "name": "Editor",
        }
        response = self.json_post(
            "actualizeaza_cursuri_connect",
            self.credentials(),
        )
        self.assertEqual(response.status_code, 200)
        setting = AppSetting.objects.get(
            scope="safe_course_date_updater",
            user=self.user,
        )
        self.assertEqual(setting.payload["wp_base_url"], "https://example.com")
        self.assertEqual(setting.payload["wp_username"], "user")
        self.assertNotIn("wp_app_password", setting.payload)

    @patch("apps.planificator.views.timezone.localdate", return_value=date(2026, 1, 10))
    @patch("apps.planificator.views.WPCourseClient")
    def test_fetch_dates_merges_without_updating(self, client_class, _localdate):
        client = client_class.return_value
        client.resolve_course_post_id.return_value = 42
        client.get_course.return_value = {
            "acf": {"program": [{"data": "09.01.2026"}, {"data": "12.01.2026"}]}
        }
        response = self.json_post(
            "actualizeaza_cursuri_fetch_dates",
            self.credentials(
                permalink="https://example.com/course/test",
                slug="test",
                excel_dates=["13.01.2026"],
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["existing_valid_dates"], ["12.01.2026"])
        self.assertEqual(response.json()["final_dates"], ["12.01.2026", "13.01.2026"])
        client.update_course_program.assert_not_called()

    @patch("apps.planificator.views.timezone.localdate", return_value=date(2026, 1, 10))
    @patch("apps.planificator.views.WPCourseClient")
    def test_update_posts_only_the_final_acf_program(self, client_class, _localdate):
        client = client_class.return_value
        client.resolve_course_post_id.return_value = 42
        client.get_course.return_value = {
            "acf": {"program": [{"data": "12.01.2026"}]}
        }
        response = self.json_post(
            "actualizeaza_cursuri_update_row",
            self.credentials(
                permalink="https://example.com/course/test",
                slug="test",
                final_dates=["13.01.2026"],
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["updated"])
        client.update_course_program.assert_called_once_with(
            42,
            [{"data": "12.01.2026"}, {"data": "13.01.2026"}],
            client.auth,
        )
```

## `apps/planificator/tests_scheduler.py`

Size: 2.7 KB

```python
from datetime import datetime

from django.test import SimpleTestCase

from .scheduler import CourseScheduler
from .services import choose_start_date, generate_schedule_from_upload


class CourseSchedulerConstraintTests(SimpleTestCase):
    def test_short_course_must_stay_in_same_work_week_and_month(self):
        scheduler = CourseScheduler(2026, [])
        self.assertFalse(scheduler.can_schedule_course(datetime(2026, 1, 30), 2))
        self.assertFalse(scheduler.can_schedule_course(datetime(2026, 3, 30), 3))

    def test_long_course_can_cross_week_boundary(self):
        self.assertTrue(CourseScheduler(2026, []).can_schedule_course(datetime(2026, 1, 28), 6))

    def test_holiday_blocks_short_and_long_courses(self):
        short = CourseScheduler(2026, ["06.01.2026"])
        long = CourseScheduler(2026, ["30.01.2026"])
        self.assertFalse(short.can_schedule_course(datetime(2026, 1, 5), 2))
        self.assertFalse(long.can_schedule_course(datetime(2026, 1, 28), 6))

    def test_format_date_range_skips_weekend(self):
        self.assertEqual(
            CourseScheduler(2026, []).format_date_range(datetime(2026, 1, 8), 3),
            "08-12.01.2026",
        )

    def test_available_dates_are_cached_by_month_and_duration(self):
        scheduler = CourseScheduler(2026, [])
        first = scheduler.get_available_start_days(1, 3)
        second = scheduler.get_available_start_days(1, 3)
        scheduler.get_available_start_days(1, 2)
        self.assertIs(first, second)
        self.assertEqual(scheduler.available_date_calculations, 2)


class ScheduleGenerationTests(SimpleTestCase):
    def test_every_course_receives_every_selected_month(self):
        content = (
            "Title,Durata Curs,Permalink\n"
            "Același titlu,2 zile,https://example.com/unu\n"
            "Același titlu,2 zile,https://example.com/doi\n"
        ).encode()
        result = generate_schedule_from_upload(
            file_bytes=content,
            file_extension=".csv",
            year=2026,
            months=[1, 2],
            randomness=5,
            holidays=[],
            random_seed=42,
        )
        self.assertEqual(len(result.schedule), 4)
        self.assertEqual({row["source_row"] for row in result.schedule}, {2, 3})
        self.assertEqual(result.calendar_calculations, 2)

    def test_long_course_uses_earliest_allowed_date(self):
        available = [datetime(2026, 1, 20), datetime(2026, 1, 5), datetime(2026, 1, 12)]
        selected = choose_start_date(
            available_dates=available,
            scheduled_dates=set(),
            randomness=10,
            duration=6,
        )
        self.assertEqual(selected, datetime(2026, 1, 5))
```

## `apps/planificator/tests_word_converter.py`

Size: 14.1 KB

```python
import base64
import io
import json
from pathlib import Path
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, SimpleTestCase, TestCase
from django.urls import reverse
from docx import Document
from openpyxl import Workbook

from .word_matching import (
    apply_word_matches,
    build_word_course_rows,
    build_word_match_preview,
    confident_match_from_scores,
    normalize_title,
    read_schedule_rows,
    score_schedule_matches,
)


def word_document_bytes(rows=None):
    rows = rows or [("Curs exact", "2 zile", "100", "", "", "")]
    document = Document()
    table = document.add_table(rows=len(rows), cols=6)
    for table_row, values in zip(table.rows, rows):
        for cell, value in zip(table_row.cells, values):
            cell.text = value
    output = io.BytesIO()
    document.save(output)
    return output.getvalue()


def schedule_row(row_index, title, dates=None):
    return {
        "row_index": row_index,
        "title": title,
        "normalized_title": normalize_title(title),
        "dates": dates or ["", "", ""],
    }


def word_upload(content=None):
    return SimpleUploadedFile(
        "planificare.docx",
        content or word_document_bytes(),
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )


def schedule_upload(content=None, name="program.csv"):
    return SimpleUploadedFile(
        name,
        content
        or b"Title,Ianuarie,Februarie,Martie\nCurs exact,05-06.01.2026,02-03.02.2026,02-03.03.2026\n",
        content_type="text/csv",
    )


class WordScheduleParsingTests(SimpleTestCase):
    def test_csv_accepts_english_months_and_keeps_first_three_non_empty_dates(self):
        rows = read_schedule_rows(
            b"Title,January,February,March,April\nCourse,05.01.2026,,02.03.2026,06.04.2026\n",
            ".csv",
        )

        self.assertEqual(rows[0]["title"], "Course")
        self.assertEqual(
            rows[0]["dates"],
            ["05.01.2026", "02.03.2026", "06.04.2026"],
        )

    def test_xlsx_accepts_month_headers_emitted_by_current_generator(self):
        workbook = Workbook()
        sheet = workbook.active
        sheet.append(["Title", "Ianuarie", "Februarie", "Martie"])
        sheet.append(["Curs", "05.01.2026", "02.02.2026", None])
        output = io.BytesIO()
        workbook.save(output)

        rows = read_schedule_rows(output.getvalue(), ".xlsx")

        self.assertEqual(rows[0]["dates"], ["05.01.2026", "02.02.2026", ""])

    def test_missing_title_months_and_corrupt_xlsx_are_rejected(self):
        with self.assertRaisesRegex(Exception, "Title"):
            read_schedule_rows(b"January\n05.01.2026\n", ".csv")
        with self.assertRaisesRegex(Exception, "coloane lunare"):
            read_schedule_rows(b"Title\nCourse\n", ".csv")
        with self.assertRaisesRegex(Exception, "structur"):
            read_schedule_rows(b"not-a-workbook", ".xlsx")


class WordMatchingLogicTests(SimpleTestCase):
    def test_normalization_handles_entities_diacritics_punctuation_and_spacing(self):
        self.assertEqual(
            normalize_title("  Audit &amp; Îmbunătățire—ISO 9001 "),
            "audit imbunatatire iso 9001",
        )

    def test_unique_exact_match_wins_before_fuzzy_candidates(self):
        rows = [
            schedule_row(4, "Managementul calității"),
            schedule_row(9, "Managementul mediului"),
        ]

        scored = score_schedule_matches("Managementul calitatii", rows)

        self.assertEqual(len(scored), 1)
        self.assertTrue(scored[0]["exact"])
        self.assertEqual(confident_match_from_scores("Managementul calitatii", scored), rows[0])

    def test_ambiguous_fuzzy_match_needs_review(self):
        rows = [
            schedule_row(0, "Auditor intern ISO 9001"),
            schedule_row(1, "Auditor intern ISO 14001"),
            schedule_row(2, "Prim ajutor"),
        ]
        scored = score_schedule_matches("Auditor intern ISO", rows)

        self.assertGreater(scored[0]["score"], scored[2]["score"])
        self.assertIsNone(
            confident_match_from_scores(
                "Auditor intern ISO",
                scored,
                {"min_match_score": 70, "min_token_coverage": 60, "min_match_gap": 8},
            )
        )

    def test_standard_code_breaks_a_close_tie(self):
        rows = [
            schedule_row(0, "Auditor intern ISO 9001 sisteme"),
            schedule_row(1, "Auditor intern ISO 14001 sisteme"),
        ]
        scored = score_schedule_matches("Curs auditor intern 9001", rows)

        matched = confident_match_from_scores(
            "Curs auditor intern 9001",
            scored,
            {"min_match_score": 99, "min_token_coverage": 99, "min_match_gap": 50},
        )

        self.assertEqual(matched, rows[0])

    def test_word_row_detection_skips_merged_and_sparse_rows(self):
        document = Document()
        table = document.add_table(rows=3, cols=6)
        table.rows[0].cells[0].merge(table.rows[0].cells[5]).text = "Antet"
        table.rows[1].cells[0].text = "Rând incomplet"
        for index, value in enumerate(("Curs", "2 zile", "100", "", "", "")):
            table.rows[2].cells[index].text = value

        rows = build_word_course_rows(document)

        self.assertEqual([row["title"] for row in rows], ["Curs"])

    def test_preview_and_generation_modify_only_selected_date_cells(self):
        word_bytes = word_document_bytes(
            [
                ("Curs exact", "2 zile", "100", "vechi 1", "vechi 2", "vechi 3"),
                ("Fără potrivire", "1 zi", "50", "păstrează 1", "păstrează 2", "păstrează 3"),
            ]
        )
        schedule_rows = [
            schedule_row(7, "Curs exact", ["nou 1", "nou 2", "nou 3"]),
            schedule_row(8, "Alt curs", ["alt 1", "alt 2", "alt 3"]),
        ]
        preview = build_word_match_preview(
            word_bytes,
            schedule_rows,
            {"min_match_score": 88, "min_token_coverage": 70, "min_match_gap": 8},
        )
        output, matched, skipped = apply_word_matches(word_bytes, schedule_rows, {0: 7})
        result = Document(io.BytesIO(output))

        self.assertEqual(preview["rows"][0]["selected_row_index"], 7)
        self.assertEqual(preview["rows"][1]["status"], "needs_review")
        self.assertLessEqual(len(preview["rows"][1]["candidates"]), 5)
        self.assertEqual((matched, skipped), (1, 1))
        self.assertEqual(
            [cell.text for cell in result.tables[0].rows[0].cells],
            ["Curs exact", "2 zile", "100", "nou 1", "nou 2", "nou 3"],
        )
        self.assertEqual(
            [cell.text for cell in result.tables[0].rows[1].cells][3:],
            ["păstrează 1", "păstrează 2", "păstrează 3"],
        )


class WordConverterViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="word-user", password="test")
        cls.permission = Permission.objects.get(
            codename="use_word_matcher",
            content_type__app_label="planificator",
        )
        cls.user.user_permissions.add(cls.permission)

    def setUp(self):
        self.client.force_login(self.user)

    def test_page_uses_app_template_active_navigation_and_separate_permission(self):
        response = self.client.get(reverse("planificator:word_converter"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "planificator/word_converter.html")
        self.assertContains(response, "Convertor planificare Word")
        self.assertContains(response, 'aria-current="page"')
        self.assertContains(response, "Convertor Word")
        self.assertNotContains(response, "Generator perioade")
        self.assertContains(response, 'name="csrfmiddlewaretoken"')

    def test_anonymous_missing_permission_and_superuser_boundaries(self):
        self.client.logout()
        url = reverse("planificator:word_converter")
        response = self.client.get(url)
        self.assertRedirects(response, f"{reverse('login')}?next={url}")

        other = get_user_model().objects.create_user(username="course-only")
        other.user_permissions.add(
            Permission.objects.get(
                codename="use_course_planning",
                content_type__app_label="planificator",
            )
        )
        self.client.force_login(other)
        self.assertEqual(self.client.get(url).status_code, 403)

        superuser = get_user_model().objects.create_superuser(username="word-root", password="test")
        self.client.force_login(superuser)
        self.assertEqual(self.client.get(url).status_code, 200)

    def test_page_is_get_only_and_endpoints_are_post_only(self):
        self.assertEqual(self.client.post(reverse("planificator:word_converter")).status_code, 405)
        self.assertEqual(self.client.get(reverse("planificator:word_match_preview")).status_code, 405)
        self.assertEqual(self.client.get(reverse("planificator:word_match_generate")).status_code, 405)

    def test_preview_and_generate_contract(self):
        preview = self.client.post(
            reverse("planificator:word_match_preview"),
            {"word_file": word_upload(), "schedule_file": schedule_upload()},
        )

        self.assertEqual(preview.status_code, 200)
        preview_payload = preview.json()
        self.assertTrue(preview_payload["success"])
        self.assertEqual(preview_payload["matched_count"], 1)
        self.assertEqual(preview_payload["rows"][0]["selected_row_index"], 0)

        generated = self.client.post(
            reverse("planificator:word_match_generate"),
            data=json.dumps(
                {
                    "word_file_b64": preview_payload["word_file_b64"],
                    "schedule_options": preview_payload["schedule_options"],
                    "matches": [{"word_row_index": 0, "schedule_row_index": 0}],
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(generated.status_code, 200)
        self.assertEqual(
            generated["Content-Type"],
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
        self.assertIn("planificare_cursuri_actualizata.docx", generated["Content-Disposition"])
        self.assertEqual(generated["X-Matched-Course-Rows"], "1")
        self.assertEqual(generated["X-Skipped-Course-Rows"], "0")
        document = Document(io.BytesIO(generated.content))
        self.assertEqual(
            [cell.text for cell in document.tables[0].rows[0].cells][3:],
            ["05-06.01.2026", "02-03.02.2026", "02-03.03.2026"],
        )

    def test_invalid_files_json_base64_and_indexes_return_safe_errors(self):
        corrupt = self.client.post(
            reverse("planificator:word_match_preview"),
            {"word_file": word_upload(b"not-a-docx"), "schedule_file": schedule_upload()},
        )
        self.assertEqual(corrupt.status_code, 400)
        self.assertNotIn("zip", corrupt.content.decode().lower())

        invalid_json = self.client.post(
            reverse("planificator:word_match_generate"),
            data="{bad-json",
            content_type="application/json",
        )
        self.assertEqual(invalid_json.status_code, 400)

        invalid_base64 = self.client.post(
            reverse("planificator:word_match_generate"),
            data=json.dumps(
                {"word_file_b64": "%%%", "schedule_options": [], "matches": []}
            ),
            content_type="application/json",
        )
        self.assertEqual(invalid_base64.status_code, 400)

        word_b64 = base64.b64encode(word_document_bytes()).decode("ascii")
        unknown_index = self.client.post(
            reverse("planificator:word_match_generate"),
            data=json.dumps(
                {
                    "word_file_b64": word_b64,
                    "schedule_options": [
                        {"row_index": 0, "title": "Curs exact", "dates": ["1", "2", "3"]}
                    ],
                    "matches": [{"word_row_index": 9, "schedule_row_index": 0}],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(unknown_index.status_code, 400)
        self.assertIn("inexistent", unknown_index.json()["error"])

    @patch("apps.planificator.forms.MAX_WORD_UPLOAD_BYTES", 4)
    def test_oversized_word_upload_is_rejected_before_document_parsing(self):
        response = self.client.post(
            reverse("planificator:word_match_preview"),
            {"word_file": word_upload(b"12345"), "schedule_file": schedule_upload()},
        )

        self.assertEqual(response.status_code, 413)
        self.assertIn("0 MB", response.json()["error"])

    def test_duplicate_schedule_indexes_are_rejected(self):
        option = {"row_index": 0, "title": "Curs exact", "dates": ["1", "2", "3"]}
        response = self.client.post(
            reverse("planificator:word_match_generate"),
            data=json.dumps(
                {
                    "word_file_b64": base64.b64encode(word_document_bytes()).decode("ascii"),
                    "schedule_options": [option, option],
                    "matches": [],
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("duplicate", response.json()["error"])

    def test_preview_requires_csrf(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.user)
        response = client.post(
            reverse("planificator:word_match_preview"),
            {"word_file": word_upload(), "schedule_file": schedule_upload()},
        )
        self.assertEqual(response.status_code, 403)

    def test_frontend_does_not_parse_html_strings(self):
        source = (
            Path(__file__).resolve().parent / "static" / "planificator" / "word_converter.js"
        ).read_text(encoding="utf-8")
        self.assertNotIn("innerHTML", source)
        self.assertNotIn("insertAdjacentHTML", source)
```

## `apps/planificator/tests_xml_export.py`

Size: 8.4 KB

Redacted secret-like assignments: 1

```python
import xml.etree.ElementTree as ET

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from django.utils import timezone

from .file_handlers import create_excel_export
from .models import AppSetting
from .xml_export import create_xml_export, read_xml_schedule


class XmlExportContractTests(SimpleTestCase):
    def test_xml_structure_ids_dates_constants_and_order_are_stable(self):
        xml_text = create_xml_export(
            [
                {"course_name": "Course A", "date_range": "5.01.2026", "permalink": "/a"},
                {
                    "course_name": "Course B",
                    "date_range": "30.01-2.02.2026",
                    "permalink": "/b",
                },
                {
                    "course_name": "Course A",
                    "date_range": "12-13.02.2026",
                    "permalink": "/a",
                },
            ],
            2026,
            start_post_id=31000,
        )

        root = ET.fromstring(xml_text)
        items = root.findall("item")
        self.assertEqual([item.findtext("title") for item in items], ["Course A", "Course A", "Course B"])
        self.assertEqual([item.findtext("ID") for item in items], ["31000", "31001", "31002"])
        self.assertEqual(items[0].findtext("post/post_author"), "5")
        self.assertEqual(items[0].findtext("post/post_status"), "draft")
        self.assertEqual(items[0].findtext("meta/mec_more_info_title"), "perioada 1")
        self.assertEqual(items[1].findtext("meta/mec_more_info_title"), "perioada 2")
        self.assertEqual(items[0].findtext("meta/mec_start_date"), "2026-01-05")
        self.assertEqual(items[1].findtext("meta/mec_end_date"), "2026-02-13")
        self.assertEqual(items[2].findtext("meta/mec_start_date"), "2026-01-30")
        self.assertEqual(items[2].findtext("meta/mec_end_date"), "2026-02-02")
        self.assertEqual(items[0].findtext("meta/mec_start_day_seconds"), "28800")
        self.assertEqual(items[0].findtext("meta/mec_end_day_seconds"), "64800")
        self.assertEqual(items[0].findtext("mec/post_id"), "31000")
        self.assertEqual(items[0].findtext("time/start"), "All Day")

    def test_default_id_and_unsupported_date_contract(self):
        xml_text = create_xml_export(
            [{"course_name": "Course", "date_range": "01.01.2026", "permalink": ""}],
            2026,
        )
        self.assertEqual(ET.fromstring(xml_text).findtext("item/ID"), "20000")

        with self.assertRaisesRegex(ValueError, "Unsupported date format"):
            create_xml_export(
                [{"course_name": "Course", "date_range": "January 1", "permalink": ""}],
                2026,
            )

    def test_legacy_and_current_month_headers_keep_source_order(self):
        schedule = read_xml_schedule(
            (
                "Title,Permalink,February,Luna 1,Ianuarie\n"
                "Course A,/a,12-13.02.2026,5.03.2026,5.01.2026\n"
            ).encode("utf-8"),
            ".csv",
        )

        self.assertEqual(
            [event["date_range"] for event in schedule],
            ["12-13.02.2026", "5.03.2026", "5.01.2026"],
        )


class XmlExportViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="xml-user",
            password=<redacted>
        )
        cls.permission = Permission.objects.get(codename="use_xml_export")
        cls.user.user_permissions.add(cls.permission)

    def setUp(self):
        self.client.force_login(self.user)

    def test_page_uses_app_template_navigation_and_separate_permission(self):
        response = self.client.get(reverse("planificator:xml_formatter"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "planificator/xml_formatter.html")
        self.assertContains(response, "Convertor XML")
        self.assertContains(response, reverse("planificator:xml_export"))
        self.assertContains(response, 'name="start_post_id"')
        self.assertContains(response, reverse("planificator:xml_export"))
        self.assertContains(response, reverse("planificator:xml_formatter"))
        self.assertContains(response, 'class="transition-none active font-semibold"')
        self.assertContains(response, 'aria-current="page"')

    def test_export_uses_submitted_start_id_and_legacy_xml_download_contract(self):
        AppSetting.objects.create(
            scope="schedule_generator",
            user=self.user,
            payload={"xml_start_post_id": 31000},
        )
        upload = SimpleUploadedFile(
            "program.csv",
            b"Title,Permalink,January\nCourse A,/course-a,5.01.2026\n",
            content_type="text/csv",
        )

        response = self.client.post(
            reverse("planificator:xml_export"),
            {"input_file": upload, "start_post_id": 32000},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/xml")
        self.assertEqual(
            response["Content-Disposition"],
            f'attachment; filename="formatted_courses_{timezone.localdate().year}.xml"',
        )
        root = ET.fromstring(response.content)
        self.assertEqual(root.findtext("item/ID"), "32000")
        self.assertEqual(root.findtext("item/meta/mec_read_more"), "/course-a")

    def test_export_accepts_current_romanian_schedule_workbook(self):
        workbook = create_excel_export(
            [
                {
                    "Title": "Curs curent",
                    "Permalink": "https://example.com/curs",
                    "Durata Curs": "2 zile",
                    "investitie": "1000",
                    "date_range": "10-11.04.2026",
                    "month": 4,
                    "source_row": 2,
                    "original_order": 0,
                }
            ],
            2026,
        )
        upload = SimpleUploadedFile(
            "program.xlsx",
            workbook,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

        response = self.client.post(
            reverse("planificator:xml_export"),
            {"input_file": upload, "start_post_id": 20000},
        )

        self.assertEqual(response.status_code, 200)
        root = ET.fromstring(response.content)
        self.assertEqual(root.findtext("item/title"), "Curs curent")
        self.assertEqual(root.findtext("item/meta/mec_start_date"), "2026-04-10")
        self.assertEqual(root.findtext("item/meta/mec_end_date"), "2026-04-11")

    def test_invalid_files_return_stable_json_errors(self):
        missing_columns = SimpleUploadedFile(
            "program.csv",
            b"Title,January\nCourse A,5.01.2026\n",
            content_type="text/csv",
        )
        response = self.client.post(
            reverse("planificator:xml_export"),
            {"input_file": missing_columns, "start_post_id": 20000},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Missing required columns: Permalink")

        invalid_date = SimpleUploadedFile(
            "program.csv",
            b"Title,Permalink,January\nCourse A,/a,January 1\n",
            content_type="text/csv",
        )
        response = self.client.post(
            reverse("planificator:xml_export"),
            {"input_file": invalid_date, "start_post_id": 20000},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["error"],
            "Unable to read the uploaded schedule or create XML.",
        )

    def test_authentication_permission_and_method_boundaries(self):
        page_url = reverse("planificator:xml_formatter")
        self.client.logout()
        response = self.client.get(page_url)
        self.assertRedirects(response, f"{reverse('login')}?next={page_url}")

        other = get_user_model().objects.create_user(username="xml-other")
        self.client.force_login(other)
        self.assertEqual(self.client.get(page_url).status_code, 403)

        self.client.force_login(self.user)
        self.assertEqual(self.client.post(page_url).status_code, 405)
        self.assertEqual(self.client.get(reverse("planificator:xml_export")).status_code, 405)
```

## `apps/planificator/urls.py`

Size: 2.3 KB

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

## `apps/planificator/validators.py`

Size: 7.0 KB

```python
from datetime import datetime
import ipaddress
import json
import re
import socket
from typing import Any
from urllib.parse import urlsplit, urlunsplit


MAX_TABULAR_UPLOAD_BYTES = 20 * 1024 * 1024
MAX_WORD_UPLOAD_BYTES = 20 * 1024 * 1024
MAX_JSON_BYTES = 32 * 1024 * 1024
MAX_COURSE_ROWS = 5_000
MAX_TABULAR_COLUMNS = 50
TABULAR_EXTENSIONS = {".csv", ".xlsx"}
WORD_EXTENSIONS = {".docx"}
HOSTNAME_RE = re.compile(
    r"^(?=.{1,253}\.?$)(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)*"
    r"[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.?$"
)
BLOCKED_METADATA_HOSTNAMES = {
    "metadata.google.internal",
    "metadata.azure.internal",
    "instance-data.ec2.internal",
}


class ClientInputError(ValueError):
    def __init__(self, message: str, *, status: int = 400):
        super().__init__(message)
        self.message = message
        self.status = status


def parse_json_object(raw_body: bytes) -> dict[str, Any]:
    if len(raw_body) > MAX_JSON_BYTES:
        raise ClientInputError("Request body is too large.", status=413)
    try:
        payload = json.loads(raw_body.decode("utf-8") or "{}")
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ClientInputError("Request body must be a valid JSON object.") from exc
    if not isinstance(payload, dict):
        raise ClientInputError("Request body must be a JSON object.")
    return payload


def require_list(value: Any, field: str, *, max_items: int = 5000) -> list[Any]:
    if not isinstance(value, list):
        raise ClientInputError(f'Field "{field}" must be a list.')
    if len(value) > max_items:
        raise ClientInputError(f'Field "{field}" contains too many items.')
    return value


def require_string(
    value: Any,
    field: str,
    *,
    allow_empty: bool = True,
    max_length: int = 2048,
) -> str:
    if not isinstance(value, str):
        raise ClientInputError(f'Field "{field}" must be text.')
    clean = value.strip()
    if not allow_empty and not clean:
        raise ClientInputError(f'Field "{field}" is required.')
    if len(clean) > max_length:
        raise ClientInputError(f'Field "{field}" is too long.')
    return clean


def require_int(value: Any, field: str, *, minimum: int, maximum: int) -> int:
    if isinstance(value, bool):
        raise ClientInputError(f'Field "{field}" must be an integer.')
    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise ClientInputError(f'Field "{field}" must be an integer.') from exc
    if str(value).strip() not in {str(parsed), f"+{parsed}"} and not isinstance(value, int):
        raise ClientInputError(f'Field "{field}" must be an integer.')
    if not minimum <= parsed <= maximum:
        raise ClientInputError(f'Field "{field}" must be between {minimum} and {maximum}.')
    return parsed


def validate_ro_date(value, field: str = "date") -> str:
    if not isinstance(value, str) or not value.strip() or len(value.strip()) > 10:
        raise ClientInputError(f'Câmpul "{field}" trebuie să conțină o dată DD.MM.YYYY.')
    clean = value.strip()
    try:
        parsed = datetime.strptime(clean, "%d.%m.%Y")
    except ValueError as exc:
        raise ClientInputError(f'Field "{field}" must use DD.MM.YYYY format.') from exc
    return parsed.strftime("%d.%m.%Y")


def validate_holiday_list(values) -> list[str]:
    if not isinstance(values, (list, tuple)):
        raise ClientInputError("Zilele nelucrătoare trebuie trimise ca listă.")
    holidays = list(values)
    if len(holidays) > 366:
        raise ClientInputError("Too many holidays were provided.")
    return [validate_ro_date(value, "holidays") for value in holidays]


def validate_upload(upload, *, allowed_extensions: set[str], max_bytes: int, label: str) -> str:
    if upload is None:
        raise ClientInputError(f"{label} is required.")
    name = str(getattr(upload, "name", "") or "")
    extension = "." + name.rsplit(".", 1)[-1].lower() if "." in name else ""
    if extension not in allowed_extensions:
        allowed = ", ".join(sorted(allowed_extensions))
        raise ClientInputError(f"{label} must use one of these formats: {allowed}.")
    size = getattr(upload, "size", None)
    if not isinstance(size, int) or size <= 0:
        raise ClientInputError(f"{label} is empty.")
    if size > max_bytes:
        raise ClientInputError(f"{label} must be {max_bytes // (1024 * 1024)} MB or smaller.", status=413)
    return extension


def validate_http_url_syntax(value: str, *, label: str = "WordPress base URL") -> str:
    try:
        parsed = urlsplit(value)
        port = parsed.port
    except ValueError as exc:
        raise ClientInputError(f"{label} is invalid.") from exc
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ClientInputError(f"{label} must use http or https.")
    if parsed.username is not None or parsed.password is not None:
        raise ClientInputError(f"{label} must not contain credentials.")
    if parsed.fragment:
        raise ClientInputError(f"{label} must not contain a fragment.")
    if not parsed.hostname or parsed.query:
        raise ClientInputError(f"{label} is invalid.")
    host = parsed.hostname.rstrip(".").lower()
    if not host or (not _is_ip_literal(host) and not HOSTNAME_RE.fullmatch(host)):
        raise ClientInputError(f"{label} contains an invalid hostname.")
    if host == "localhost" or host.endswith(".localhost") or host in BLOCKED_METADATA_HOSTNAMES:
        raise ClientInputError(f"{label} points to a prohibited destination.")
    default_port = 443 if parsed.scheme.lower() == "https" else 80
    netloc = f"[{host}]" if ":" in host else host
    if port and port != default_port:
        netloc = f"{netloc}:{port}"
    path = parsed.path.rstrip("/")
    return urlunsplit((parsed.scheme.lower(), netloc, path, "", ""))


def _is_ip_literal(host: str) -> bool:
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


def _is_prohibited_ip(value: str) -> bool:
    address = ipaddress.ip_address(value.split("%", 1)[0])
    if isinstance(address, ipaddress.IPv6Address) and address.ipv4_mapped:
        address = address.ipv4_mapped
    return not address.is_global


def validate_public_http_url(value: str) -> str:
    normalized = validate_http_url_syntax(value)
    parsed = urlsplit(normalized)
    host = parsed.hostname or ""
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    try:
        addresses = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
    except socket.gaierror as exc:
        raise ClientInputError("WordPress host could not be resolved.") from exc
    if not addresses:
        raise ClientInputError("WordPress host could not be resolved.")
    try:
        prohibited = any(_is_prohibited_ip(item[4][0]) for item in addresses)
    except ValueError as exc:
        raise ClientInputError("WordPress host resolved to an invalid address.") from exc
    if prohibited:
        raise ClientInputError("WordPress base URL points to a prohibited destination.")
    return normalized
```

## `apps/planificator/views.py`

Size: 31.6 KB

```python
import base64
import csv
import json
import logging
from io import StringIO
from pathlib import Path
from zipfile import BadZipFile

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, TemplateView
from docx.opc.exceptions import PackageNotFoundError

from .constants import ROMANIAN_MONTH_NAMES
from .file_handlers import create_excel_export, read_tabular_rows
from .forms import (
    SafeCoursePreviewForm,
    ScheduleExportForm,
    ScheduleGeneratorForm,
    WordMatchGenerationForm,
    WordMatchUploadForm,
    XmlExportForm,
    normalize_schedule_initial,
)
from .presentation import build_preview_rows, build_source_preview, selected_month_headers
from .selectors import get_owned_generation, list_owned_generations
from .services import (
    GenerationSourceUnavailable,
    GenerationWorkflowError,
    create_schedule_generation,
)
from .settings_store import get_settings, save_settings
from .validators import (
    MAX_JSON_BYTES,
    ClientInputError,
    require_int,
    require_list,
    require_string,
)
from .word_matching import apply_word_matches, build_word_match_preview, read_schedule_rows
from .wp_course_updater import (
    WPCourseClient,
    WordPressRequestError,
    build_final_program,
    extract_slug_from_permalink,
    parse_effective_end_date,
    parse_excel_dates_from_row,
    valid_existing_program,
)
from .xml_export import create_xml_export, read_xml_schedule

logger = logging.getLogger(__name__)


class PlanificatorPermissionMixin(LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = "planificator.use_course_planning"


class WordMatcherPermissionMixin(LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = "planificator.use_word_matcher"


class XmlExportPermissionMixin(LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = "planificator.use_xml_export"


def _form_error(form, fallback: str) -> str:
    for errors in form.errors.values():
        if errors:
            return str(errors[0])
    return fallback


def _json_error(message: str, *, status: int = 400) -> JsonResponse:
    return JsonResponse({"success": False, "error": message}, status=status)


def _json_request_data(request: HttpRequest) -> dict:
    if request.content_type != "application/json":
        raise ClientInputError("Cererea trebuie trimisă ca JSON.")
    if len(request.body) > MAX_JSON_BYTES:
        raise ClientInputError("Cererea este prea mare.", status=413)
    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ClientInputError("Cererea nu conține un obiect JSON valid.") from exc
    if not isinstance(payload, dict):
        raise ClientInputError("Cererea trebuie să conțină un obiect JSON.")
    return payload


def build_generator_form(user, *, source_generation_id=None) -> ScheduleGeneratorForm:
    settings = get_settings("schedule_generator", user)
    initial = normalize_schedule_initial(settings)
    if source_generation_id:
        initial["source_generation_id"] = source_generation_id
    return ScheduleGeneratorForm(initial=initial)


def generator_context(form: ScheduleGeneratorForm, **extra) -> dict:
    if form.is_bound and hasattr(form, "cleaned_data"):
        months = list(form.cleaned_data.get("months", []))
        holidays = list(form.cleaned_data.get("holidays", []))
    else:
        months = [int(month) for month in form.initial.get("months", []) if str(month).isdigit()]
        holidays_value = form.initial.get("holidays", "")
        holidays = [value.strip() for value in str(holidays_value).splitlines() if value.strip()]
    context = {
        "form": form,
        "selected_months": months,
        "selected_month_count": len(months),
        "selected_month_headers": selected_month_headers(months),
        "holiday_count": len(holidays),
        "working_days_label": "Luni – vineri",
        "page_messages": [],
        "preview_rows": [],
        "source_preview_rows": [],
        "unscheduled_courses": {},
    }
    context.update(extra)
    return context


class PeriodGeneratorView(PlanificatorPermissionMixin, TemplateView):
    template_name = "planificator/generator_perioade.html"

    def get_context_data(self, **kwargs):
        form = kwargs.pop("form", None) or build_generator_form(self.request.user)
        return generator_context(form, **super().get_context_data(**kwargs))

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        form = ScheduleGeneratorForm(request.POST, request.FILES)
        if not form.is_valid():
            context = generator_context(
                form,
                page_messages=[{
                    "level": "error",
                    "title": "Formularul este incomplet",
                    "body": "Corectează câmpurile marcate și încearcă din nou.",
                }],
            )
            return self.render_to_response(context, status=getattr(form, "upload_error_status", 400))

        try:
            workflow = create_schedule_generation(
                owner=request.user,
                upload=form.cleaned_data.get("input_file"),
                source_generation_id=form.cleaned_data.get("source_generation_id"),
                year=form.cleaned_data["year"],
                months=form.cleaned_data["months"],
                randomness=form.cleaned_data["randomness"],
                holidays=form.cleaned_data["holidays"],
            )
            if workflow.unscheduled_courses:
                context = generator_context(
                    form,
                    uploaded_file_name=workflow.source_file_name,
                    unscheduled_courses=workflow.unscheduled_courses,
                    generation_error="Programul nu poate fi salvat deoarece unele combinații curs/lună lipsesc.",
                    page_messages=[{
                        "level": "error",
                        "title": "Program incomplet",
                        "body": "Ajustează lunile sau zilele nelucrătoare și încearcă din nou.",
                    }],
                )
                return self.render_to_response(context, status=400)
            return redirect(
                "planificator:generator_perioade_result",
                generation_id=workflow.generation.pk,
            )
        except GenerationSourceUnavailable as exc:
            form.add_error("input_file", exc.message)
            return self.render_to_response(
                generator_context(
                    form,
                    page_messages=[{
                        "level": "warning",
                        "title": "Fișier necesar",
                        "body": exc.message,
                    }],
                ),
                status=exc.status,
            )
        except GenerationWorkflowError as exc:
            form.add_error(None, exc.message)
            context = generator_context(
                form,
                uploaded_file_name=exc.source_file_name,
                page_messages=[{
                    "level": "error",
                    "title": "Datele nu pot fi procesate",
                    "body": exc.message,
                }],
            )
            return self.render_to_response(context, status=exc.status)
        except ClientInputError as exc:
            form.add_error(None, exc.message)
            return self.render_to_response(
                generator_context(
                    form,
                    page_messages=[{
                        "level": "error",
                        "title": "Datele nu pot fi procesate",
                        "body": exc.message,
                    }],
                ),
                status=exc.status,
            )
        except Http404:
            raise
        except Exception:
            logger.exception("Unexpected schedule generation failure", extra={"user_id": request.user.pk})
            form.add_error(None, "Fișierul nu a putut fi procesat.")
            return self.render_to_response(
                generator_context(
                    form,
                    page_messages=[{
                        "level": "error",
                        "title": "Eroare la procesare",
                        "body": "Verifică structura fișierului și încearcă din nou.",
                    }],
                ),
                status=400,
            )


class ScheduleResultView(PlanificatorPermissionMixin, TemplateView):
    template_name = "planificator/generator_perioade.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        generation = get_owned_generation(
            generation_id=self.kwargs["generation_id"],
            user=self.request.user,
        )
        form = build_generator_form(self.request.user, source_generation_id=generation.pk)
        context.update(
            generator_context(
                form,
                generation=generation,
                schedule=generation.schedule,
                preview_rows=build_preview_rows(generation.schedule, generation.selected_months),
                source_preview_rows=build_source_preview(generation.schedule),
                source_course_count=generation.source_course_count,
                source_file_digest=generation.source_file_digest[:12],
                uploaded_file_name=generation.source_file_name,
                selected_months=generation.selected_months,
                selected_month_count=len(generation.selected_months),
                selected_month_headers=selected_month_headers(generation.selected_months),
                export_form=ScheduleExportForm(initial={"generation_id": generation.pk}),
            )
        )
        return context


class ScheduleHistoryDetailView(ScheduleResultView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["history_read_only"] = True
        return context


class CourseRefreshView(PlanificatorPermissionMixin, TemplateView):
    template_name = "planificator/actualizeaza_cursuri.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SafeCoursePreviewForm()
        context["updater_settings"] = get_settings(
            "safe_course_date_updater",
            self.request.user,
        )
        return context


def _wp_client_from_payload(payload: dict) -> WPCourseClient:
    return WPCourseClient(
        payload["wp_base_url"],
        payload.get("wp_username", ""),
        payload.get("wp_app_password", ""),
    )


def _validate_wp_payload(
    payload: dict,
    *,
    allowed_fields: set[str],
    require_credentials: bool = True,
) -> dict:
    unknown = sorted(set(payload) - allowed_fields)
    if unknown:
        raise ClientInputError(f"Unknown request field: {unknown[0]}.")
    clean = {
        "wp_base_url": require_string(
            payload.get("wp_base_url"),
            "wp_base_url",
            allow_empty=False,
        )
    }
    if "wp_username" in allowed_fields:
        clean["wp_username"] = require_string(
            payload.get("wp_username", ""),
            "wp_username",
            allow_empty=not require_credentials,
            max_length=150,
        )
    if "wp_app_password" in allowed_fields:
        clean["wp_app_password"] = require_string(
            payload.get("wp_app_password", ""),
            "wp_app_password",
            allow_empty=not require_credentials,
            max_length=500,
        )
    for field in ("permalink", "slug"):
        if field in allowed_fields:
            clean[field] = require_string(
                payload.get(field, ""),
                field,
                max_length=2048 if field == "permalink" else 300,
            )
    if "post_id" in allowed_fields and payload.get("post_id") not in (None, ""):
        clean["post_id"] = require_int(
            payload["post_id"],
            "post_id",
            minimum=1,
            maximum=2_147_483_647,
        )
    for field in ("excel_dates", "final_dates"):
        if field in allowed_fields:
            dates = require_list(payload.get(field, []), field, max_items=1000)
            clean_dates = []
            for value in dates:
                date_value = require_string(value, field, allow_empty=False, max_length=50)
                if parse_effective_end_date(date_value) is None:
                    raise ClientInputError(f'Field "{field}" contains an invalid date.')
                clean_dates.append(date_value)
            clean[field] = clean_dates
    return clean


class CourseRefreshPreviewView(PlanificatorPermissionMixin, View):
    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        form = SafeCoursePreviewForm(request.POST, request.FILES)
        if not form.is_valid():
            return _json_error(
                _form_error(form, "Selectează un fișier CSV sau XLSX."),
                status=getattr(form, "upload_error_status", 400),
            )
        try:
            upload = form.cleaned_data["input_file"]
            raw_rows = read_tabular_rows(upload.read(), form.file_extension)
            if not raw_rows:
                raise ClientInputError("Input file must contain Title and Permalink columns.")
            header = [str(value or "").strip() for value in raw_rows[0]]
            normalized_columns = {
                name.lower(): index for index, name in enumerate(header) if name
            }
            missing = [
                name for name in ("title", "permalink") if name not in normalized_columns
            ]
            if missing:
                raise ClientInputError("Input file must contain Title and Permalink columns.")

            today = timezone.localdate()
            rows = []
            for row_index, values in enumerate(raw_rows[1:]):
                if not any(str(value or "").strip() for value in values):
                    continue
                row = {
                    header[index]: values[index] if index < len(values) else ""
                    for index in range(len(header))
                }
                title = str(row.get(header[normalized_columns["title"]], "") or "").strip()
                permalink = str(
                    row.get(header[normalized_columns["permalink"]], "") or ""
                ).strip()
                slug = extract_slug_from_permalink(permalink)
                excel_dates = parse_excel_dates_from_row(row)
                excel_only_program = build_final_program([], excel_dates, today)
                excel_only_dates = [item["data"] for item in excel_only_program]
                row_payload = {
                    "row_index": row_index,
                    "title": title,
                    "permalink": permalink,
                    "slug": slug,
                    "post_id": None,
                    "existing_valid_dates": [],
                    "excel_dates": excel_dates,
                    "final_dates": excel_only_dates,
                    "status": "preview ready",
                    "error": None,
                    "can_update": bool(slug and excel_only_dates),
                    "payload": {
                        "acf": {
                            "program": excel_only_program if excel_only_program else False
                        }
                    },
                }
                if not permalink:
                    row_payload["status"] = "error"
                    row_payload["error"] = "Missing permalink."
                elif not slug:
                    row_payload["status"] = "error"
                    row_payload["error"] = "Unable to extract slug from permalink."
                rows.append(row_payload)
            return JsonResponse({"success": True, "rows": rows})
        except ClientInputError as exc:
            return _json_error(exc.message, status=exc.status)
        except (ValueError, KeyError, TypeError, UnicodeError, BadZipFile, OSError):
            return _json_error("Unable to read the uploaded schedule file.")


class CourseRefreshConnectView(PlanificatorPermissionMixin, View):
    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        try:
            payload = _validate_wp_payload(
                _json_request_data(request),
                allowed_fields={"wp_base_url", "wp_username", "wp_app_password"},
            )
            user = _wp_client_from_payload(payload).test_connection()
            save_settings(
                "safe_course_date_updater",
                request.user,
                {
                    "wp_base_url": payload["wp_base_url"],
                    "wp_username": payload["wp_username"],
                },
            )
            return JsonResponse(
                {
                    "success": True,
                    "message": "Connected",
                    "user": {
                        "id": user.get("id"),
                        "name": user.get("name")
                        or user.get("slug")
                        or payload["wp_username"],
                    },
                }
            )
        except ClientInputError as exc:
            return _json_error(exc.message, status=exc.status)
        except WordPressRequestError as exc:
            return _json_error(str(exc), status=502)


class CourseRefreshResolveView(PlanificatorPermissionMixin, View):
    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        try:
            payload = _validate_wp_payload(
                _json_request_data(request),
                allowed_fields={
                    "wp_base_url",
                    "wp_username",
                    "wp_app_password",
                    "permalink",
                    "slug",
                },
                require_credentials=False,
            )
            permalink = payload.get("permalink", "")
            slug = payload.get("slug", "") or extract_slug_from_permalink(permalink)
            if not slug:
                raise ClientInputError("Missing slug/permalink.")
            post_id = _wp_client_from_payload(payload).resolve_course_post_id(
                slug=slug,
                permalink=permalink,
            )
            if not post_id:
                return _json_error(
                    "Could not resolve post ID from REST slug lookup.",
                    status=404,
                )
            return JsonResponse({"success": True, "post_id": int(post_id)})
        except ClientInputError as exc:
            return _json_error(exc.message, status=exc.status)
        except WordPressRequestError as exc:
            return _json_error(str(exc), status=502)


class CourseRefreshFetchDatesView(PlanificatorPermissionMixin, View):
    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        try:
            payload = _validate_wp_payload(
                _json_request_data(request),
                allowed_fields={
                    "wp_base_url",
                    "wp_username",
                    "wp_app_password",
                    "permalink",
                    "slug",
                    "post_id",
                    "excel_dates",
                },
            )
            permalink = payload.get("permalink", "")
            slug = payload.get("slug", "") or extract_slug_from_permalink(permalink)
            if not slug:
                raise ClientInputError("Missing slug/permalink.")
            client = _wp_client_from_payload(payload)
            post_id = client.resolve_course_post_id(
                slug=slug,
                permalink=permalink,
                fallback_post_id=payload.get("post_id"),
            )
            if not post_id:
                return _json_error(f"Course not found by slug: {slug}", status=404)
            existing_program = (
                client.get_course(int(post_id)).get("acf", {}).get("program") or []
            )
            today = timezone.localdate()
            current_valid = [
                item["data"] for item in valid_existing_program(existing_program, today)
            ]
            final_valid = [
                item["data"]
                for item in build_final_program(
                    existing_program,
                    payload.get("excel_dates", []),
                    today,
                )
            ]
            final_program = [{"data": value} for value in final_valid]
            return JsonResponse(
                {
                    "success": True,
                    "post_id": int(post_id),
                    "existing_valid_dates": current_valid,
                    "final_dates": final_valid,
                    "payload": {
                        "acf": {"program": final_program if final_program else False}
                    },
                    "can_update": bool(final_valid),
                }
            )
        except ClientInputError as exc:
            return _json_error(exc.message, status=exc.status)
        except WordPressRequestError as exc:
            return _json_error(str(exc), status=502)
        except (TypeError, ValueError, KeyError):
            return _json_error("WordPress returned invalid course data.")


class CourseRefreshUpdateRowView(PlanificatorPermissionMixin, View):
    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        try:
            payload = _validate_wp_payload(
                _json_request_data(request),
                allowed_fields={
                    "wp_base_url",
                    "wp_username",
                    "wp_app_password",
                    "permalink",
                    "slug",
                    "post_id",
                    "final_dates",
                },
            )
            permalink = payload.get("permalink", "")
            slug = payload.get("slug", "") or extract_slug_from_permalink(permalink)
            if not slug:
                raise ClientInputError("Missing slug/permalink.")
            client = _wp_client_from_payload(payload)
            post_id = client.resolve_course_post_id(
                slug=slug,
                permalink=permalink,
                fallback_post_id=payload.get("post_id"),
            )
            if not post_id:
                return _json_error(f"Course not found by slug: {slug}", status=404)
            today = timezone.localdate()
            existing_program = (
                client.get_course(int(post_id)).get("acf", {}).get("program") or []
            )
            current_valid = [
                item["data"] for item in valid_existing_program(existing_program, today)
            ]
            final_valid = [
                item["data"]
                for item in build_final_program(
                    existing_program,
                    payload.get("final_dates", []),
                    today,
                )
            ]
            if current_valid == final_valid:
                return JsonResponse(
                    {
                        "success": True,
                        "status": "no changes",
                        "updated": False,
                        "post_id": int(post_id),
                    }
                )
            client.update_course_program(
                int(post_id),
                [{"data": value} for value in final_valid],
                client.auth,
            )
            return JsonResponse(
                {
                    "success": True,
                    "status": "success",
                    "updated": True,
                    "post_id": int(post_id),
                    "final_dates": final_valid,
                }
            )
        except ClientInputError as exc:
            return _json_error(exc.message, status=exc.status)
        except WordPressRequestError as exc:
            return _json_error(str(exc), status=502)
        except (TypeError, ValueError, KeyError):
            return _json_error("WordPress returned invalid course data.")


class XmlFormatterView(XmlExportPermissionMixin, TemplateView):
    template_name = "planificator/xml_formatter.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        schedule_settings = get_settings("schedule_generator", self.request.user)
        context["form"] = XmlExportForm(
            initial={
                "start_post_id": schedule_settings.get("xml_start_post_id") or 20000
            }
        )
        return context


class XmlExportView(XmlExportPermissionMixin, View):
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        form = XmlExportForm(request.POST, request.FILES)
        if not form.is_valid():
            return JsonResponse(
                {"error": _form_error(form, "Choose a CSV or XLSX file.")},
                status=getattr(form, "upload_error_status", 400),
            )

        upload = form.cleaned_data["input_file"]
        year = timezone.localdate().year
        try:
            schedule = read_xml_schedule(upload.read(), form.file_extension)
            xml_text = create_xml_export(
                schedule,
                year,
                start_post_id=form.cleaned_data["start_post_id"],
            )
        except ClientInputError as exc:
            return JsonResponse({"error": exc.message}, status=exc.status)
        except (ValueError, KeyError, TypeError, UnicodeError, BadZipFile, OSError):
            return JsonResponse(
                {"error": "Unable to read the uploaded schedule or create XML."},
                status=400,
            )
        except Exception:
            logger.exception(
                "Unexpected XML export failure", extra={"user_id": request.user.pk}
            )
            return JsonResponse(
                {"error": "Unable to read the uploaded schedule or create XML."},
                status=400,
            )

        response = HttpResponse(xml_text.encode("utf-8"), content_type="application/xml")
        response["Content-Disposition"] = (
            f'attachment; filename="formatted_courses_{year}.xml"'
        )
        return response


class WordConverterView(WordMatcherPermissionMixin, TemplateView):
    template_name = "planificator/word_converter.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = WordMatchUploadForm()
        return context


class WordMatchPreviewView(WordMatcherPermissionMixin, View):
    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        form = WordMatchUploadForm(request.POST, request.FILES)
        if not form.is_valid():
            return _json_error(
                _form_error(form, "Selectați documentul Word și programul generat."),
                status=getattr(form, "upload_error_status", 400),
            )

        word_file = form.cleaned_data["word_file"]
        schedule_file = form.cleaned_data["schedule_file"]
        try:
            word_file_bytes = word_file.read()
            schedule_rows = read_schedule_rows(
                schedule_file.read(),
                Path(schedule_file.name).suffix.lower(),
            )
            preview = build_word_match_preview(
                word_file_bytes,
                schedule_rows,
                get_settings("word_converter", request.user),
            )
        except ClientInputError as exc:
            return _json_error(exc.message, status=exc.status)
        except (BadZipFile, PackageNotFoundError, OSError, ValueError, KeyError):
            return _json_error("Documentul Word sau programul generat nu a putut fi citit.")
        except Exception:
            logger.exception("Unexpected Word match preview failure", extra={"user_id": request.user.pk})
            return _json_error("Previzualizarea potrivirilor nu a putut fi creată.")

        preview.update(
            {
                "success": True,
                "word_file_b64": base64.b64encode(word_file_bytes).decode("ascii"),
            }
        )
        return JsonResponse(preview)


class WordMatchGenerateView(WordMatcherPermissionMixin, View):
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        try:
            payload = _json_request_data(request)
        except ClientInputError as exc:
            return _json_error(exc.message, status=exc.status)

        form = WordMatchGenerationForm(payload)
        if not form.is_valid():
            return _json_error(
                _form_error(form, "Datele pentru generarea documentului sunt invalide."),
                status=getattr(form, "validation_status", 400),
            )

        try:
            output_bytes, matched_count, skipped_count = apply_word_matches(
                form.cleaned_data["word_file_b64"],
                form.cleaned_data["schedule_options"],
                form.cleaned_data["matches"],
            )
        except ClientInputError as exc:
            return _json_error(exc.message, status=exc.status)
        except (BadZipFile, PackageNotFoundError, OSError, ValueError, KeyError):
            return _json_error("Documentul Word nu a putut fi generat.")
        except Exception:
            logger.exception("Unexpected Word generation failure", extra={"user_id": request.user.pk})
            return _json_error("Documentul Word nu a putut fi generat.")

        response = HttpResponse(
            output_bytes,
            content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
        response["Content-Disposition"] = (
            'attachment; filename="planificare_cursuri_actualizata.docx"'
        )
        response["X-Matched-Course-Rows"] = str(matched_count)
        response["X-Skipped-Course-Rows"] = str(skipped_count)
        return response


class ScheduleHistoryView(PlanificatorPermissionMixin, ListView):
    template_name = "planificator/istoric.html"
    context_object_name = "generations"
    paginate_by = 20

    def get_queryset(self):
        return list_owned_generations(user=self.request.user)


class ScheduleSampleCsvView(PlanificatorPermissionMixin, View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        buffer = StringIO()
        writer = csv.writer(buffer)
        writer.writerow(["Title", "Durata Curs", "investitie", "Permalink"])
        writer.writerow(["Inspector stații ITP", "5 zile", "2500", "https://example.com/curs-itp"])
        response = HttpResponse(buffer.getvalue(), content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = 'attachment; filename="model_cursuri.csv"'
        return response


class ScheduleExportView(PlanificatorPermissionMixin, View):
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        form = ScheduleExportForm(request.POST)
        if not form.is_valid():
            return JsonResponse({"success": False, "error": "Identificator de export invalid."}, status=400)
        generation = get_owned_generation(
            generation_id=form.cleaned_data["generation_id"],
            user=request.user,
        )
        try:
            excel_data = create_excel_export(generation.schedule, generation.year, generation.holidays)
        except Exception:
            logger.exception("Unexpected schedule export failure", extra={"generation_id": str(generation.pk)})
            return JsonResponse({"success": False, "error": "Exportul nu a putut fi creat."}, status=400)
        response = HttpResponse(
            excel_data,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = f'attachment; filename="program_cursuri_{generation.year}.xlsx"'
        return response
```

## `apps/planificator/word_matching.py`

Size: 16.0 KB

```python
import base64
import binascii
import html
import io
import re
from datetime import date, datetime
from typing import Any

from docx import Document
from rapidfuzz import fuzz

from .constants import ROMANIAN_MONTH_NAMES
from .file_handlers import read_tabular_rows
from .validators import (
    MAX_COURSE_ROWS,
    MAX_TABULAR_COLUMNS,
    MAX_WORD_UPLOAD_BYTES,
    ClientInputError,
)


ENGLISH_MONTH_NAMES = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}
MIN_MATCH_SCORE = 88
MIN_TOKEN_COVERAGE = 70
MIN_MATCH_GAP = 8
MAX_TEXT_LENGTH = 1_000
MAX_DATE_LENGTH = 50


def normalize_title(value: str) -> str:
    normalized = html.unescape(str(value or "")).replace("\xa0", " ").strip().lower()
    normalized = normalized.translate(
        str.maketrans(
            {
                "ă": "a",
                "â": "a",
                "î": "i",
                "ș": "s",
                "ş": "s",
                "ț": "t",
                "ţ": "t",
            }
        )
    )
    normalized = re.sub(r"[^\w\s]", " ", normalized)
    return re.sub(r"\s+", " ", normalized).strip()


def _cell_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, datetime):
        return value.strftime("%d.%m.%Y")
    if isinstance(value, date):
        return value.strftime("%d.%m.%Y")
    return str(value).strip()


def read_schedule_rows(file_data: bytes, file_extension: str) -> list[dict[str, Any]]:
    raw_rows = read_tabular_rows(file_data, file_extension.lower())
    if not raw_rows:
        raise ClientInputError("Fișierul de program nu conține un antet.")

    header = [_cell_text(value) for value in raw_rows[0]]
    if len(header) > MAX_TABULAR_COLUMNS:
        raise ClientInputError(f"Fișierul poate avea cel mult {MAX_TABULAR_COLUMNS} coloane.")
    normalized = {name.lower(): index for index, name in enumerate(header) if name}
    if "title" not in normalized:
        raise ClientInputError('Fișierul de program trebuie să conțină coloana "Title".')

    month_indexes: list[int] = []
    for month in range(1, 13):
        aliases = (
            ROMANIAN_MONTH_NAMES[month].lower(),
            ENGLISH_MONTH_NAMES[month].lower(),
        )
        month_index = next((normalized[alias] for alias in aliases if alias in normalized), None)
        if month_index is not None:
            month_indexes.append(month_index)
    if not month_indexes:
        raise ClientInputError(
            "Fișierul de program trebuie să conțină coloane lunare în română sau engleză."
        )

    title_index = normalized["title"]
    schedule_rows: list[dict[str, Any]] = []
    for row_index, raw_row in enumerate(raw_rows[1:]):
        if len(raw_row) > MAX_TABULAR_COLUMNS:
            raise ClientInputError(f"Rândul {row_index + 2} depășește limita de coloane.")
        title = _cell_text(raw_row[title_index]) if title_index < len(raw_row) else ""
        if not title:
            continue
        if len(title) > MAX_TEXT_LENGTH:
            raise ClientInputError(f"Rândul {row_index + 2} conține un titlu prea lung.")
        if len(schedule_rows) >= MAX_COURSE_ROWS:
            raise ClientInputError(
                f"Fișierul poate conține cel mult {MAX_COURSE_ROWS} cursuri.",
                status=413,
            )

        dates: list[str] = []
        for month_index in month_indexes:
            value = _cell_text(raw_row[month_index]) if month_index < len(raw_row) else ""
            if value and value.lower() != "nan":
                if len(value) > MAX_DATE_LENGTH:
                    raise ClientInputError(f"Rândul {row_index + 2} conține o perioadă prea lungă.")
                dates.append(value)
            if len(dates) == 3:
                break
        dates.extend([""] * (3 - len(dates)))
        schedule_rows.append(
            {
                "row_index": row_index,
                "title": title,
                "normalized_title": normalize_title(title),
                "dates": dates,
            }
        )

    if not schedule_rows:
        raise ClientInputError("Fișierul de program nu conține cursuri valide.")
    return schedule_rows


def build_word_course_rows(document: Document) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for table in document.tables:
        for row in table.rows:
            cells = row.cells
            if len(cells) < 6:
                continue
            first_cell = cells[0]
            if first_cell._tc in {cell._tc for cell in cells[1:]}:
                continue
            course_title = first_cell.text.strip()
            if not course_title or sum(1 for cell in cells if cell.text.strip()) <= 1:
                continue
            rows.append(
                {
                    "row": row,
                    "title": course_title,
                    "normalized_title": normalize_title(course_title),
                }
            )
    return rows


def _token_coverage(source: str, target: str) -> float:
    source_tokens = set(source.split())
    target_tokens = set(target.split())
    if not source_tokens:
        return 0
    return len(source_tokens & target_tokens) / len(source_tokens) * 100


def _combined_title_score(word_normalized: str, schedule_normalized: str) -> float:
    return (
        0.35 * fuzz.WRatio(word_normalized, schedule_normalized)
        + 0.25 * fuzz.token_sort_ratio(word_normalized, schedule_normalized)
        + 0.20 * _token_coverage(word_normalized, schedule_normalized)
        + 0.20 * _token_coverage(schedule_normalized, word_normalized)
    )


def _standard_code_tokens(value: str) -> set[str]:
    return set(re.findall(r"\b\d{4,5}\b", value))


def score_schedule_matches(
    word_title: str,
    schedule_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    word_normalized = normalize_title(word_title)
    if not word_normalized or not schedule_rows:
        return []
    exact_matches = [
        entry for entry in schedule_rows if entry["normalized_title"] == word_normalized
    ]
    if len(exact_matches) == 1:
        return [
            {
                "entry": exact_matches[0],
                "score": 100,
                "word_coverage": 100,
                "schedule_coverage": 100,
                "exact": True,
            }
        ]

    scored_matches = []
    for entry in schedule_rows:
        schedule_normalized = entry["normalized_title"]
        scored_matches.append(
            {
                "entry": entry,
                "score": _combined_title_score(word_normalized, schedule_normalized),
                "word_coverage": _token_coverage(word_normalized, schedule_normalized),
                "schedule_coverage": _token_coverage(schedule_normalized, word_normalized),
                "exact": False,
            }
        )
    scored_matches.sort(key=lambda item: item["score"], reverse=True)
    return scored_matches


def confident_match_from_scores(
    word_title: str,
    scored_matches: list[dict[str, Any]],
    match_settings: dict[str, float] | None = None,
) -> dict[str, Any] | None:
    if not scored_matches:
        return None
    if scored_matches[0].get("exact"):
        return scored_matches[0]["entry"]

    match_settings = match_settings or {
        "min_match_score": MIN_MATCH_SCORE,
        "min_token_coverage": MIN_TOKEN_COVERAGE,
        "min_match_gap": MIN_MATCH_GAP,
    }
    word_normalized = normalize_title(word_title)
    best = scored_matches[0]
    second = scored_matches[1] if len(scored_matches) > 1 else None
    below_threshold = (
        best["score"] < float(match_settings["min_match_score"])
        or best["word_coverage"] < float(match_settings["min_token_coverage"])
        or best["schedule_coverage"] < float(match_settings["min_token_coverage"])
    )
    if below_threshold:
        word_codes = _standard_code_tokens(word_normalized)
        best_codes = _standard_code_tokens(best["entry"]["normalized_title"])
        second_codes = (
            _standard_code_tokens(second["entry"]["normalized_title"]) if second else set()
        )
        code_match = (
            word_codes
            and word_codes.issubset(best_codes)
            and not word_codes.issubset(second_codes)
            and best["score"] >= 70
            and best["word_coverage"] >= 60
        )
        if not code_match:
            return None

    if second and best["score"] - second["score"] < float(match_settings["min_match_gap"]):
        word_codes = _standard_code_tokens(word_normalized)
        best_codes = _standard_code_tokens(best["entry"]["normalized_title"])
        second_codes = _standard_code_tokens(second["entry"]["normalized_title"])
        code_match = (
            word_codes
            and word_codes.issubset(best_codes)
            and not word_codes.issubset(second_codes)
            and best["word_coverage"] >= 60
        )
        if not code_match:
            return None
    return best["entry"]


def _candidate_payload(scored_match: dict[str, Any]) -> dict[str, Any]:
    entry = scored_match["entry"]
    return {
        "row_index": entry["row_index"],
        "title": entry["title"],
        "dates": entry["dates"],
        "score": round(scored_match["score"], 1),
        "word_coverage": round(scored_match["word_coverage"], 1),
        "schedule_coverage": round(scored_match["schedule_coverage"], 1),
        "exact": bool(scored_match.get("exact")),
    }


def build_word_match_preview(
    word_file_bytes: bytes,
    schedule_rows: list[dict[str, Any]],
    match_settings: dict[str, Any],
) -> dict[str, Any]:
    document = Document(io.BytesIO(word_file_bytes))
    word_rows = build_word_course_rows(document)
    if not word_rows:
        raise ClientInputError(
            "Documentul Word nu conține rânduri de curs compatibile cu structura așteptată."
        )

    clean_settings = {
        "min_match_score": float(match_settings.get("min_match_score", MIN_MATCH_SCORE)),
        "min_token_coverage": float(
            match_settings.get("min_token_coverage", MIN_TOKEN_COVERAGE)
        ),
        "min_match_gap": float(match_settings.get("min_match_gap", MIN_MATCH_GAP)),
    }
    rows = []
    matched_count = 0
    for word_index, word_row in enumerate(word_rows):
        scored_matches = score_schedule_matches(word_row["title"], schedule_rows)
        confident_match = confident_match_from_scores(
            word_row["title"], scored_matches, clean_settings
        )
        selected_row_index = confident_match["row_index"] if confident_match else None
        matched_count += int(confident_match is not None)
        rows.append(
            {
                "word_row_index": word_index,
                "word_title": word_row["title"],
                "selected_row_index": selected_row_index,
                "status": "matched" if confident_match else "needs_review",
                "candidates": [_candidate_payload(match) for match in scored_matches[:5]],
            }
        )
    return {
        "rows": rows,
        "schedule_options": [
            {
                "row_index": row["row_index"],
                "title": row["title"],
                "dates": row["dates"],
            }
            for row in schedule_rows
        ],
        "matched_count": matched_count,
        "skipped_count": len(rows) - matched_count,
    }


def decode_word_base64(value: Any) -> bytes:
    if not isinstance(value, str) or not value:
        raise ClientInputError("Datele documentului Word lipsesc. Refaceți previzualizarea.")
    if len(value) > (MAX_WORD_UPLOAD_BYTES * 4 // 3) + 8:
        raise ClientInputError("Datele documentului Word depășesc limita permisă.", status=413)
    try:
        decoded = base64.b64decode(value, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise ClientInputError("Datele documentului Word sunt invalide.") from exc
    if not decoded or len(decoded) > MAX_WORD_UPLOAD_BYTES:
        raise ClientInputError("Datele documentului Word au o dimensiune invalidă.", status=413)
    return decoded


def validate_schedule_options(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        raise ClientInputError("Opțiunile programului trebuie trimise ca listă.")
    if not value or len(value) > MAX_COURSE_ROWS:
        raise ClientInputError("Numărul opțiunilor programului este invalid.")

    rows = []
    seen_indexes: set[int] = set()
    for item in value:
        if not isinstance(item, dict) or set(item) != {"row_index", "title", "dates"}:
            raise ClientInputError("O opțiune din program are o structură invalidă.")
        row_index = item["row_index"]
        if isinstance(row_index, bool) or not isinstance(row_index, int) or row_index < 0:
            raise ClientInputError("Un index din program este invalid.")
        if row_index in seen_indexes:
            raise ClientInputError("Programul conține indexuri duplicate.")
        seen_indexes.add(row_index)

        title = item["title"]
        dates = item["dates"]
        if not isinstance(title, str) or not title.strip() or len(title.strip()) > MAX_TEXT_LENGTH:
            raise ClientInputError("Un titlu din program este invalid.")
        if not isinstance(dates, list) or len(dates) != 3:
            raise ClientInputError("Fiecare curs trebuie să conțină exact trei perioade.")
        clean_dates = []
        for date_value in dates:
            if not isinstance(date_value, str) or len(date_value.strip()) > MAX_DATE_LENGTH:
                raise ClientInputError("O perioadă din program este invalidă.")
            clean_dates.append(date_value.strip())
        rows.append(
            {
                "row_index": row_index,
                "title": title.strip(),
                "normalized_title": normalize_title(title),
                "dates": clean_dates,
            }
        )
    return rows


def validate_matches(value: Any) -> dict[int, int]:
    if not isinstance(value, list) or len(value) > MAX_COURSE_ROWS:
        raise ClientInputError("Selecțiile trebuie trimise ca listă.")
    matches: dict[int, int] = {}
    for item in value:
        if not isinstance(item, dict) or set(item) != {
            "word_row_index",
            "schedule_row_index",
        }:
            raise ClientInputError("O selecție are o structură invalidă.")
        word_index = item["word_row_index"]
        schedule_index = item["schedule_row_index"]
        if (
            isinstance(word_index, bool)
            or not isinstance(word_index, int)
            or word_index < 0
            or isinstance(schedule_index, bool)
            or not isinstance(schedule_index, int)
            or schedule_index < 0
        ):
            raise ClientInputError("O selecție conține un index invalid.")
        if word_index in matches:
            raise ClientInputError("Selecțiile conțin rânduri Word duplicate.")
        matches[word_index] = schedule_index
    return matches


def apply_word_matches(
    word_file_bytes: bytes,
    schedule_rows: list[dict[str, Any]],
    matches: dict[int, int],
) -> tuple[bytes, int, int]:
    document = Document(io.BytesIO(word_file_bytes))
    word_rows = build_word_course_rows(document)
    schedule_by_index = {row["row_index"]: row for row in schedule_rows}
    if any(index >= len(word_rows) for index in matches):
        raise ClientInputError("O selecție indică un rând Word inexistent.")
    if any(index not in schedule_by_index for index in matches.values()):
        raise ClientInputError("O selecție indică un rând de program inexistent.")

    matched_count = 0
    for word_index, word_row in enumerate(word_rows):
        selected_schedule = schedule_by_index.get(matches.get(word_index))
        if not selected_schedule:
            continue
        for target_index, date_value in zip((3, 4, 5), selected_schedule["dates"]):
            word_row["row"].cells[target_index].text = date_value
        matched_count += 1

    output = io.BytesIO()
    document.save(output)
    return output.getvalue(), matched_count, len(word_rows) - matched_count
```

## `apps/planificator/wp_course_updater.py`

Size: 16.5 KB

Redacted secret-like assignments: 2

```python
from __future__ import annotations

from datetime import date, datetime
import random
import re
import time
from typing import Any
from urllib.parse import urljoin, urlparse

import requests
from requests.auth import HTTPBasicAuth

from .validators import validate_http_url_syntax, validate_public_http_url


MONTH_COLUMNS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]
ROMANIAN_MONTH_COLUMNS = [
    "Ianuarie",
    "Februarie",
    "Martie",
    "Aprilie",
    "Mai",
    "Iunie",
    "Iulie",
    "August",
    "Septembrie",
    "Octombrie",
    "Noiembrie",
    "Decembrie",
]
MAX_RESPONSE_BYTES = 5 * 1024 * 1024
MAX_REDIRECTS = 3


class WordPressRequestError(RuntimeError):
    """A client-safe WordPress integration failure."""


class WPCourseClient:
    def __init__(self, base_url: str, username: str, app_password: str):
        raw_base_url = (base_url or "").strip().rstrip("/")
        self.base_url = validate_http_url_syntax(raw_base_url) if raw_base_url else ""

        clean_username = (username or "").strip()
        clean_password = (app_password or "").strip().replace(" ", "")
        self.auth = HTTPBasicAuth(clean_username, clean_password)
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "insomnia/11.0.2",
                "Accept": "*/*",
                "Content-Type": "application/json",
                "Origin": self.base_url,
                "Referer": f"{self.base_url}/",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
            }
        )
        self.timeout = (5, 30)
        self.min_interval_seconds = 0.85
        self.max_retries = 4
        self.base_backoff_seconds = 1.25
        self.last_request_ts = 0.0

    def _endpoint(self, path: str) -> str:
        normalized = path if path.startswith("/") else f"/{path}"
        return f"{self.base_url}{normalized}"

    def _rest_candidate_paths(self, path: str) -> list[str]:
        normalized = path if path.startswith("/") else f"/{path}"
        return [normalized]

    def _sleep_for_spacing(self) -> None:
        elapsed = time.monotonic() - self.last_request_ts
        if elapsed < self.min_interval_seconds:
            time.sleep(self.min_interval_seconds - elapsed)

    def _mark_request_complete(self) -> None:
        self.last_request_ts = time.monotonic()

    @staticmethod
    def _is_cloudflare_challenge(response: requests.Response) -> bool:
        return (
            response.headers.get("cf-mitigated", "").lower() == "challenge"
            or "just a moment" in (response.text or "").lower()
        )

    @staticmethod
    def _retry_after_seconds(response: requests.Response) -> float | None:
        value = (response.headers.get("Retry-After") or "").strip()
        if not value:
            return None
        try:
            return max(0.0, float(value))
        except ValueError:
            return None

    def _compute_backoff(
        self,
        attempt_index: int,
        response: requests.Response | None = None,
    ) -> float:
        retry_after = self._retry_after_seconds(response) if response is not None else None
        if retry_after is not None:
            return retry_after + random.uniform(0.1, 0.4)
        delay = min(self.base_backoff_seconds * (2**attempt_index), 12.0)
        return delay + random.uniform(0.1, 0.5)

    @staticmethod
    def _raise_for_response(response: requests.Response) -> None:
        if response.ok:
            return
        if WPCourseClient._is_cloudflare_challenge(response):
            raise WordPressRequestError("WordPress rejected the request with a browser challenge.")
        if response.status_code == 401:
            raise WordPressRequestError("WordPress authentication failed.")
        if response.status_code == 403:
            raise WordPressRequestError("WordPress denied this operation.")
        if response.status_code == 404:
            raise WordPressRequestError("The required WordPress endpoint was not found.")
        if response.status_code == 429:
            raise WordPressRequestError("WordPress is temporarily rate limiting requests.")
        if response.status_code >= 500:
            raise WordPressRequestError("WordPress is temporarily unavailable.")
        raise WordPressRequestError("WordPress rejected the request.")

    @staticmethod
    def _read_bounded_response(response: requests.Response) -> requests.Response:
        content_length = response.headers.get("Content-Length")
        if content_length:
            try:
                if int(content_length) > MAX_RESPONSE_BYTES:
                    response.close()
                    raise WordPressRequestError("WordPress returned a response that is too large.")
            except ValueError:
                pass
        chunks: list[bytes] = []
        total = 0
        for chunk in response.iter_content(chunk_size=64 * 1024):
            if not chunk:
                continue
            total += len(chunk)
            if total > MAX_RESPONSE_BYTES:
                response.close()
                raise WordPressRequestError("WordPress returned a response that is too large.")
            chunks.append(chunk)
        response._content = b"".join(chunks)
        response._content_consumed = True
        return response

    def _send_with_safe_redirects(
        self,
        method: str,
        url: str,
        *,
        auth=None,
        **kwargs,
    ) -> requests.Response:
        current_method = method.upper()
        current_url = url
        current_kwargs = dict(kwargs)

        for redirect_index in range(MAX_REDIRECTS + 1):
            current_url = validate_public_http_url(current_url)
            self._sleep_for_spacing()
            try:
                response = self.session.request(
                    method=current_method,
                    url=current_url,
                    auth=auth,
                    timeout=self.timeout,
                    allow_redirects=False,
                    stream=True,
                    **current_kwargs,
                )
            except (requests.Timeout, requests.ConnectionError) as exc:
                self._mark_request_complete()
                raise WordPressRequestError("Unable to reach WordPress.") from exc
            except requests.RequestException as exc:
                self._mark_request_complete()
                raise WordPressRequestError("WordPress request failed.") from exc
            self._mark_request_complete()
            response = self._read_bounded_response(response)

            if response.status_code not in {301, 302, 303, 307, 308}:
                return response
            location = response.headers.get("Location", "").strip()
            if not location:
                raise WordPressRequestError("WordPress returned an invalid redirect.")
            if redirect_index >= MAX_REDIRECTS:
                raise WordPressRequestError("WordPress returned too many redirects.")
            current_url = urljoin(current_url, location)
            validate_public_http_url(current_url)
            if response.status_code == 303 or (
                response.status_code in {301, 302} and current_method == "POST"
            ):
                current_method = "GET"
                current_kwargs.pop("json", None)
                current_kwargs.pop("data", None)
                current_kwargs.pop("files", None)
        raise WordPressRequestError("WordPress returned too many redirects.")

    def _request_with_retries(
        self,
        method: str,
        path: str,
        *,
        auth=None,
        retry_on_401_without_auth: bool = False,
        **kwargs,
    ) -> requests.Response:
        last_response: requests.Response | None = None
        for candidate_path in self._rest_candidate_paths(path):
            url = self._endpoint(candidate_path)
            for attempt in range(self.max_retries + 1):
                response = self._send_with_safe_redirects(method, url, auth=auth, **kwargs)
                if response.ok:
                    return response
                last_response = response
                if response.status_code == 401 and retry_on_401_without_auth and auth is not None:
                    fallback = self._send_with_safe_redirects(method, url, auth=None, **kwargs)
                    if fallback.ok:
                        return fallback
                    last_response = fallback
                if response.status_code in (403, 429, 500, 502, 503, 504) and attempt < self.max_retries:
                    time.sleep(self._compute_backoff(attempt, response))
                    continue
                break
        if last_response is not None:
            self._raise_for_response(last_response)
        raise WordPressRequestError("Unable to call the WordPress endpoint.")

    def _get_with_optional_auth(
        self,
        path: str,
        prefer_auth: bool = True,
        **kwargs,
    ) -> requests.Response:
        if prefer_auth:
            return self._request_with_retries(
                "GET",
                path,
                auth=self.auth,
                retry_on_401_without_auth=True,
                **kwargs,
            )
        return self._request_with_retries(
            "GET",
            path,
            auth=None,
            retry_on_401_without_auth=False,
            **kwargs,
        )

    @staticmethod
    def _response_json(response: requests.Response) -> Any:
        try:
            return response.json()
        except (requests.exceptions.JSONDecodeError, ValueError) as exc:
            raise WordPressRequestError("WordPress returned an invalid response.") from exc

    def get_course_by_slug(self, slug: str) -> dict[str, Any] | None:
        slug = str(slug or "").strip()
        if not slug:
            return None
        response = self._get_with_optional_auth(
            "/wp-json/wp/v2/cursuri",
            prefer_auth=True,
            params={"slug": slug},
        )
        data = self._response_json(response)
        if not isinstance(data, list):
            return None
        for item in data:
            if str((item or {}).get("slug", "")).strip() == slug:
                return item
        return None

    def test_connection(self) -> dict[str, Any]:
        response = self._request_with_retries(
            "GET",
            "/wp-json/wp/v2/users/me",
            auth=self.auth,
            retry_on_401_without_auth=False,
        )
        data = self._response_json(response)
        return data if isinstance(data, dict) else {}

    def resolve_course_post_id(
        self,
        slug: str | None = None,
        permalink: str | None = None,
        fallback_post_id: int | None = None,
    ) -> int | None:
        clean_slug = str(slug or "").strip()
        if not clean_slug and permalink:
            clean_slug = extract_slug_from_permalink(permalink)
        if not clean_slug:
            return None
        course = self.get_course_by_slug(clean_slug)
        if not course or course.get("id") is None:
            return None
        try:
            return int(course["id"])
        except (TypeError, ValueError):
            return None

    def get_course(self, post_id: int) -> dict[str, Any]:
        response = self._get_with_optional_auth(
            f"/wp-json/wp/v2/cursuri/{int(post_id)}",
            prefer_auth=True,
        )
        data = self._response_json(response)
        if not isinstance(data, dict):
            raise WordPressRequestError("WordPress returned an invalid response.")
        return data

    def update_course_program(
        self,
        post_id: int,
        final_program: list[dict],
        auth=None,
    ) -> dict[str, Any]:
        payload = {"acf": {"program": final_program if final_program else False}}
        response = self._request_with_retries(
            "POST",
            f"/wp-json/wp/v2/cursuri/{int(post_id)}",
            auth=auth or self.auth,
            retry_on_401_without_auth=False,
            json=payload,
        )
        data = self._response_json(response)
        if not isinstance(data, dict):
            raise WordPressRequestError("WordPress returned an invalid response.")
        return data


def extract_slug_from_permalink(url: str) -> str:
    parsed = urlparse((url or "").strip())
    parts = [part for part in (parsed.path or "").strip("/ ").split("/") if part]
    return parts[-1] if parts else ""


def parse_single_ro_date(value: str) -> date:
    return datetime.strptime(value.strip(), "%d.%m.%Y").date()


def parse_effective_end_date(text: str) -> date | None:
    text = str(text or "").strip()
    if not text:
        return None
    single = re.fullmatch(r"(\d{1,2})\.(\d{1,2})\.(\d{4})", text)
    if single:
        day, month, year = map(int, single.groups())
        try:
            return date(year, month, day)
        except ValueError:
            return None
    date_range = re.fullmatch(r"(\d{1,2})-(\d{1,2})\.(\d{1,2})\.(\d{4})", text)
    if date_range:
        _start_day, end_day, month, year = map(int, date_range.groups())
        try:
            return date(year, month, end_day)
        except ValueError:
            return None
    return None


def _normalize_excel_date_value(value: Any) -> str:
    if value is None:
        return ""
    if hasattr(value, "to_pydatetime"):
        value = value.to_pydatetime()
    if isinstance(value, datetime):
        return value.strftime("%d.%m.%Y")
    if isinstance(value, date):
        return value.strftime("%d.%m.%Y")
    return str(value).strip()


def expand_date_token(token: str) -> list[str]:
    token = <redacted>
    if not token or token.lower() == "nan":
        return []
    token = <redacted>
    if re.fullmatch(r"\d{1,2}\.\d{1,2}\.\d{4}", token):
        parsed = datetime.strptime(token, "%d.%m.%Y")
        return [parsed.strftime("%d.%m.%Y")]
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}(?:\s+\d{2}:\d{2}:\d{2})?", token):
        parsed = datetime.strptime(token[:10], "%Y-%m-%d")
        return [parsed.strftime("%d.%m.%Y")]
    match = re.fullmatch(r"(\d{1,2})-(\d{1,2})\.(\d{1,2})\.(\d{4})", token)
    if not match:
        return []
    start_day, end_day, month, year = map(int, match.groups())
    if end_day < start_day:
        return []
    out: list[str] = []
    for day in range(start_day, end_day + 1):
        normalized = f"{day:02d}.{month:02d}.{year}"
        try:
            parse_single_ro_date(normalized)
        except ValueError:
            return []
        out.append(normalized)
    return out


def split_cell_tokens(value: Any) -> list[str]:
    text = _normalize_excel_date_value(value)
    if not text or text.lower() == "nan":
        return []
    return [text]


def parse_excel_dates_from_row(row: dict) -> list[str]:
    dates: list[str] = []
    lowered_row = {str(key).strip().lower(): value for key, value in (row or {}).items()}
    for english_column, romanian_column in zip(MONTH_COLUMNS, ROMANIAN_MONTH_COLUMNS):
        raw_value = lowered_row.get(english_column.lower())
        if raw_value in (None, ""):
            raw_value = lowered_row.get(romanian_column.lower())
        for token in split_cell_tokens(raw_value):
            normalized = str(token).strip()
            if normalized:
                dates.append(normalized)
    return dates


def _filter_existing_non_expired_rows(
    program: list[dict],
    today: date,
) -> list[dict[str, str]]:
    normalized: list[dict[str, str]] = []
    seen: set[str] = set()
    for row in program or []:
        raw = str((row or {}).get("data", "")).strip()
        if not raw:
            continue
        end_date = parse_effective_end_date(raw)
        if end_date is not None and end_date >= today and raw not in seen:
            normalized.append({"data": raw})
            seen.add(raw)
    return normalized


def build_final_program(
    existing_program: list,
    excel_dates: list[str],
    today: date,
) -> list[dict]:
    seen: set[str] = set()
    result: list[dict[str, str]] = []
    for row in _filter_existing_non_expired_rows(existing_program, today):
        raw = row["data"]
        if raw not in seen:
            result.append({"data": raw})
            seen.add(raw)
    for raw in excel_dates:
        normalized = str(raw).strip()
        if normalized and normalized not in seen:
            result.append({"data": normalized})
            seen.add(normalized)
    return result


def valid_existing_program(existing_program: list, today: date) -> list[dict[str, str]]:
    return _filter_existing_non_expired_rows(existing_program, today)
```

## `apps/planificator/xml_export.py`

Size: 9.1 KB

```python
import calendar
from datetime import datetime
import re
from typing import Any
import xml.etree.ElementTree as ET
from xml.dom import minidom

from .constants import ROMANIAN_MONTH_NAMES
from .file_handlers import read_tabular_rows
from .validators import ClientInputError, MAX_COURSE_ROWS, MAX_TABULAR_COLUMNS


def parse_xml_date_range(date_range: str) -> tuple[str, str]:
    normalized = (date_range or "").strip()

    single_day = re.match(r"^(\d{1,2})\.(\d{1,2})\.(\d{4})$", normalized)
    if single_day:
        day, month, parsed_year = single_day.groups()
        iso_date = f"{parsed_year}-{month.zfill(2)}-{day.zfill(2)}"
        return iso_date, iso_date

    multi_day_same_month = re.match(
        r"^(\d{1,2})\s*-\s*(\d{1,2})\.(\d{1,2})\.(\d{4})$",
        normalized,
    )
    if multi_day_same_month:
        start_day, end_day, month, parsed_year = multi_day_same_month.groups()
        return (
            f"{parsed_year}-{month.zfill(2)}-{start_day.zfill(2)}",
            f"{parsed_year}-{month.zfill(2)}-{end_day.zfill(2)}",
        )

    multi_day_with_month = re.match(
        r"^(\d{1,2})\.(\d{1,2})\s*-\s*(\d{1,2})\.(\d{1,2})\.(\d{4})$",
        normalized,
    )
    if multi_day_with_month:
        start_day, start_month, end_day, end_month, parsed_year = (
            multi_day_with_month.groups()
        )
        return (
            f"{parsed_year}-{start_month.zfill(2)}-{start_day.zfill(2)}",
            f"{parsed_year}-{end_month.zfill(2)}-{end_day.zfill(2)}",
        )

    raise ValueError(f"Unsupported date format: {date_range}")


def create_xml_export(
    schedule: list[dict[str, Any]],
    year: int,
    *,
    start_post_id: int = 20000,
) -> str:
    # ``year`` remains part of the legacy contract and download workflow even
    # though each event date already carries its own year.
    del year

    root = ET.Element("events")
    courses: dict[str, list[dict[str, Any]]] = {}
    for event in schedule:
        courses.setdefault(event["course_name"], []).append(event)

    event_id = int(start_post_id or 20000) - 1

    for course_name, course_events in courses.items():
        for period_idx, event in enumerate(course_events, start=1):
            event_id += 1
            start_date, end_date = parse_xml_date_range(str(event["date_range"]).strip())
            start_day_seconds = 8 * 3600
            end_day_seconds = 18 * 3600
            start_datetime = f"{start_date} 08:00 AM"
            end_datetime = f"{end_date} 06:00 PM"

            item = ET.SubElement(root, "item")
            ET.SubElement(item, "ID").text = str(event_id)
            ET.SubElement(item, "title").text = course_name
            ET.SubElement(item, "content").text = ""

            post = ET.SubElement(item, "post")
            ET.SubElement(post, "ID").text = str(event_id)
            ET.SubElement(post, "post_author").text = "5"
            ET.SubElement(post, "post_date").text = f"{start_date} 00:00:00"
            ET.SubElement(post, "post_date_gmt").text = f"{start_date} 00:00:00"
            ET.SubElement(post, "post_title").text = course_name
            ET.SubElement(post, "post_status").text = "draft"

            meta = ET.SubElement(item, "meta")
            ET.SubElement(meta, "mec_more_info_title").text = f"perioada {period_idx}"
            ET.SubElement(meta, "mec_read_more").text = event.get("permalink", "")
            ET.SubElement(meta, "mec_color").text = ""
            ET.SubElement(meta, "mec_location_id").text = "1"
            ET.SubElement(meta, "mec_organizer_id").text = "1"
            ET.SubElement(meta, "mec_allday").text = "1"
            ET.SubElement(meta, "mec_start_date").text = start_date
            ET.SubElement(meta, "mec_start_time_hour").text = "8"
            ET.SubElement(meta, "mec_start_time_minutes").text = "00"
            ET.SubElement(meta, "mec_start_time_ampm").text = "AM"
            ET.SubElement(meta, "mec_start_day_seconds").text = str(start_day_seconds)
            ET.SubElement(meta, "mec_start_datetime").text = start_datetime
            ET.SubElement(meta, "mec_end_date").text = end_date
            ET.SubElement(meta, "mec_end_time_hour").text = "6"
            ET.SubElement(meta, "mec_end_time_minutes").text = "00"
            ET.SubElement(meta, "mec_end_time_ampm").text = "PM"
            ET.SubElement(meta, "mec_end_day_seconds").text = str(end_day_seconds)
            ET.SubElement(meta, "mec_end_datetime").text = end_datetime
            ET.SubElement(meta, "mec_repeat_status").text = "0"

            mec_date = ET.SubElement(meta, "mec_date")
            start = ET.SubElement(mec_date, "start")
            ET.SubElement(start, "date").text = start_date
            ET.SubElement(start, "hour").text = "8"
            ET.SubElement(start, "minutes").text = "00"
            ET.SubElement(start, "ampm").text = "AM"
            end = ET.SubElement(mec_date, "end")
            ET.SubElement(end, "date").text = end_date
            ET.SubElement(end, "hour").text = "6"
            ET.SubElement(end, "minutes").text = "00"
            ET.SubElement(end, "ampm").text = "PM"
            ET.SubElement(mec_date, "allday").text = "1"

            mec_block = ET.SubElement(item, "mec")
            ET.SubElement(mec_block, "id").text = ""
            ET.SubElement(mec_block, "post_id").text = str(event_id)
            ET.SubElement(mec_block, "start").text = start_date
            ET.SubElement(mec_block, "end").text = end_date
            ET.SubElement(mec_block, "repeat").text = "0"
            ET.SubElement(mec_block, "time_start").text = str(start_day_seconds)
            ET.SubElement(mec_block, "time_end").text = str(end_day_seconds)

            time = ET.SubElement(item, "time")
            ET.SubElement(time, "start").text = "All Day"
            ET.SubElement(time, "end").text = ""
            ET.SubElement(time, "start_raw").text = "8:00 am"
            ET.SubElement(time, "end_raw").text = "6:00 pm"
            ET.SubElement(time, "start_timestamp").text = str(
                int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
                + start_day_seconds
            )
            ET.SubElement(time, "end_timestamp").text = str(
                int(datetime.strptime(end_date, "%Y-%m-%d").timestamp())
                + end_day_seconds
            )

    return minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")


def _cell_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def read_xml_schedule(file_data: bytes, file_extension: str) -> list[dict[str, str]]:
    raw_rows = read_tabular_rows(file_data, file_extension.lower())
    if not raw_rows:
        raise ClientInputError("Missing required columns: Title, Permalink")

    header = [_cell_text(value) for value in raw_rows[0]]
    if len(header) > MAX_TABULAR_COLUMNS:
        raise ClientInputError(
            f"The input file may contain at most {MAX_TABULAR_COLUMNS} columns."
        )
    normalized_columns = {
        column.strip().lower(): index for index, column in enumerate(header)
    }
    missing_columns = [
        canonical
        for source, canonical in {"title": "Title", "permalink": "Permalink"}.items()
        if source not in normalized_columns
    ]
    if missing_columns:
        raise ClientInputError(
            f"Missing required columns: {', '.join(missing_columns)}"
        )

    month_aliases = (
        {calendar.month_name[index].lower() for index in range(1, 13)}
        | {f"luna {index}" for index in range(1, 13)}
        | {name.lower() for name in ROMANIAN_MONTH_NAMES.values()}
    )
    month_columns = [
        index
        for normalized, index in normalized_columns.items()
        if normalized in month_aliases
    ]
    if not month_columns:
        raise ClientInputError(
            "No supported date columns found. Use Romanian or English month columns, "
            "or Luna columns (Luna 1-Luna 12)."
        )

    title_index = normalized_columns["title"]
    permalink_index = normalized_columns["permalink"]
    schedule: list[dict[str, str]] = []
    course_rows = 0

    for raw_row in raw_rows[1:]:
        title = _cell_text(raw_row[title_index]) if title_index < len(raw_row) else ""
        permalink = (
            _cell_text(raw_row[permalink_index])
            if permalink_index < len(raw_row)
            else ""
        )
        if not title:
            continue
        course_rows += 1
        if course_rows > MAX_COURSE_ROWS:
            raise ClientInputError(
                f"The input file may contain at most {MAX_COURSE_ROWS} courses.",
                status=413,
            )
        for month_index in month_columns:
            date_value = (
                _cell_text(raw_row[month_index]) if month_index < len(raw_row) else ""
            )
            if date_value and date_value.lower() != "nan":
                schedule.append(
                    {
                        "course_name": title,
                        "date_range": date_value,
                        "permalink": permalink,
                    }
                )

    if not schedule:
        raise ClientInputError("No valid course data found in the input file")
    return schedule
```

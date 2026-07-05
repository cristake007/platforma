# apps/planificator/file_handlers.py

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `apps/planificator/file_handlers.py`
- App: `planificator`
- App guide: `codex-context/apps/planificator.md`
- Role: `backend`
- Size: 7527 bytes
- Source SHA-256: `0506266523ea7539f49edbd6bed8c71f2004d68e4a6ff504c0bf0ece2fb22d1e`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

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

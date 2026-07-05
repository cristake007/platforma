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

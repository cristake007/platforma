# apps/diplome/pdf_renderer.py

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `apps/diplome/pdf_renderer.py`
- App: `diplome`
- App guide: `codex-context/apps/diplome.md`
- Role: `backend`
- Size: 18531 bytes
- Source SHA-256: `df8960da6f02e09d098709efd0d5755009d5532ee96174f4f64a709e2520806b`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from __future__ import annotations

from io import BytesIO
from pathlib import Path

from django.conf import settings
from reportlab.graphics import renderPDF
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as pdf_canvas
from svglib.svglib import svg2rlg

from apps.media_library.services import require_owned_layout_assets

from .validators import validate_layout_json


CSS_PX_TO_PT = 72 / 96
FONT_NAMES = {
    "sans": {
        (False, False): "DiplomaSans",
        (True, False): "DiplomaSans-Bold",
        (False, True): "DiplomaSans-Italic",
        (True, True): "DiplomaSans-BoldItalic",
    },
    "serif": {
        (False, False): "DiplomaSerif",
        (True, False): "DiplomaSerif-Bold",
        (False, True): "DiplomaSerif-Italic",
        (True, True): "DiplomaSerif-BoldItalic",
    },
}
FALLBACK_FONT_NAMES = {
    "sans": {
        (False, False): "Helvetica",
        (True, False): "Helvetica-Bold",
        (False, True): "Helvetica-Oblique",
        (True, True): "Helvetica-BoldOblique",
    },
    "serif": {
        (False, False): "Times-Roman",
        (True, False): "Times-Bold",
        (False, True): "Times-Italic",
        (True, True): "Times-BoldItalic",
    },
}
FONT_FILES = {
    "sans": {
        (False, False): "arial.ttf",
        (True, False): "arialbd.ttf",
        (False, True): "ariali.ttf",
        (True, True): "arialbi.ttf",
    },
    "serif": {
        (False, False): "times.ttf",
        (True, False): "timesbd.ttf",
        (False, True): "timesi.ttf",
        (True, True): "timesbi.ttf",
    },
}
LIBERATION_FONT_FILES = {
    "sans": {
        (False, False): "LiberationSans-Regular.ttf",
        (True, False): "LiberationSans-Bold.ttf",
        (False, True): "LiberationSans-Italic.ttf",
        (True, True): "LiberationSans-BoldItalic.ttf",
    },
    "serif": {
        (False, False): "LiberationSerif-Regular.ttf",
        (True, False): "LiberationSerif-Bold.ttf",
        (False, True): "LiberationSerif-Italic.ttf",
        (True, True): "LiberationSerif-BoldItalic.ttf",
    },
}
_fonts_registered = False


def _register_local_fonts() -> bool:
    global _fonts_registered
    if _fonts_registered:
        return True

    font_sources = (
        (Path("C:/Windows/Fonts"), FONT_FILES),
        (
            Path(settings.BASE_DIR) / "theme" / "static" / "fonts" / "pdf",
            FONT_FILES,
        ),
        (
            Path("/usr/share/fonts/truetype/liberation2"),
            LIBERATION_FONT_FILES,
        ),
    )
    for root, font_files in font_sources:
        if not all(
            (root / filename).is_file()
            for family_files in font_files.values()
            for filename in family_files.values()
        ):
            continue
        for family, variants in font_files.items():
            for variant, filename in variants.items():
                pdfmetrics.registerFont(
                    TTFont(FONT_NAMES[family][variant], root / filename)
                )
        _fonts_registered = True
        return True
    return False


def _font_name(family: str, *, bold: bool, italic: bool = False) -> str:
    family_group = "serif" if family in {"Lora", "Georgia", "Times New Roman"} else "sans"
    names = FONT_NAMES if _register_local_fonts() else FALLBACK_FONT_NAMES
    return names[family_group][(bold, italic)]


def _participant_data(participant) -> dict[str, str]:
    return {
        "full_name": participant.full_name,
        "date_of_birth": participant.date_of_birth.strftime("%d.%m.%Y"),
        "place_of_birth": participant.place_of_birth,
        "certificate_number": participant.certificate_number,
    }


def _text_width(text: str, font_name: str, font_size: float, char_space: float = 0) -> float:
    return max(
        0,
        pdfmetrics.stringWidth(text, font_name, font_size)
        + max(0, len(text) - 1) * char_space,
    )


def _wrap_text(
    text: str,
    font_name: str,
    font_size: float,
    max_width: float,
    char_space: float = 0,
) -> list[str]:
    lines = []
    for paragraph in text.splitlines() or [""]:
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            candidate = f"{current} {word}"
            if _text_width(candidate, font_name, font_size, char_space) <= max_width:
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def _aligned_x(x: float, width: float, text_width: float, align: str) -> float:
    if align == "center":
        return x + (width - text_width) / 2
    if align == "right":
        return x + width - text_width
    return x


def _transform_text(text: str, transform: str) -> str:
    if transform == "uppercase":
        return text.upper()
    if transform == "lowercase":
        return text.lower()
    return text


def _draw_tracked_line(
    pdf,
    *,
    text: str,
    x: float,
    baseline: float,
    font_name: str,
    font_size: float,
    char_space: float,
) -> None:
    text_object = pdf.beginText()
    text_object.setTextOrigin(x, baseline)
    text_object.setFont(font_name, font_size)
    text_object.setCharSpace(char_space)
    text_object.textLine(text)
    pdf.drawText(text_object)


def _draw_text(pdf, *, text: str, element: dict, x: float, y: float, width: float, height: float) -> None:
    style = element["style"]
    font_size = style["fontSize"] * CSS_PX_TO_PT
    font_name = _font_name(
        style["fontFamily"],
        bold=style["bold"],
        italic=style.get("italic", False),
    )
    char_space = style["letterSpacing"] * CSS_PX_TO_PT
    text = _transform_text(text, style["textTransform"])
    leading = font_size * style["lineHeight"]
    lines = _wrap_text(text, font_name, font_size, width, char_space)
    max_lines = max(1, int(height // leading))
    lines = lines[:max_lines]
    block_height = len(lines) * leading
    baseline = y + (height - block_height) / 2 + block_height - font_size

    clip = pdf.beginPath()
    clip.rect(x, y, width, height)
    pdf.clipPath(clip, stroke=0, fill=0)
    pdf.setFillColor(HexColor(style["color"]))
    pdf.setFont(font_name, font_size)
    for line in lines:
        text_width = _text_width(line, font_name, font_size, char_space)
        line_x = _aligned_x(x, width, text_width, style["align"])
        _draw_tracked_line(
            pdf,
            text=line,
            x=line_x,
            baseline=baseline,
            font_name=font_name,
            font_size=font_size,
            char_space=char_space,
        )
        if style.get("underline"):
            pdf.setLineWidth(max(0.35, font_size / 18))
            pdf.line(line_x, baseline - 1.2, line_x + text_width, baseline - 1.2)
        baseline -= leading


def _draw_list(pdf, *, element: dict, x: float, y: float, width: float, height: float) -> None:
    style = element["style"]
    font_size = style["fontSize"] * CSS_PX_TO_PT
    font_name = _font_name(
        style["fontFamily"], bold=style["bold"], italic=style.get("italic", False)
    )
    char_space = style["letterSpacing"] * CSS_PX_TO_PT
    leading = font_size * style["lineHeight"]
    indent = style["indent_mm"] * mm
    marker_gap = max(2, font_size * 0.35)
    rows = []
    for index, item in enumerate(element["items"], start=1):
        marker = "•" if style["listType"] == "bullet" else f"{index}."
        marker_width = _text_width(marker, font_name, font_size, char_space)
        content_x = x + min(indent, max(0, width - marker_width - marker_gap))
        available = max(1, width - (content_x - x) - marker_width - marker_gap)
        transformed = _transform_text(item, style["textTransform"])
        wrapped = _wrap_text(transformed, font_name, font_size, available, char_space)
        rows.append((marker, marker_width, content_x, available, wrapped))

    flattened = [
        (marker, marker_width, content_x, available, line, line_index)
        for marker, marker_width, content_x, available, lines in rows
        for line_index, line in enumerate(lines)
    ]
    max_lines = max(1, int(height // leading))
    flattened = flattened[:max_lines]
    block_height = len(flattened) * leading
    baseline = y + (height - block_height) / 2 + block_height - font_size

    clip = pdf.beginPath()
    clip.rect(x, y, width, height)
    pdf.clipPath(clip, stroke=0, fill=0)
    pdf.setFillColor(HexColor(style["color"]))
    for marker, marker_width, content_x, available, line, line_index in flattened:
        if line_index == 0:
            marker_x = content_x
            _draw_tracked_line(
                pdf,
                text=marker,
                x=marker_x,
                baseline=baseline,
                font_name=font_name,
                font_size=font_size,
                char_space=char_space,
            )
        content_start = content_x + marker_width + marker_gap
        line_x = _aligned_x(
            content_start,
            available,
            _text_width(line, font_name, font_size, char_space),
            style["align"],
        )
        _draw_tracked_line(
            pdf,
            text=line,
            x=line_x,
            baseline=baseline,
            font_name=font_name,
            font_size=font_size,
            char_space=char_space,
        )
        baseline -= leading


def _draw_table(pdf, *, element: dict, x: float, y: float, width: float, height: float) -> None:
    style = element["style"]
    rows = [element["columns"], *element["rows"]]
    column_count = len(element["columns"])
    row_count = len(rows)
    column_width = width / column_count
    row_height = height / row_count
    font_size = style["fontSize"] * CSS_PX_TO_PT
    font_name = _font_name(style["fontFamily"], bold=style["bold"])

    pdf.setStrokeColor(HexColor(style["borderColor"]))
    pdf.setLineWidth(0.5)
    pdf.setFillColor(HexColor(style["headerBackground"]))
    pdf.rect(x, y + height - row_height, width, row_height, stroke=0, fill=1)
    for row_index, row in enumerate(rows):
        cell_y = y + height - ((row_index + 1) * row_height)
        for column_index, value in enumerate(row):
            cell_x = x + column_index * column_width
            pdf.rect(cell_x, cell_y, column_width, row_height, stroke=1, fill=0)
            available_width = max(0, column_width - 4)
            clipped_value = value
            while (
                clipped_value
                and pdfmetrics.stringWidth(clipped_value, font_name, font_size)
                > available_width
            ):
                clipped_value = clipped_value[:-1]
            if clipped_value != value and len(clipped_value) > 1:
                clipped_value = f"{clipped_value[:-1]}…"
            text_width = pdfmetrics.stringWidth(clipped_value, font_name, font_size)
            text_x = _aligned_x(
                cell_x + 2,
                available_width,
                text_width,
                style["align"],
            )
            text_y = cell_y + (row_height - font_size) / 2
            pdf.setFillColor(HexColor(style["color"]))
            pdf.setFont(font_name, font_size)
            pdf.drawString(text_x, text_y, clipped_value)


def _draw_icon(pdf, *, element: dict, x: float, y: float, width: float, height: float) -> None:
    style = element["style"]
    center_x = x + width / 2
    center_y = y + height / 2
    radius = min(width, height) * 0.42
    pdf.setStrokeColor(HexColor(style["color"]))
    pdf.setFillColor(HexColor(style["color"]))
    pdf.setLineWidth(max(1, radius / 8))
    if element["iconName"] == "patch-check":
        pdf.circle(center_x, center_y, radius, stroke=1, fill=0)
        pdf.line(center_x - radius * 0.5, center_y, center_x - radius * 0.1, center_y - radius * 0.4)
        pdf.line(center_x - radius * 0.1, center_y - radius * 0.4, center_x + radius * 0.6, center_y + radius * 0.45)
    elif element["iconName"] == "award":
        pdf.circle(center_x, center_y + radius * 0.25, radius * 0.7, stroke=1, fill=0)
        pdf.line(center_x - radius * 0.35, center_y - radius * 0.4, center_x - radius * 0.55, center_y - radius)
        pdf.line(center_x + radius * 0.35, center_y - radius * 0.4, center_x + radius * 0.55, center_y - radius)
    else:
        points = []
        for index in range(10):
            angle = 90 + index * 36
            point_radius = radius if index % 2 == 0 else radius * 0.42
            from math import cos, radians, sin

            points.append(
                (
                    center_x + point_radius * cos(radians(angle)),
                    center_y + point_radius * sin(radians(angle)),
                )
            )
        path = pdf.beginPath()
        path.moveTo(*points[0])
        for point in points[1:]:
            path.lineTo(*point)
        path.close()
        pdf.drawPath(path, stroke=0, fill=1)


def _fitted_box(*, source_width: float, source_height: float, x: float, y: float, width: float, height: float, fit: str):
    if fit == "stretch":
        return x, y, width, height
    scale = (
        max(width / source_width, height / source_height)
        if fit == "cover"
        else min(width / source_width, height / source_height)
    )
    draw_width = source_width * scale
    draw_height = source_height * scale
    return (
        x + (width - draw_width) / 2,
        y + (height - draw_height) / 2,
        draw_width,
        draw_height,
    )


def _draw_media(pdf, *, asset, element: dict, x: float, y: float, width: float, height: float) -> None:
    with asset.file.open("rb") as file_handle:
        content = file_handle.read()
    if asset.kind == asset.Kind.SVG:
        drawing = svg2rlg(BytesIO(content))
        if drawing is None or not drawing.width or not drawing.height:
            raise ValueError("Fișierul SVG nu poate fi redat în PDF.")
        source_width, source_height = drawing.width, drawing.height
    else:
        drawing = None
        image = ImageReader(BytesIO(content))
        source_width, source_height = image.getSize()

    draw_x, draw_y, draw_width, draw_height = _fitted_box(
        source_width=source_width,
        source_height=source_height,
        x=x,
        y=y,
        width=width,
        height=height,
        fit=element["style"].get("fit", "contain"),
    )
    pdf.saveState()
    clip = pdf.beginPath()
    clip.rect(x, y, width, height)
    pdf.clipPath(clip, stroke=0, fill=0)
    opacity = element["style"]["opacity"]
    if hasattr(pdf, "setFillAlpha"):
        pdf.setFillAlpha(opacity)
        pdf.setStrokeAlpha(opacity)
    if drawing is not None:
        pdf.translate(draw_x, draw_y)
        pdf.scale(draw_width / source_width, draw_height / source_height)
        renderPDF.draw(drawing, pdf, 0, 0)
    else:
        pdf.drawImage(
            image,
            draw_x,
            draw_y,
            width=draw_width,
            height=draw_height,
            mask="auto",
        )
    pdf.restoreState()


def render_diploma_pdf(*, template, participant) -> bytes:
    layout = validate_layout_json(template.layout_json)
    assets = require_owned_layout_assets(owner=template.owner, layout=layout)
    page = layout["page"]
    page_width = page["width_mm"] * mm
    page_height = page["height_mm"] * mm
    participant_data = _participant_data(participant)
    buffer = BytesIO()
    pdf = pdf_canvas.Canvas(
        buffer,
        pagesize=(page_width, page_height),
        pageCompression=1,
    )
    pdf.setTitle(f"Diplomă - {participant.full_name}")
    pdf.setAuthor("Platforma TUVTK")

    for element in sorted(layout["elements"], key=lambda item: item["zIndex"]):
        if not element["visible"]:
            continue
        x = element["x_mm"] * mm
        y = (page["height_mm"] - element["y_mm"] - element["height_mm"]) * mm
        width = element["width_mm"] * mm
        height = element["height_mm"] * mm

        pdf.saveState()
        if element["rotation"]:
            center_x = x + width / 2
            center_y = y + height / 2
            pdf.translate(center_x, center_y)
            pdf.rotate(-element["rotation"])
            x, y = -width / 2, -height / 2

        if element["type"] in {"image", "background"}:
            _draw_media(
                pdf,
                asset=assets[element["assetId"]],
                element=element,
                x=x,
                y=y,
                width=width,
                height=height,
            )
        elif element["type"] == "text":
            _draw_text(
                pdf,
                text=element["text"],
                element=element,
                x=x,
                y=y,
                width=width,
                height=height,
            )
        elif element["type"] == "variable":
            _draw_text(
                pdf,
                text=participant_data[element["variable"]],
                element=element,
                x=x,
                y=y,
                width=width,
                height=height,
            )
        elif element["type"] == "list":
            _draw_list(
                pdf,
                element=element,
                x=x,
                y=y,
                width=width,
                height=height,
            )
        elif element["type"] == "table":
            _draw_table(
                pdf,
                element=element,
                x=x,
                y=y,
                width=width,
                height=height,
            )
        elif element["type"] == "icon":
            if element.get("assetId"):
                _draw_media(
                    pdf,
                    asset=assets[element["assetId"]],
                    element=element,
                    x=x,
                    y=y,
                    width=width,
                    height=height,
                )
            else:
                _draw_icon(
                    pdf,
                    element=element,
                    x=x,
                    y=y,
                    width=width,
                    height=height,
                )
        pdf.restoreState()

    pdf.showPage()
    pdf.save()
    return buffer.getvalue()
```

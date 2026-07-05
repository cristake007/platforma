# apps/diplome/validators.py

Generated: `2026-07-05T22:30:50`

## Scope

- Real source file: `apps/diplome/validators.py`
- App: `diplome`
- App guide: `codex-context/apps/diplome.md`
- Role: `backend`
- Size: 20936 bytes
- Source SHA-256: `c4fb8049a9e82c9057d787663a0940e2f1cd88d2ea3441ea8b0ef3dc16593740`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
import math
import re
import uuid
from copy import deepcopy

from django.core.exceptions import ValidationError


MAX_LAYOUT_JSON_BYTES = 256 * 1024
MAX_PARTICIPANT_UPLOAD_BYTES = 10 * 1024 * 1024
MAX_PARTICIPANT_ROWS = 5000
PARTICIPANT_UPLOAD_EXTENSIONS = {".csv", ".xlsx"}
MAX_LAYOUT_ELEMENTS = 100
MAX_TEXT_LENGTH = 500
MAX_TABLE_COLUMNS = 8
MAX_TABLE_ROWS = 20
MAX_LIST_ITEMS = 20
MAX_LIST_ITEM_LENGTH = 200
MAX_GUIDES_PER_AXIS = 50

SUPPORTED_ELEMENT_TYPES = {"text", "variable", "list", "image", "icon", "table", "background"}
SUPPORTED_VARIABLES = {
    "full_name",
    "date_of_birth",
    "place_of_birth",
    "certificate_number",
}
SUPPORTED_FONTS = {"Inter", "Lora", "Georgia", "Arial", "Times New Roman"}
SUPPORTED_ICONS = {"award", "patch-check", "star"}

ELEMENT_ID_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{0,63}$")
HEX_COLOR_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")
HTML_TAG_RE = re.compile(r"</?[A-Za-z][^>]*>")
UNSAFE_SCHEME_RE = re.compile(
    r"(?:https?://|www\.|(?:data|javascript|vbscript|file|ftp):)", re.IGNORECASE
)
CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")

TOP_LEVEL_KEYS = {"version", "page", "elements", "guides"}
GUIDE_KEYS = {"vertical", "horizontal"}
PAGE_KEYS = {
    "size",
    "orientation",
    "width_mm",
    "height_mm",
    "grid_mm",
    "major_grid_mm",
    "background",
}
COMMON_ELEMENT_KEYS = {
    "id",
    "type",
    "label",
    "x_mm",
    "y_mm",
    "width_mm",
    "height_mm",
    "rotation",
    "zIndex",
    "locked",
    "visible",
    "style",
}
TYPOGRAPHY_STYLE_KEYS = {
    "fontFamily",
    "fontSize",
    "bold",
    "italic",
    "underline",
    "color",
    "align",
    "lineHeight",
    "letterSpacing",
    "textTransform",
}
LEGACY_TYPOGRAPHY_STYLE_KEYS = TYPOGRAPHY_STYLE_KEYS - {
    "lineHeight",
    "letterSpacing",
    "textTransform",
}
LIST_STYLE_KEYS = TYPOGRAPHY_STYLE_KEYS | {"listType", "indent_mm"}
IMAGE_STYLE_KEYS = {"fit", "opacity"}
ICON_STYLE_KEYS = {"color", "opacity"}
TABLE_STYLE_KEYS = {
    "fontFamily",
    "fontSize",
    "bold",
    "color",
    "align",
    "borderColor",
    "headerBackground",
}
TYPE_KEYS = {
    "text": {"text"},
    "variable": {"variable", "placeholder"},
    "list": {"items"},
    "image": {"assetId", "alt"},
    "background": {"assetId", "alt"},
    "icon": {"iconName"},
    "table": {"columns", "rows"},
}
A4_PAGE_MM = {
    "landscape": (297, 210),
    "portrait": (210, 297),
}


def _fail(message: str) -> None:
    raise ValidationError(message)


def _require_exact_keys(value: dict, expected: set[str], label: str) -> None:
    missing = expected - set(value)
    unknown = set(value) - expected
    if missing:
        _fail(f"{label}: lipsesc câmpurile {', '.join(sorted(missing))}.")
    if unknown:
        _fail(f"{label}: câmpuri necunoscute {', '.join(sorted(unknown))}.")


def _plain_text(value, label: str, *, allow_empty: bool = False, max_length: int = MAX_TEXT_LENGTH) -> str:
    if not isinstance(value, str):
        _fail(f"{label} trebuie să fie text.")
    clean = value.strip()
    if not clean and not allow_empty:
        _fail(f"{label} este obligatoriu.")
    if len(clean) > max_length:
        _fail(f"{label} depășește limita de {max_length} caractere.")
    if CONTROL_RE.search(clean) or HTML_TAG_RE.search(clean) or UNSAFE_SCHEME_RE.search(clean):
        _fail(f"{label} conține conținut nesigur.")
    return clean


def _integer(value, label: str, minimum: int, maximum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        _fail(f"{label} trebuie să fie un număr întreg.")
    if not minimum <= value <= maximum:
        _fail(f"{label} trebuie să fie între {minimum} și {maximum}.")
    return value


def _boolean(value, label: str) -> bool:
    if not isinstance(value, bool):
        _fail(f"{label} trebuie să fie true sau false.")
    return value


def _validate_guides(guides, page: dict) -> dict:
    if not isinstance(guides, dict):
        _fail("Layout.guides trebuie să fie un obiect.")
    _require_exact_keys(guides, GUIDE_KEYS, "Layout.guides")
    normalized = {}
    for orientation, maximum in (
        ("vertical", page["width_mm"]),
        ("horizontal", page["height_mm"]),
    ):
        positions = guides[orientation]
        if not isinstance(positions, list):
            _fail(f"Layout.guides.{orientation} trebuie să fie o listă.")
        if len(positions) > MAX_GUIDES_PER_AXIS:
            _fail(
                f"Layout.guides.{orientation} poate conține cel mult "
                f"{MAX_GUIDES_PER_AXIS} ghidaje."
            )
        validated = [
            _integer(
                position,
                f"Layout.guides.{orientation}[{index}]",
                0,
                maximum,
            )
            for index, position in enumerate(positions)
        ]
        normalized[orientation] = sorted(set(validated))
    return normalized


def _color(value, label: str) -> str:
    if not isinstance(value, str) or not HEX_COLOR_RE.fullmatch(value):
        _fail(f"{label} trebuie să fie o culoare #RRGGBB.")
    return value.lower()


def _opacity(value, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        _fail(f"{label} trebuie să fie un număr finit.")
    if not 0 <= value <= 1:
        _fail(f"{label} trebuie să fie între 0 și 1.")
    return float(value)


def _number(value, label: str, minimum: float, maximum: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        _fail(f"{label} trebuie să fie un număr finit.")
    if not minimum <= value <= maximum:
        _fail(f"{label} trebuie să fie între {minimum} și {maximum}.")
    return float(value)


def _validate_typography_style(style: dict, label: str) -> dict:
    unknown = set(style) - TYPOGRAPHY_STYLE_KEYS
    missing_legacy = LEGACY_TYPOGRAPHY_STYLE_KEYS - set(style)
    if unknown:
        _fail(f"{label}: câmpuri necunoscute {', '.join(sorted(unknown))}.")
    if missing_legacy:
        _fail(f"{label}: lipsesc câmpurile {', '.join(sorted(missing_legacy))}.")
    style = {
        **style,
        "lineHeight": style.get("lineHeight", 1.18),
        "letterSpacing": style.get("letterSpacing", 0),
        "textTransform": style.get("textTransform", "none"),
    }
    if style["fontFamily"] not in SUPPORTED_FONTS:
        _fail(f"{label}.fontFamily nu este acceptat.")
    if style["align"] not in {"left", "center", "right"}:
        _fail(f"{label}.align nu este acceptat.")
    if style["textTransform"] not in {"none", "uppercase", "lowercase"}:
        _fail(f"{label}.textTransform nu este acceptat.")
    return {
        "fontFamily": style["fontFamily"],
        "fontSize": _integer(style["fontSize"], f"{label}.fontSize", 8, 200),
        "bold": _boolean(style["bold"], f"{label}.bold"),
        "italic": _boolean(style["italic"], f"{label}.italic"),
        "underline": _boolean(style["underline"], f"{label}.underline"),
        "color": _color(style["color"], f"{label}.color"),
        "align": style["align"],
        "lineHeight": _number(style["lineHeight"], f"{label}.lineHeight", 0.8, 3),
        "letterSpacing": _number(
            style["letterSpacing"], f"{label}.letterSpacing", -5, 20
        ),
        "textTransform": style["textTransform"],
    }


def _validate_style(element_type: str, style, label: str) -> dict:
    if not isinstance(style, dict):
        _fail(f"{label} trebuie să fie un obiect.")
    if element_type in {"text", "variable"}:
        return _validate_typography_style(style, label)
    if element_type == "list":
        unknown = set(style) - LIST_STYLE_KEYS
        required = LEGACY_TYPOGRAPHY_STYLE_KEYS | {"listType", "indent_mm"}
        missing = required - set(style)
        if unknown:
            _fail(f"{label}: câmpuri necunoscute {', '.join(sorted(unknown))}.")
        if missing:
            _fail(f"{label}: lipsesc câmpurile {', '.join(sorted(missing))}.")
        normalized = _validate_typography_style(
            {key: style[key] for key in TYPOGRAPHY_STYLE_KEYS if key in style}, label
        )
        if style["listType"] not in {"bullet", "number"}:
            _fail(f"{label}.listType nu este acceptat.")
        normalized.update({
            "listType": style["listType"],
            "indent_mm": _number(style["indent_mm"], f"{label}.indent_mm", 0, 50),
        })
        return normalized
    if element_type in {"image", "background"}:
        _require_exact_keys(style, IMAGE_STYLE_KEYS, label)
        if style["fit"] not in {"contain", "cover", "stretch"}:
            _fail(f"{label}.fit nu este acceptat.")
        return {"fit": style["fit"], "opacity": _opacity(style["opacity"], f"{label}.opacity")}
    if element_type == "icon":
        _require_exact_keys(style, ICON_STYLE_KEYS, label)
        return {
            "color": _color(style["color"], f"{label}.color"),
            "opacity": _opacity(style["opacity"], f"{label}.opacity"),
        }
    _require_exact_keys(style, TABLE_STYLE_KEYS, label)
    if style["fontFamily"] not in SUPPORTED_FONTS:
        _fail(f"{label}.fontFamily nu este acceptat.")
    if style["align"] not in {"left", "center", "right"}:
        _fail(f"{label}.align nu este acceptat.")
    return {
        "fontFamily": style["fontFamily"],
        "fontSize": _integer(style["fontSize"], f"{label}.fontSize", 8, 72),
        "bold": _boolean(style["bold"], f"{label}.bold"),
        "color": _color(style["color"], f"{label}.color"),
        "align": style["align"],
        "borderColor": _color(style["borderColor"], f"{label}.borderColor"),
        "headerBackground": _color(style["headerBackground"], f"{label}.headerBackground"),
    }


def _validate_element(element, index: int, page: dict) -> dict:
    label = f"Elementul {index + 1}"
    if not isinstance(element, dict):
        _fail(f"{label} trebuie să fie un obiect.")
    element_type = element.get("type")
    if element_type not in SUPPORTED_ELEMENT_TYPES:
        _fail(f"{label}.type nu este acceptat.")
    if element_type == "icon":
        required_keys = COMMON_ELEMENT_KEYS | TYPE_KEYS[element_type]
        allowed_keys = required_keys | {"assetId", "alt"}
        missing = required_keys - set(element)
        unknown = set(element) - allowed_keys
        if missing:
            _fail(f"{label}: lipsesc câmpurile {', '.join(sorted(missing))}.")
        if unknown:
            _fail(f"{label}: câmpuri necunoscute {', '.join(sorted(unknown))}.")
        if ("assetId" in element) != ("alt" in element):
            _fail(f"{label}: assetId și alt trebuie furnizate împreună.")
    else:
        _require_exact_keys(element, COMMON_ELEMENT_KEYS | TYPE_KEYS[element_type], label)

    element_id = element["id"]
    if not isinstance(element_id, str) or not ELEMENT_ID_RE.fullmatch(element_id):
        _fail(f"{label}.id nu este valid.")

    width_mm = _integer(
        element["width_mm"], f"{label}.width_mm", 1, page["width_mm"]
    )
    height_mm = _integer(
        element["height_mm"], f"{label}.height_mm", 1, page["height_mm"]
    )
    x_mm = _integer(
        element["x_mm"], f"{label}.x_mm", 0, page["width_mm"] - width_mm
    )
    y_mm = _integer(
        element["y_mm"], f"{label}.y_mm", 0, page["height_mm"] - height_mm
    )
    z_index = _integer(element["zIndex"], f"{label}.zIndex", 0, 1000)

    normalized = {
        "id": element_id,
        "type": element_type,
        "label": _plain_text(element["label"], f"{label}.label", max_length=120),
        "x_mm": x_mm,
        "y_mm": y_mm,
        "width_mm": width_mm,
        "height_mm": height_mm,
        "rotation": _integer(element["rotation"], f"{label}.rotation", -180, 180),
        "zIndex": z_index,
        "locked": _boolean(element["locked"], f"{label}.locked"),
        "visible": _boolean(element["visible"], f"{label}.visible"),
        "style": _validate_style(element_type, element["style"], f"{label}.style"),
    }

    if element_type == "text":
        normalized["text"] = _plain_text(element["text"], f"{label}.text")
    elif element_type == "variable":
        if element["variable"] not in SUPPORTED_VARIABLES:
            _fail(f"{label}.variable nu este acceptată.")
        normalized["variable"] = element["variable"]
        normalized["placeholder"] = _plain_text(element["placeholder"], f"{label}.placeholder")
    elif element_type == "list":
        items = element["items"]
        if not isinstance(items, list) or not 1 <= len(items) <= MAX_LIST_ITEMS:
            _fail(
                f"{label}.items trebuie să conțină între 1 și {MAX_LIST_ITEMS} elemente."
            )
        normalized["items"] = [
            _plain_text(
                item,
                f"{label}.items[{item_index}]",
                max_length=MAX_LIST_ITEM_LENGTH,
            )
            for item_index, item in enumerate(items, start=1)
        ]
    elif element_type in {"image", "background"}:
        try:
            asset_id = uuid.UUID(str(element["assetId"]))
        except (AttributeError, TypeError, ValueError) as exc:
            raise ValidationError(f"{label}.assetId trebuie să fie un UUID valid.") from exc
        normalized["assetId"] = str(asset_id)
        normalized["alt"] = _plain_text(element["alt"], f"{label}.alt", allow_empty=True, max_length=160)
        if element_type == "background":
            if (x_mm, y_mm, width_mm, height_mm, z_index) != (
                0,
                0,
                page["width_mm"],
                page["height_mm"],
                0,
            ):
                _fail("Fundalul trebuie să acopere integral pagina și să aibă zIndex 0.")
    elif element_type == "icon":
        if element["iconName"] not in SUPPORTED_ICONS:
            _fail(f"{label}.iconName nu este acceptat.")
        normalized["iconName"] = element["iconName"]
        if "assetId" in element:
            try:
                asset_id = uuid.UUID(str(element["assetId"]))
            except (AttributeError, TypeError, ValueError) as exc:
                raise ValidationError(f"{label}.assetId trebuie să fie un UUID valid.") from exc
            normalized["assetId"] = str(asset_id)
            normalized["alt"] = _plain_text(
                element["alt"], f"{label}.alt", allow_empty=True, max_length=160
            )
    else:
        columns = element["columns"]
        rows = element["rows"]
        if not isinstance(columns, list) or not 1 <= len(columns) <= MAX_TABLE_COLUMNS:
            _fail(f"{label}.columns trebuie să conțină între 1 și {MAX_TABLE_COLUMNS} coloane.")
        if not isinstance(rows, list) or len(rows) > MAX_TABLE_ROWS:
            _fail(f"{label}.rows poate conține cel mult {MAX_TABLE_ROWS} rânduri.")
        normalized["columns"] = [
            _plain_text(value, f"{label}.columns", max_length=120) for value in columns
        ]
        normalized_rows = []
        for row_number, row in enumerate(rows, start=1):
            if not isinstance(row, list) or len(row) != len(columns):
                _fail(f"{label}.rows[{row_number}] nu corespunde numărului de coloane.")
            normalized_rows.append([
                _plain_text(value, f"{label}.rows[{row_number}]", allow_empty=True, max_length=160)
                for value in row
            ])
        normalized["rows"] = normalized_rows
    return normalized


def convert_layout_v1_to_v2(layout) -> dict:
    if not isinstance(layout, dict) or layout.get("version") != 1:
        return deepcopy(layout)
    page = layout.get("page")
    elements = layout.get("elements")
    if not isinstance(page, dict) or not isinstance(elements, list):
        _fail("Layout-ul versiunea 1 nu poate fi convertit.")

    orientation = page.get("orientation")
    if orientation not in A4_PAGE_MM:
        _fail("Orientarea paginii nu este acceptată.")
    old_width = page.get("width")
    old_height = page.get("height")
    if (
        isinstance(old_width, bool)
        or isinstance(old_height, bool)
        or not isinstance(old_width, (int, float))
        or not isinstance(old_height, (int, float))
        or old_width <= 0
        or old_height <= 0
    ):
        _fail("Dimensiunile layout-ului versiunea 1 nu sunt valide.")

    page_width_mm, page_height_mm = A4_PAGE_MM[orientation]
    converted_elements = []
    for source in elements:
        if not isinstance(source, dict):
            _fail("Elementele layout-ului versiunea 1 nu sunt valide.")
        converted = deepcopy(source)
        try:
            width_mm = max(1, min(page_width_mm, round(source["width"] * page_width_mm / old_width)))
            height_mm = max(1, min(page_height_mm, round(source["height"] * page_height_mm / old_height)))
            x_mm = max(0, min(page_width_mm - width_mm, round(source["x"] * page_width_mm / old_width)))
            y_mm = max(0, min(page_height_mm - height_mm, round(source["y"] * page_height_mm / old_height)))
        except (KeyError, TypeError, ValueError) as exc:
            _fail("Geometria layout-ului versiunea 1 nu poate fi convertită.")
        for old_key in ("x", "y", "width", "height"):
            converted.pop(old_key, None)
        converted.update({
            "x_mm": x_mm,
            "y_mm": y_mm,
            "width_mm": width_mm,
            "height_mm": height_mm,
        })
        if converted.get("type") == "background":
            converted.update({
                "x_mm": 0,
                "y_mm": 0,
                "width_mm": page_width_mm,
                "height_mm": page_height_mm,
            })
        converted_elements.append(converted)

    return {
        "version": 2,
        "page": {
            "size": "A4",
            "orientation": orientation,
            "width_mm": page_width_mm,
            "height_mm": page_height_mm,
            "grid_mm": 1,
            "major_grid_mm": 10,
            "background": None,
        },
        "elements": converted_elements,
    }


def validate_layout_json(layout) -> dict:
    if not isinstance(layout, dict):
        _fail("Layout-ul trebuie să fie un obiect JSON.")
    layout = convert_layout_v1_to_v2(layout)
    if "guides" not in layout:
        layout = {**layout, "guides": {"vertical": [], "horizontal": []}}
    _require_exact_keys(layout, TOP_LEVEL_KEYS, "Layout")
    if layout["version"] != 2:
        _fail("Este acceptată doar versiunea 2 a layout-ului.")

    page = layout["page"]
    if not isinstance(page, dict):
        _fail("Layout.page trebuie să fie un obiect.")
    _require_exact_keys(page, PAGE_KEYS, "Layout.page")
    if page["size"] != "A4":
        _fail("În această versiune este acceptat doar formatul A4.")
    if page["orientation"] not in {"landscape", "portrait"}:
        _fail("Orientarea paginii nu este acceptată.")
    expected_width_mm, expected_height_mm = A4_PAGE_MM[page["orientation"]]
    normalized_page = {
        "size": "A4",
        "orientation": page["orientation"],
        "width_mm": _integer(page["width_mm"], "Layout.page.width_mm", 1, 1000),
        "height_mm": _integer(page["height_mm"], "Layout.page.height_mm", 1, 1000),
        "grid_mm": _integer(page["grid_mm"], "Layout.page.grid_mm", 1, 2),
        "major_grid_mm": _integer(
            page["major_grid_mm"], "Layout.page.major_grid_mm", 10, 10
        ),
        "background": None,
    }
    if (
        normalized_page["width_mm"],
        normalized_page["height_mm"],
    ) != (expected_width_mm, expected_height_mm):
        _fail("Dimensiunile paginii nu corespund formatului A4 selectat.")
    if normalized_page["major_grid_mm"] % normalized_page["grid_mm"]:
        _fail("Grila majoră trebuie să fie un multiplu al grilei de snapping.")
    if page["background"] is not None:
        _fail("Layout.page.background trebuie să fie null în această versiune.")

    normalized_guides = _validate_guides(layout["guides"], normalized_page)

    elements = layout["elements"]
    if not isinstance(elements, list):
        _fail("Layout.elements trebuie să fie o listă.")
    if len(elements) > MAX_LAYOUT_ELEMENTS:
        _fail(f"Layout-ul poate conține cel mult {MAX_LAYOUT_ELEMENTS} elemente.")
    normalized_elements = [
        _validate_element(element, index, normalized_page) for index, element in enumerate(elements)
    ]
    ids = [element["id"] for element in normalized_elements]
    if len(ids) != len(set(ids)):
        _fail("Identificatorii elementelor trebuie să fie unici.")
    if sum(element["type"] == "background" for element in normalized_elements) > 1:
        _fail("Layout-ul poate conține un singur fundal.")

    return deepcopy({
        "version": 2,
        "page": normalized_page,
        "guides": normalized_guides,
        "elements": normalized_elements,
    })
```

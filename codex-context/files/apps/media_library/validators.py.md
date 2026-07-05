# apps/media_library/validators.py

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `apps/media_library/validators.py`
- App: `media_library`
- App guide: `codex-context/apps/media_library.md`
- Role: `backend`
- Size: 14423 bytes
- Source SHA-256: `7e3aac9dff4d126b3b875447810207193aac7d49088c487568def3ed736097ad`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
import hashlib
import re
import warnings
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from xml.etree import ElementTree

from defusedxml import ElementTree as DefusedElementTree
from defusedxml.common import DefusedXmlException
from django.core.exceptions import ValidationError
from PIL import Image, ImageOps, UnidentifiedImageError
import tinycss2


MAX_MEDIA_FILE_BYTES = 10 * 1024 * 1024
MAX_SVG_FILE_BYTES = 2 * 1024 * 1024
MAX_RASTER_PIXELS = 40_000_000
MAX_RASTER_DIMENSION = 10_000
MAX_SVG_ELEMENTS = 2_000
MAX_SVG_DEPTH = 32
SVG_NAMESPACE = "http://www.w3.org/2000/svg"

RASTER_FORMATS = {
    ".png": ("PNG", "image/png"),
    ".jpg": ("JPEG", "image/jpeg"),
    ".jpeg": ("JPEG", "image/jpeg"),
    ".webp": ("WEBP", "image/webp"),
}
SUPPORTED_EXTENSIONS = {*RASTER_FORMATS, ".svg"}

SVG_ALLOWED_TAG_ATTRIBUTES = {
    "svg": {"viewBox", "width", "height", "preserveAspectRatio"},
    "g": set(),
    "path": {"d", "pathLength"},
    "rect": {"x", "y", "width", "height", "rx", "ry"},
    "circle": {"cx", "cy", "r"},
    "ellipse": {"cx", "cy", "rx", "ry"},
    "line": {"x1", "y1", "x2", "y2"},
    "polyline": {"points"},
    "polygon": {"points"},
    "defs": set(),
    "linearGradient": {
        "x1", "y1", "x2", "y2", "gradientUnits", "gradientTransform", "spreadMethod",
    },
    "radialGradient": {
        "cx", "cy", "r", "fx", "fy", "fr", "gradientUnits", "gradientTransform", "spreadMethod",
    },
    "stop": {"offset", "stop-color", "stop-opacity"},
}
SVG_GLOBAL_ATTRIBUTES = {
    "id", "transform", "opacity", "fill", "fill-opacity", "fill-rule", "clip-rule",
    "stroke", "stroke-width", "stroke-opacity", "stroke-linecap", "stroke-linejoin",
    "stroke-miterlimit", "stroke-dasharray", "stroke-dashoffset", "vector-effect",
    "stop-color", "stop-opacity",
}
SVG_STRIPPED_METADATA_ATTRIBUTES = {"data-name"}
SVG_SAFE_CSS_PROPERTIES = {
    "fill", "fill-opacity", "fill-rule", "clip-rule", "opacity", "stop-color", "stop-opacity",
    "stroke", "stroke-width", "stroke-opacity", "stroke-linecap", "stroke-linejoin",
    "stroke-miterlimit", "stroke-dasharray", "stroke-dashoffset", "vector-effect",
}
SVG_INTERNAL_URL_RE = re.compile(r"^url\(#[A-Za-z_][A-Za-z0-9_.:-]{0,127}\)$")
SVG_ID_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_.:-]{0,127}$")
SVG_CLASS_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]{0,127}$")
SVG_CLASS_SELECTOR_RE = re.compile(r"^\.[A-Za-z_][A-Za-z0-9_-]{0,127}$")
SVG_COLOR_FUNCTION_RE = re.compile(r"^(?:rgb|rgba|hsl|hsla)\([^()]{1,128}\)$", re.IGNORECASE)
UNSAFE_VALUE_RE = re.compile(r"(?:javascript\s*:|data\s*:|https?\s*:|//)", re.IGNORECASE)
CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


@dataclass(frozen=True)
class PreparedMedia:
    content: bytes
    extension: str
    kind: str
    mime_type: str
    width_px: int | None
    height_px: int | None
    sha256: str


def _read_upload(uploaded_file) -> tuple[bytes, str]:
    original_name = Path(uploaded_file.name or "").name
    extension = Path(original_name).suffix.lower()
    if extension not in SUPPORTED_EXTENSIONS:
        raise ValidationError("Sunt acceptate doar fișiere SVG, PNG, JPG, JPEG și WEBP.")
    limit = MAX_SVG_FILE_BYTES if extension == ".svg" else MAX_MEDIA_FILE_BYTES
    content = uploaded_file.read(limit + 1)
    if not content:
        raise ValidationError("Fișierul este gol.")
    if len(content) > limit:
        limit_mb = limit // (1024 * 1024)
        raise ValidationError(f"Fișierul depășește limita de {limit_mb} MB.")
    return content, extension


def _prepare_raster(content: bytes, extension: str) -> PreparedMedia:
    expected_format, mime_type = RASTER_FORMATS[extension]
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(BytesIO(content)) as source:
                if source.format != expected_format:
                    raise ValidationError("Extensia nu corespunde conținutului imaginii.")
                if getattr(source, "n_frames", 1) != 1:
                    raise ValidationError("Imaginile animate nu sunt acceptate.")
                width, height = source.size
                if (
                    width < 1
                    or height < 1
                    or width > MAX_RASTER_DIMENSION
                    or height > MAX_RASTER_DIMENSION
                    or width * height > MAX_RASTER_PIXELS
                ):
                    raise ValidationError("Dimensiunile imaginii depășesc limitele acceptate.")
                source.load()
                image = ImageOps.exif_transpose(source)
                has_alpha = "A" in image.getbands() or "transparency" in image.info
                image = image.convert("RGBA" if has_alpha and expected_format != "JPEG" else "RGB")
                output = BytesIO()
                if expected_format == "JPEG":
                    image.save(output, format="JPEG", quality=95, optimize=True)
                elif expected_format == "PNG":
                    image.save(output, format="PNG", optimize=True)
                else:
                    image.save(output, format="WEBP", quality=95, method=6)
    except ValidationError:
        raise
    except (Image.DecompressionBombError, Image.DecompressionBombWarning, UnidentifiedImageError, OSError, ValueError) as exc:
        raise ValidationError("Fișierul nu este o imagine validă și sigură.") from exc

    sanitized = output.getvalue()
    return PreparedMedia(
        content=sanitized,
        extension=extension,
        kind="raster",
        mime_type=mime_type,
        width_px=width,
        height_px=height,
        sha256=hashlib.sha256(sanitized).hexdigest(),
    )


def _svg_local_name(qualified_name: str) -> tuple[str, str | None]:
    if qualified_name.startswith("{"):
        namespace, local_name = qualified_name[1:].split("}", 1)
        return local_name, namespace
    return qualified_name, None


def _validate_svg_style_value(value: str) -> str:
    value = value.strip()
    if not value or len(value) > 20_000 or CONTROL_RE.search(value) or UNSAFE_VALUE_RE.search(value):
        raise ValidationError("SVG-ul conține o valoare CSS nesigură.")
    lowered = value.lower()
    if "url(" in lowered and not SVG_INTERNAL_URL_RE.fullmatch(value):
        raise ValidationError("Stilurile SVG pot folosi doar referințe interne către gradienți.")
    if "(" in value and not SVG_INTERNAL_URL_RE.fullmatch(value) and not SVG_COLOR_FUNCTION_RE.fullmatch(value):
        raise ValidationError("SVG-ul conține o funcție CSS neacceptată.")
    return value


def _parse_safe_declarations(content) -> dict[str, str]:
    declarations = {}
    for item in tinycss2.parse_declaration_list(content, skip_comments=True, skip_whitespace=True):
        if item.type == "error":
            raise ValidationError("SVG-ul conține CSS invalid.")
        if item.type != "declaration" or item.lower_name not in SVG_SAFE_CSS_PROPERTIES or item.important:
            raise ValidationError("SVG-ul conține o declarație CSS neacceptată.")
        declarations[item.lower_name] = _validate_svg_style_value(tinycss2.serialize(item.value))
    return declarations


def _sanitize_svg_styles(root) -> None:
    class_rules = []
    for parent in root.iter():
        for child in list(parent):
            tag_name, namespace = _svg_local_name(child.tag)
            if tag_name != "style":
                continue
            if namespace not in {None, SVG_NAMESPACE} or set(child.attrib) - {"type"}:
                raise ValidationError("Elementul SVG style conține atribute neacceptate.")
            if child.attrib.get("type", "text/css").lower() != "text/css":
                raise ValidationError("Elementul SVG style trebuie să conțină CSS.")
            rules = tinycss2.parse_stylesheet(child.text or "", skip_comments=True, skip_whitespace=True)
            for rule in rules:
                if rule.type == "error":
                    raise ValidationError("SVG-ul conține CSS invalid.")
                if rule.type != "qualified-rule":
                    raise ValidationError("Regulile CSS de tip @import, font sau animație nu sunt acceptate.")
                selectors = {
                    selector.strip().removeprefix(".")
                    for selector in tinycss2.serialize(rule.prelude).split(",")
                    if selector.strip()
                }
                serialized_selectors = [selector.strip() for selector in tinycss2.serialize(rule.prelude).split(",")]
                if not serialized_selectors or any(
                    not SVG_CLASS_SELECTOR_RE.fullmatch(selector) for selector in serialized_selectors
                ):
                    raise ValidationError("Sunt acceptați doar selectori CSS simpli de clasă în SVG.")
                class_rules.append((selectors, _parse_safe_declarations(rule.content)))
            parent.remove(child)

    for element in root.iter():
        class_value = element.attrib.pop("class", "").strip()
        inline_style = element.attrib.pop("style", None)
        classes = class_value.split() if class_value else []
        if any(not SVG_CLASS_RE.fullmatch(class_name) for class_name in classes):
            raise ValidationError("SVG-ul conține un nume de clasă CSS invalid.")
        applied = {}
        matched_classes = set()
        for selectors, declarations in class_rules:
            matching = selectors.intersection(classes)
            if matching:
                matched_classes.update(matching)
                applied.update(declarations)
        if set(classes) - matched_classes:
            raise ValidationError("SVG-ul conține o clasă CSS fără o regulă sigură asociată.")
        if inline_style is not None:
            applied.update(_parse_safe_declarations(inline_style))
        for property_name, value in applied.items():
            element.set(property_name, value)


def _validate_svg_tree(root) -> None:
    root_name, root_namespace = _svg_local_name(root.tag)
    if root_name != "svg" or root_namespace not in {None, SVG_NAMESPACE}:
        raise ValidationError("Fișierul trebuie să aibă un element rădăcină SVG valid.")

    ids = set()
    internal_references = set()
    stack = [(root, 1)]
    element_count = 0
    while stack:
        element, depth = stack.pop()
        element_count += 1
        if element_count > MAX_SVG_ELEMENTS or depth > MAX_SVG_DEPTH:
            raise ValidationError("Structura SVG este prea complexă.")
        tag_name, namespace = _svg_local_name(element.tag)
        if namespace not in {None, SVG_NAMESPACE} or tag_name not in SVG_ALLOWED_TAG_ATTRIBUTES:
            raise ValidationError(f"Elementul SVG «{tag_name}» nu este acceptat.")
        if element.text and CONTROL_RE.search(element.text):
            raise ValidationError("SVG-ul conține caractere de control nepermise.")
        if element.text and element.text.strip():
            raise ValidationError("Conținutul text nu este acceptat în SVG.")
        if element.tail and element.tail.strip():
            raise ValidationError("Conținutul text nu este acceptat în SVG.")

        allowed_attributes = SVG_GLOBAL_ATTRIBUTES | SVG_ALLOWED_TAG_ATTRIBUTES[tag_name]
        for qualified_attribute, value in list(element.attrib.items()):
            attribute, attribute_namespace = _svg_local_name(qualified_attribute)
            if attribute_namespace is not None:
                raise ValidationError("Atributele SVG cu namespace nu sunt acceptate.")
            lowered = attribute.lower()
            if lowered.startswith("on") or lowered in {"style", "href"}:
                raise ValidationError(f"Atributul SVG «{attribute}» nu este acceptat.")
            if len(value) > 20_000 or CONTROL_RE.search(value) or UNSAFE_VALUE_RE.search(value):
                raise ValidationError("SVG-ul conține o valoare de atribut nesigură.")
            if attribute in SVG_STRIPPED_METADATA_ATTRIBUTES:
                del element.attrib[qualified_attribute]
                continue
            if attribute not in allowed_attributes:
                raise ValidationError(f"Atributul SVG «{attribute}» nu este acceptat.")
            if "url(" in value.lower():
                if not SVG_INTERNAL_URL_RE.fullmatch(value.strip()):
                    raise ValidationError("SVG-ul poate folosi doar referințe interne către gradienți.")
                internal_references.add(value.strip()[5:-1])
            if attribute == "id":
                if not SVG_ID_RE.fullmatch(value) or value in ids:
                    raise ValidationError("SVG-ul conține un identificator invalid sau duplicat.")
                ids.add(value)
        stack.extend((child, depth + 1) for child in reversed(list(element)))

    if not internal_references.issubset(ids):
        raise ValidationError("SVG-ul conține o referință internă inexistentă.")


def _prepare_svg(content: bytes) -> PreparedMedia:
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValidationError("Fișierul SVG trebuie să fie codificat UTF-8.") from exc
    if re.search(r"<!\s*(?:DOCTYPE|ENTITY)", text, re.IGNORECASE):
        raise ValidationError("Declarațiile DTD și ENTITY nu sunt acceptate în SVG.")
    try:
        root = DefusedElementTree.fromstring(
            text,
            forbid_dtd=True,
            forbid_entities=True,
            forbid_external=True,
        )
    except (DefusedXmlException, ElementTree.ParseError, ValueError) as exc:
        raise ValidationError("Fișierul SVG nu este valid sau conține XML nesigur.") from exc
    _sanitize_svg_styles(root)
    _validate_svg_tree(root)
    ElementTree.register_namespace("", SVG_NAMESPACE)
    sanitized = ElementTree.tostring(root, encoding="utf-8", xml_declaration=True)
    return PreparedMedia(
        content=sanitized,
        extension=".svg",
        kind="svg",
        mime_type="image/svg+xml",
        width_px=None,
        height_px=None,
        sha256=hashlib.sha256(sanitized).hexdigest(),
    )


def validate_and_prepare_media(uploaded_file) -> PreparedMedia:
    content, extension = _read_upload(uploaded_file)
    if extension == ".svg":
        return _prepare_svg(content)
    return _prepare_raster(content, extension)
```

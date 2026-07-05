# apps/planificator/validators.py

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `apps/planificator/validators.py`
- App: `planificator`
- App guide: `codex-context/apps/planificator.md`
- Role: `backend`
- Size: 7118 bytes
- Source SHA-256: `bc23f7ab2758dbd6a74f4d0435c27318020f922fea029fb825af67ae18527ecd`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

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

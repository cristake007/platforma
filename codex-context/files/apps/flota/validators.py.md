# Source snapshot

## `apps/flota/validators.py`

Size: 2.0 KB

```python
import re
from datetime import date
from pathlib import Path

from django.core.exceptions import ValidationError


MAX_EMBLEM_SIZE = 2 * 1024 * 1024
ALLOWED_EMBLEM_TYPES = {"image/jpeg", "image/png", "image/webp"}
ALLOWED_EMBLEM_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
VIN_PATTERN = re.compile(r"^[A-HJ-NPR-Z0-9]{17}$")


def normalize_registration_number(value: str) -> str:
    return re.sub(r"[^A-Z0-9]", "", (value or "").upper())


def normalize_vin(value: str) -> str:
    return "".join((value or "").upper().split())


def validate_registration_number(value: str) -> None:
    normalized = normalize_registration_number(value)
    if not 4 <= len(normalized) <= 12:
        raise ValidationError("Numărul de înmatriculare trebuie să conțină între 4 și 12 caractere.")


def validate_vin(value: str) -> None:
    if value and not VIN_PATTERN.fullmatch(normalize_vin(value)):
        raise ValidationError("VIN-ul trebuie să aibă 17 caractere și nu poate conține I, O sau Q.")


def validate_manufacture_year(value: int | None) -> None:
    if value is None:
        return
    maximum = date.today().year + 1
    if value < 1886 or value > maximum:
        raise ValidationError(f"Anul fabricației trebuie să fie între 1886 și {maximum}.")


def validate_emblem(uploaded_file) -> None:
    if not uploaded_file:
        return
    if uploaded_file.size > MAX_EMBLEM_SIZE:
        raise ValidationError("Emblema nu poate depăși 2 MB.")
    content_type = getattr(uploaded_file, "content_type", "")
    extension = Path(uploaded_file.name).suffix.lower()
    if content_type not in ALLOWED_EMBLEM_TYPES or extension not in ALLOWED_EMBLEM_EXTENSIONS:
        raise ValidationError("Emblema trebuie să fie un fișier JPEG, PNG sau WebP.")


def validate_maintenance_dates(completed_on, next_due_on) -> None:
    if completed_on and next_due_on and next_due_on <= completed_on:
        raise ValidationError({"next_due_on": "Următorul termen trebuie să fie după data efectuării."})
```

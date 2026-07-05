from urllib.parse import urlsplit

from django.core.exceptions import ValidationError


def validate_origin_url(value: str) -> None:
    if not value:
        return
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc or not value.startswith("/") or value.startswith("//"):
        raise ValidationError("Linkul sursă trebuie să fie o cale internă sigură.")


def validate_stage_balance(*, terminal_count: int, non_terminal_count: int) -> None:
    if terminal_count < 1 or non_terminal_count < 1:
        raise ValidationError("Board-ul trebuie să păstreze cel puțin o etapă activă și una terminală.")


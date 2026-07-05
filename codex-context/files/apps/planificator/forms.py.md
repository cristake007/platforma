# apps/planificator/forms.py

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `apps/planificator/forms.py`
- App: `planificator`
- App guide: `codex-context/apps/planificator.md`
- Role: `backend`
- Size: 9620 bytes
- Source SHA-256: `c69ea2ddb113cfd23afca8f841e672fa68e5f52f1730d51e39f7a07a2732b1f2`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

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

# Source snapshot

## `apps/diplome/forms.py`

Size: 14.6 KB

```python
import json
from pathlib import Path

from django import forms
from django.core.exceptions import ValidationError

from .models import DiplomaGenerationBatch, DiplomaTemplate, Participant, ParticipantList
from .selectors import (
    list_owned_participant_lists_with_counts,
    list_owned_templates_for_generation,
)
from .validators import (
    MAX_LAYOUT_JSON_BYTES,
    MAX_PARTICIPANT_UPLOAD_BYTES,
    PARTICIPANT_UPLOAD_EXTENSIONS,
    validate_layout_json,
)


class DiplomaTemplateCreateForm(forms.Form):
    name = forms.CharField(
        max_length=160,
        strip=True,
        widget=forms.TextInput(
            attrs={"class": "input input-bordered w-full", "autofocus": True}
        ),
    )
    category = forms.CharField(
        max_length=80,
        strip=True,
        initial=DiplomaTemplate.DEFAULT_CATEGORY,
        widget=forms.TextInput(
            attrs={
                "class": "input input-bordered w-full",
                "placeholder": "Ex. SSM, PSI, ISCIR",
            }
        ),
    )
    description = forms.CharField(
        required=False,
        strip=True,
        widget=forms.Textarea(
            attrs={"class": "textarea textarea-bordered min-h-28 w-full", "rows": 4}
        ),
    )
    page_size = forms.ChoiceField(
        choices=DiplomaTemplate.PageSize.choices,
        initial=DiplomaTemplate.PageSize.A4,
        widget=forms.Select(attrs={"class": "select select-bordered w-full"}),
    )
    orientation = forms.ChoiceField(
        choices=DiplomaTemplate.Orientation.choices,
        initial=DiplomaTemplate.Orientation.PORTRAIT,
        widget=forms.Select(attrs={"class": "select select-bordered w-full"}),
    )

    def clean_name(self):
        return self.cleaned_data["name"].strip()

    def clean_category(self):
        return " ".join(self.cleaned_data["category"].split())


class DiplomaTemplateFilterForm(forms.Form):
    category = forms.ChoiceField(
        required=False,
        label="Categorie",
        widget=forms.Select(
            attrs={
                "class": "select select-bordered select-sm min-w-52",
                "aria-label": "Filtrează după categorie",
            }
        ),
    )

    def __init__(self, *args, categories=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].choices = [
            ("", "Toate categoriile"),
            *((category, category) for category in categories),
        ]


class DiplomaTemplateLayoutForm(forms.Form):
    layout_json = forms.CharField()

    def clean_layout_json(self):
        raw_layout = self.cleaned_data["layout_json"]
        if len(raw_layout.encode("utf-8")) > MAX_LAYOUT_JSON_BYTES:
            raise ValidationError("Layout-ul depășește limita de 256 KB.")
        try:
            payload = json.loads(
                raw_layout,
                parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)),
            )
        except (json.JSONDecodeError, ValueError) as exc:
            raise ValidationError("Layout-ul nu conține JSON valid.") from exc
        return validate_layout_json(payload)


class ParticipantFilteringSelect(forms.Select):
    def create_option(self, name, value, *args, **kwargs):
        option = super().create_option(name, value, *args, **kwargs)
        instance = getattr(value, "instance", None)
        if instance is not None:
            option["attrs"]["data-participant-list-id"] = str(
                instance.participant_list_id
            )
        return option


class ParticipantListChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        count = getattr(obj, "actual_participant_count", obj.participant_count)
        return f"{obj.name} ({count} participanți)"


class ParticipantChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.full_name} — {obj.certificate_number}"


class DiplomaTemplateChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.name} — {obj.page_size}, {obj.get_orientation_display()}"


class DiplomaGenerationSelectionForm(forms.Form):
    participant_list = ParticipantListChoiceField(
        label="Listă participanți",
        queryset=ParticipantList.objects.none(),
        empty_label="Selectează lista",
        widget=forms.Select(
            attrs={
                "class": "select select-bordered w-full",
                "data-generation-list": "",
            }
        ),
    )
    participant = ParticipantChoiceField(
        label="Participant",
        queryset=Participant.objects.none(),
        empty_label="Selectează participantul",
        widget=ParticipantFilteringSelect(
            attrs={
                "class": "select select-bordered w-full",
                "data-generation-participant": "",
            }
        ),
    )
    template = DiplomaTemplateChoiceField(
        label="Template diplomă",
        queryset=DiplomaTemplate.objects.none(),
        empty_label="Selectează template-ul",
        widget=forms.Select(attrs={"class": "select select-bordered w-full"}),
    )

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields["participant_list"].queryset = ParticipantList.objects.filter(
            owner=user
        )
        self.fields["participant"].queryset = Participant.objects.filter(
            owner=user,
            participant_list__owner=user,
        ).select_related("participant_list")
        self.fields["template"].queryset = DiplomaTemplate.objects.filter(owner=user)

    def clean(self):
        cleaned = super().clean()
        participant_list = cleaned.get("participant_list")
        participant = cleaned.get("participant")
        template = cleaned.get("template")
        participant_values = self.data.getlist("participant") if self.is_bound else []
        if len(participant_values) > 1:
            self.add_error("participant", "Selectează un singur participant.")
        if participant_list and participant:
            if participant.participant_list_id != participant_list.pk:
                self.add_error(
                    "participant",
                    "Participantul nu aparține listei selectate.",
                )
        if participant_list and participant_list.owner_id != self.user.pk:
            self.add_error("participant_list", "Lista selectată nu este disponibilă.")
        if participant and participant.owner_id != self.user.pk:
            self.add_error("participant", "Participantul selectat nu este disponibil.")
        if template and template.owner_id != self.user.pk:
            self.add_error("template", "Template-ul selectat nu este disponibil.")
        return cleaned


class BulkDiplomaGenerationForm(forms.Form):
    participant_list = ParticipantListChoiceField(
        label="Listă participanți",
        queryset=ParticipantList.objects.none(),
        empty_label="Selectează lista",
        widget=forms.Select(attrs={"class": "select select-bordered w-full"}),
    )
    template = DiplomaTemplateChoiceField(
        label="Template diplomă",
        queryset=DiplomaTemplate.objects.none(),
        empty_label="Selectează template-ul",
        widget=forms.Select(attrs={"class": "select select-bordered w-full"}),
    )

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields["participant_list"].queryset = (
            list_owned_participant_lists_with_counts(user)
        )
        self.fields["template"].queryset = list_owned_templates_for_generation(user)

    def clean_participant_list(self):
        participant_list = self.cleaned_data["participant_list"]
        if participant_list.owner_id != self.user.pk:
            raise ValidationError("Lista selectată nu este disponibilă.")
        participant_count = getattr(participant_list, "actual_participant_count", None)
        if participant_count is None:
            participant_count = participant_list.participants.count()
        if participant_count == 0:
            raise ValidationError("Lista selectată nu conține participanți.")
        return participant_list

    def clean_template(self):
        template = self.cleaned_data["template"]
        if template.owner_id != self.user.pk:
            raise ValidationError("Template-ul selectat nu este disponibil.")
        try:
            validate_layout_json(template.layout_json)
        except ValidationError as exc:
            raise ValidationError(
                "Template-ul selectat nu are un layout valid."
            ) from exc
        return template


class DiplomaGenerationHistoryFilterForm(forms.Form):
    participant_list = forms.ModelChoiceField(
        label="Listă",
        required=False,
        queryset=ParticipantList.objects.none(),
        empty_label="Toate listele",
        widget=forms.Select(attrs={"class": "select select-bordered select-sm w-full"}),
    )
    template = forms.ModelChoiceField(
        label="Template",
        required=False,
        queryset=DiplomaTemplate.objects.none(),
        empty_label="Toate template-urile",
        widget=forms.Select(attrs={"class": "select select-bordered select-sm w-full"}),
    )
    status = forms.ChoiceField(
        label="Status",
        required=False,
        choices=(("", "Toate statusurile"), *DiplomaGenerationBatch.Status.choices),
        widget=forms.Select(attrs={"class": "select select-bordered select-sm w-full"}),
    )
    date = forms.DateField(
        label="Data",
        required=False,
        widget=forms.DateInput(
            attrs={"class": "input input-bordered input-sm w-full", "type": "date"}
        ),
    )

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["participant_list"].queryset = (
            list_owned_participant_lists_with_counts(user)
        )
        self.fields["template"].queryset = list_owned_templates_for_generation(user)


class ParticipantListImportForm(forms.Form):
    list_name = forms.CharField(
        label="Numele listei",
        max_length=160,
        strip=True,
        error_messages={"required": "Numele listei este obligatoriu."},
        widget=forms.TextInput(
            attrs={"class": "input input-bordered w-full", "autofocus": True}
        ),
    )
    description = forms.CharField(
        label="Descriere",
        required=False,
        strip=True,
        widget=forms.Textarea(
            attrs={"class": "textarea textarea-bordered min-h-24 w-full", "rows": 3}
        ),
    )
    course_name = forms.CharField(
        label="Denumirea cursului",
        max_length=200,
        required=False,
        strip=True,
        widget=forms.TextInput(
            attrs={
                "class": "input input-bordered w-full",
                "placeholder": "Opțional, doar pentru afișare",
            }
        ),
    )
    source_file = forms.FileField(
        label="Fișier participanți",
        widget=forms.ClearableFileInput(
            attrs={
                "class": "file-input file-input-bordered file-input-primary w-full",
                "accept": ".csv,.xlsx",
            }
        ),
    )
    first_row_has_headers = forms.BooleanField(
        label="Primul rând conține denumirile coloanelor",
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={"class": "checkbox checkbox-primary checkbox-sm"}),
    )

    def clean_list_name(self):
        return " ".join(self.cleaned_data["list_name"].split())

    def clean_source_file(self):
        upload = self.cleaned_data["source_file"]
        extension = Path(upload.name).suffix.lower()
        if extension not in PARTICIPANT_UPLOAD_EXTENSIONS:
            raise ValidationError("Fișierul trebuie să fie în format CSV sau XLSX.")
        if upload.size > MAX_PARTICIPANT_UPLOAD_BYTES:
            raise ValidationError("Fișierul nu poate depăși 10 MB.")
        return upload


class ParticipantSheetSelectionForm(forms.Form):
    sheet_index = forms.ChoiceField(
        label="Foaia de importat",
        widget=forms.RadioSelect(attrs={"class": "radio radio-primary radio-sm"}),
    )

    def __init__(self, *args, sheets=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["sheet_index"].choices = [
            (
                str(index),
                f"{sheet['name']} — {len(sheet['source_rows'])} rânduri, "
                f"{len(sheet['columns'])} coloane",
            )
            for index, sheet in enumerate(sheets)
        ]

    def selected_index(self) -> int:
        return int(self.cleaned_data["sheet_index"])


class ParticipantColumnMappingForm(forms.Form):
    TARGET_FIELDS = (
        ("full_name", "Nume complet"),
        ("date_of_birth", "Data nașterii"),
        ("place_of_birth", "Locul nașterii"),
        ("certificate_number", "Număr certificat"),
    )

    def __init__(self, *args, columns=(), suggested_mapping=None, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [("", "Nu importa")]
        choices.extend(self.TARGET_FIELDS)
        suggested_mapping = suggested_mapping or {}
        suggested_by_column = {
            int(column_index): target_field
            for target_field, column_index in suggested_mapping.items()
        }
        for column in columns:
            column_index = int(column["index"])
            self.fields[f"column_{column_index}"] = forms.ChoiceField(
                label=column["label"],
                choices=choices,
                required=False,
                initial=suggested_by_column.get(column_index, ""),
                widget=forms.Select(
                    attrs={
                        "class": "select select-bordered w-full",
                        "data-mapping-select": "",
                    }
                ),
            )

    def clean(self):
        cleaned = super().clean()
        selected = [value for value in cleaned.values() if value]
        if len(selected) != len(set(selected)):
            raise ValidationError("Fiecare câmp din sistem poate fi asociat o singură dată.")
        required = {field for field, _ in self.TARGET_FIELDS}
        missing = required - set(selected)
        if missing:
            missing_labels = ", ".join(
                label for field, label in self.TARGET_FIELDS if field in missing
            )
            raise ValidationError(
                f"Asociază toate câmpurile obligatorii din sistem: {missing_labels}."
            )
        return cleaned

    def get_column_mapping(self):
        return {
            target_field: int(source_field.removeprefix("column_"))
            for source_field, target_field in self.cleaned_data.items()
            if target_field
        }
```

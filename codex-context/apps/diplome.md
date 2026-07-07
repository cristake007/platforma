# Django app: diplome

Migrations are excluded by default. Tests are included unless `--no-tests` is used.

## `apps/diplome/__init__.py`

Size: 1 B

```python

```

## `apps/diplome/admin.py`

Size: 3.6 KB

```python
from django.contrib import admin

from .models import (
    DiplomaGenerationBatch,
    DiplomaTemplate,
    GeneratedDiploma,
    Participant,
    ParticipantImportDraft,
    ParticipantList,
)


@admin.register(DiplomaTemplate)
class DiplomaTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "owner", "page_size", "orientation", "is_active", "updated_at")
    list_filter = ("category", "is_active", "page_size", "orientation", "updated_at")
    search_fields = (
        "name",
        "category",
        "description",
        "owner__username",
        "owner__first_name",
        "owner__last_name",
    )
    readonly_fields = ("id", "created_at", "updated_at")
    list_select_related = ("owner",)


@admin.register(ParticipantList)
class ParticipantListAdmin(admin.ModelAdmin):
    list_display = ("name", "course_name", "owner", "participant_count", "updated_at")
    search_fields = ("name", "course_name", "source_file_name", "owner__username")
    readonly_fields = ("id", "participant_count", "created_at", "updated_at")
    list_select_related = ("owner",)


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "certificate_number",
        "participant_list",
        "owner",
        "source_row",
    )
    search_fields = (
        "full_name",
        "certificate_number",
        "participant_list__name",
        "owner__username",
    )
    readonly_fields = ("id", "created_at", "updated_at")
    list_select_related = ("owner", "participant_list")


@admin.register(ParticipantImportDraft)
class ParticipantImportDraftAdmin(admin.ModelAdmin):
    list_display = ("list_name", "source_file_name", "owner", "created_at", "expires_at")
    search_fields = ("list_name", "source_file_name", "owner__username")
    readonly_fields = ("id", "created_at")
    list_select_related = ("owner",)


@admin.register(GeneratedDiploma)
class GeneratedDiplomaAdmin(admin.ModelAdmin):
    list_display = (
        "participant_name",
        "certificate_number",
        "participant_list_display_name",
        "template_display_name",
        "owner",
        "created_at",
    )
    search_fields = (
        "participant_name",
        "certificate_number",
        "participant_list_name",
        "template_name",
        "participant_list__name",
        "template__name",
        "owner__username",
    )
    readonly_fields = (
        "id",
        "certificate_number",
        "participant_name",
        "participant_list_name",
        "template_name",
        "pdf_file",
        "created_at",
        "updated_at",
    )
    list_select_related = ("owner", "participant_list", "participant", "template", "batch")


@admin.register(DiplomaGenerationBatch)
class DiplomaGenerationBatchAdmin(admin.ModelAdmin):
    list_display = (
        "participant_list_display_name",
        "template_display_name",
        "owner",
        "status",
        "success_count",
        "failed_count",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = (
        "participant_list_name",
        "template_name",
        "participant_list__name",
        "template__name",
        "owner__username",
    )
    readonly_fields = (
        "id",
        "status",
        "total_count",
        "success_count",
        "failed_count",
        "participant_list_name",
        "template_name",
        "output_folder",
        "error_summary",
        "created_at",
        "updated_at",
        "started_at",
        "completed_at",
    )
    list_select_related = ("owner", "participant_list", "template")
```

## `apps/diplome/AGENTS.md`

Size: 3.1 KB

````markdown
# Diplome App Instructions

## Scope and workflows

This app owns diploma templates and layout JSON, participant-list import, single/bulk PDF generation, downloads, and generation history.

It integrates with `media_library` for owned layout assets.

## Read before editing

- Root `AGENTS.md`.
- `coding-standards.md`.
- `frontend.md` for UI/template work.
- This file.
- Only the files for the selected workflow.

Use `codex-context/apps/diplome.md` only when a path is unknown.

Do not open editor, participant, generation, and history files together unless the change crosses those contracts.

## Minimal routing

- Template list/create/editor/preview: `urls.py`, `views.py`, `forms.py`, `services.py`, `validators.py`, exact template/static file, then `tests.py`.
- Participant CSV/XLSX import and mapping: `forms.py`, `services.py`, `views.py`, exact participant template/JavaScript, then `tests_participants.py`.
- Single generation/download: `forms.py`, `selectors.py`, `services.py`, `pdf_renderer.py`, relevant generation templates, then `tests_generation.py`.
- Bulk generation/history/ZIP: `models.py`, `selectors.py`, `services.py`, relevant batch/history templates, then `tests_bulk_generation.py`.
- Model changes: `models.py`, affected service/selector/tests, then only relevant migration history.

## Domain contracts

- Templates, participant records, drafts, generated diplomas, and batches are owner-scoped.
- Cross-owner access returns 404 or a validation error appropriate to the existing endpoint.
- `validators.py` is the canonical layout JSON contract.
- Keep browser rendering, PDF rendering, form validation, and stored layout versions compatible.
- Use `services.py` for transactional imports, template mutation, generation, ZIP creation, and history snapshots.
- Views orchestrate HTTP only.
- Preserve history snapshots when source participants, lists, or templates are deleted.
- Validate participant membership against the selected owned list.
- Validate every media asset through `media_library` ownership services.
- Keep state-changing endpoints POST-only with CSRF protection.
- Downloads must use owned selectors and safe filenames.

## Reuse and UI standards

- Reuse existing form, participant, table, history, and message partials before adding markup.
- Standard pages extend `layouts/base.html` and use shared semantic tokens.
- Use sharp bordered operational screens for list/import/history pages.
- Avoid rounded card-heavy ordinary pages.
- `template_editor.css` may implement editor geometry.
- Editor chrome must consume global semantic variables.
- Diploma canvas element colors are user-authored document data and may remain literal/stored values.
- Keep `template_renderer.js` behavior compatible with preview and editor consumers.
- Server validation remains authoritative.

## Focused checks

```powershell
python manage.py test apps.diplome.tests
python manage.py test apps.diplome.tests_participants
python manage.py test apps.diplome.tests_generation
python manage.py test apps.diplome.tests_bulk_generation
```

Run only the command matching the changed workflow unless the contract crosses them.
````

## `apps/diplome/apps.py`

Size: 180 B

```python
from django.apps import AppConfig


class DiplomeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.diplome"
    verbose_name = "Diplome"
```

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

## `apps/diplome/models.py`

Size: 15.0 KB

```python
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from .validators import validate_layout_json


def generated_diploma_upload_to(instance, _filename: str) -> str:
    if instance.batch_id:
        return f"{instance.batch.output_folder}/{_filename}"
    return (
        f"diplomas/{instance.owner_id}/{instance.participant_list_id}/"
        f"{instance.pk}.pdf"
    )


class DiplomaTemplate(models.Model):
    DEFAULT_CATEGORY = "General"

    class PageSize(models.TextChoices):
        A4 = "A4", "A4"

    class Orientation(models.TextChoices):
        LANDSCAPE = "landscape", "Peisaj"
        PORTRAIT = "portrait", "Portret"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="diploma_templates",
    )
    name = models.CharField(max_length=160)
    category = models.CharField(max_length=80, default=DEFAULT_CATEGORY)
    description = models.TextField(blank=True)
    page_size = models.CharField(max_length=16, choices=PageSize.choices, default=PageSize.A4)
    orientation = models.CharField(
        max_length=16,
        choices=Orientation.choices,
        default=Orientation.LANDSCAPE,
    )
    page_width_mm = models.PositiveSmallIntegerField(default=297)
    page_height_mm = models.PositiveSmallIntegerField(default=210)
    grid_size_mm = models.PositiveSmallIntegerField(default=1)
    major_grid_size_mm = models.PositiveSmallIntegerField(default=10)
    layout_json = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-updated_at", "name")
        indexes = [
            models.Index(fields=("owner", "name"), name="dipl_tmpl_owner_name"),
            models.Index(
                fields=("owner", "is_active", "-updated_at"),
                name="dipl_tmpl_owner_act_upd",
            ),
            models.Index(
                fields=("owner", "category", "-updated_at"),
                name="dipl_tmpl_owner_cat_upd",
            ),
        ]
        constraints = [
            models.CheckConstraint(condition=Q(page_width_mm__gt=0), name="dipl_tmpl_width_mm_gt_0"),
            models.CheckConstraint(condition=Q(page_height_mm__gt=0), name="dipl_tmpl_height_mm_gt_0"),
            models.CheckConstraint(condition=Q(grid_size_mm__gt=0), name="dipl_tmpl_grid_mm_gt_0"),
            models.CheckConstraint(condition=Q(major_grid_size_mm__gt=0), name="dipl_tmpl_major_grid_gt_0"),
        ]

    def clean(self):
        super().clean()
        normalized_category = " ".join((self.category or "").split())
        if not normalized_category:
            raise ValidationError({"category": "Categoria este obligatorie."})
        self.category = normalized_category
        if not self.layout_json:
            return
        normalized = validate_layout_json(self.layout_json)
        page = normalized["page"]
        mismatches = (
            page["size"] != self.page_size,
            page["orientation"] != self.orientation,
            page["width_mm"] != self.page_width_mm,
            page["height_mm"] != self.page_height_mm,
            page["grid_mm"] != self.grid_size_mm,
            page["major_grid_mm"] != self.major_grid_size_mm,
        )
        if any(mismatches):
            raise ValidationError({"layout_json": "Metadatele paginii nu corespund template-ului."})
        self.layout_json = normalized

    def __str__(self) -> str:
        return f"{self.name} — {self.owner}"


class ParticipantList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="participant_lists",
    )
    name = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    course_name = models.CharField(max_length=200, blank=True)
    source_file_name = models.CharField(max_length=255)
    participant_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-updated_at", "name")
        indexes = [
            models.Index(
                fields=("owner", "-updated_at"),
                name="dipl_plist_owner_upd",
            ),
        ]

    def __str__(self) -> str:
        return self.name


class Participant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="diploma_participants",
    )
    participant_list = models.ForeignKey(
        ParticipantList,
        on_delete=models.CASCADE,
        related_name="participants",
    )
    full_name = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=200)
    certificate_number = models.CharField(max_length=100)
    source_row = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("source_row", "full_name")
        indexes = [
            models.Index(
                fields=("participant_list", "source_row"),
                name="dipl_part_list_row",
            ),
            models.Index(
                fields=("owner", "certificate_number"),
                name="dipl_part_owner_cert",
            ),
        ]

    def clean(self):
        super().clean()
        if self.participant_list_id and self.owner_id != self.participant_list.owner_id:
            raise ValidationError(
                {"participant_list": "Lista de participanți trebuie să aparțină aceluiași utilizator."}
            )

    def __str__(self) -> str:
        return self.full_name


class ParticipantImportDraft(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="participant_import_drafts",
    )
    list_name = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    course_name = models.CharField(max_length=200, blank=True)
    source_file_name = models.CharField(max_length=255)
    source_sheets_json = models.JSONField(default=list)
    source_columns_json = models.JSONField(default=list)
    source_rows_json = models.JSONField(default=list)
    column_mapping_json = models.JSONField(default=dict)
    mapping_confirmed = models.BooleanField(default=False)
    valid_rows_json = models.JSONField(default=list)
    invalid_rows_json = models.JSONField(default=list)
    warnings_json = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(db_index=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(
                fields=("owner", "expires_at"),
                name="dipl_pdraft_owner_exp",
            ),
        ]

    def __str__(self) -> str:
        return self.list_name


class DiplomaGenerationBatch(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "În așteptare"
        RUNNING = "running", "În curs"
        COMPLETED = "completed", "Finalizat"
        COMPLETED_WITH_ERRORS = "completed_with_errors", "Finalizat cu erori"
        FAILED = "failed", "Eșuat"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="diploma_generation_batches",
    )
    participant_list = models.ForeignKey(
        ParticipantList,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="diploma_generation_batches",
    )
    template = models.ForeignKey(
        DiplomaTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="diploma_generation_batches",
    )
    participant_list_name = models.CharField(max_length=160, default="")
    template_name = models.CharField(max_length=160, default="")
    status = models.CharField(
        max_length=24,
        choices=Status.choices,
        default=Status.PENDING,
    )
    total_count = models.PositiveIntegerField(default=0)
    success_count = models.PositiveIntegerField(default=0)
    failed_count = models.PositiveIntegerField(default=0)
    output_folder = models.CharField(max_length=500)
    error_summary = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(
                fields=("owner", "-created_at"),
                name="dipl_batch_owner_created",
            ),
            models.Index(
                fields=("participant_list", "-created_at"),
                name="dipl_batch_list_created",
            ),
            models.Index(
                fields=("template", "-created_at"),
                name="dipl_batch_tmpl_created",
            ),
            models.Index(
                fields=("owner", "status", "-created_at"),
                name="dipl_batch_owner_st_created",
            ),
        ]

    def clean(self):
        super().clean()
        errors = {}
        if self.participant_list_id:
            if self.owner_id != self.participant_list.owner_id:
                errors["participant_list"] = "Lista trebuie să aparțină aceluiași utilizator."
            self.participant_list_name = self.participant_list_name or self.participant_list.name
        if self.template_id:
            if self.owner_id != self.template.owner_id:
                errors["template"] = "Template-ul trebuie să aparțină aceluiași utilizator."
            self.template_name = self.template_name or self.template.name
        if errors:
            raise ValidationError(errors)

    def __str__(self) -> str:
        return f"{self.participant_list_display_name} — {self.get_status_display()}"

    @property
    def participant_list_display_name(self) -> str:
        return self.participant_list_name or getattr(self.participant_list, "name", "Listă ștearsă")

    @property
    def template_display_name(self) -> str:
        return self.template_name or getattr(self.template, "name", "Template șters")


class GeneratedDiploma(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="generated_diplomas",
    )
    participant_list = models.ForeignKey(
        ParticipantList,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="generated_diplomas",
    )
    participant = models.ForeignKey(
        Participant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="generated_diplomas",
    )
    template = models.ForeignKey(
        DiplomaTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="generated_diplomas",
    )
    batch = models.ForeignKey(
        DiplomaGenerationBatch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="generated_diplomas",
    )
    certificate_number = models.CharField(max_length=100)
    participant_name = models.CharField(max_length=200)
    participant_list_name = models.CharField(max_length=160, default="")
    template_name = models.CharField(max_length=160, default="")
    pdf_file = models.FileField(upload_to=generated_diploma_upload_to, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(
                fields=("owner", "-created_at"),
                name="dipl_gen_owner_created",
            ),
            models.Index(
                fields=("batch", "participant_name"),
                name="dipl_gen_batch_name",
            ),
            models.Index(
                fields=("participant_list", "participant_name"),
                name="dipl_gen_list_name",
            ),
            models.Index(
                fields=("participant", "-created_at"),
                name="dipl_gen_part_created",
            ),
            models.Index(
                fields=("template", "created_at"),
                name="dipl_gen_tmpl_created",
            ),
        ]

    def clean(self):
        super().clean()
        errors = {}
        if self.participant_list_id:
            if self.owner_id != self.participant_list.owner_id:
                errors["participant_list"] = "Lista trebuie să aparțină aceluiași utilizator."
            self.participant_list_name = self.participant_list_name or self.participant_list.name
        if self.participant_id:
            if self.owner_id != self.participant.owner_id:
                errors["participant"] = "Participantul trebuie să aparțină aceluiași utilizator."
            elif (
                self.participant_list_id
                and self.participant.participant_list_id != self.participant_list_id
            ):
                errors["participant"] = "Participantul nu aparține listei selectate."
        if self.template_id:
            if self.owner_id != self.template.owner_id:
                errors["template"] = "Template-ul trebuie să aparțină aceluiași utilizator."
            self.template_name = self.template_name or self.template.name
        if self.batch_id:
            if self.owner_id != self.batch.owner_id:
                errors["batch"] = "Lotul trebuie să aparțină aceluiași utilizator."
            elif (
                self.participant_list_id
                and self.batch.participant_list_id != self.participant_list_id
            ):
                errors["batch"] = "Lotul nu corespunde listei selectate."
            elif self.template_id and self.batch.template_id != self.template_id:
                errors["batch"] = "Lotul nu corespunde template-ului selectat."
        if errors:
            raise ValidationError(errors)

    def __str__(self) -> str:
        return f"{self.participant_name} — {self.certificate_number}"

    @property
    def participant_list_display_name(self) -> str:
        return self.participant_list_name or getattr(self.participant_list, "name", "Listă ștearsă")

    @property
    def template_display_name(self) -> str:
        return self.template_name or getattr(self.template, "name", "Template șters")
```

## `apps/diplome/pdf_renderer.py`

Size: 18.1 KB

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

## `apps/diplome/selectors.py`

Size: 4.7 KB

```python
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import (
    DiplomaGenerationBatch,
    DiplomaTemplate,
    GeneratedDiploma,
    Participant,
    ParticipantImportDraft,
    ParticipantList,
)


def list_owned_templates(*, user, category=""):
    queryset = DiplomaTemplate.objects.filter(owner=user)
    if category:
        queryset = queryset.filter(category=category)
    return queryset.only(
        "id",
        "name",
        "category",
        "description",
        "page_size",
        "orientation",
        "is_active",
        "created_at",
        "updated_at",
    )


def list_owned_template_categories(*, user):
    return (
        DiplomaTemplate.objects.filter(owner=user)
        .exclude(category="")
        .order_by("category")
        .values_list("category", flat=True)
        .distinct()
    )


def get_owned_template(*, user, template_id) -> DiplomaTemplate:
    return get_object_or_404(DiplomaTemplate, pk=template_id, owner=user)


def get_owned_template_for_update(*, user, template_id) -> DiplomaTemplate:
    return get_object_or_404(
        DiplomaTemplate.objects.select_for_update(),
        pk=template_id,
        owner=user,
    )


def list_owned_participant_lists(*, user):
    return ParticipantList.objects.filter(owner=user).only(
        "id",
        "name",
        "description",
        "course_name",
        "source_file_name",
        "participant_count",
        "created_at",
        "updated_at",
    )


def get_owned_participant_list(*, user, participant_list_id) -> ParticipantList:
    return get_object_or_404(
        ParticipantList,
        pk=participant_list_id,
        owner=user,
    )


def list_owned_participants(*, user, participant_list):
    return participant_list.participants.filter(owner=user)


def list_owned_participants_for_list(*, user, participant_list_id):
    return Participant.objects.filter(
        owner=user,
        participant_list_id=participant_list_id,
        participant_list__owner=user,
    ).select_related("participant_list")


def get_owned_participant(*, user, participant_id) -> Participant:
    return get_object_or_404(
        Participant.objects.select_related("participant_list"),
        pk=participant_id,
        owner=user,
        participant_list__owner=user,
    )


def get_owned_participant_for_update(*, user, participant_id) -> Participant:
    return get_object_or_404(
        Participant.objects.select_for_update().select_related("participant_list"),
        pk=participant_id,
        owner=user,
        participant_list__owner=user,
    )


def get_owned_participant_list_for_update(*, user, participant_list_id) -> ParticipantList:
    return get_object_or_404(
        ParticipantList.objects.select_for_update(),
        pk=participant_list_id,
        owner=user,
    )


def get_owned_import_draft(*, user, draft_id) -> ParticipantImportDraft:
    return get_object_or_404(
        ParticipantImportDraft,
        pk=draft_id,
        owner=user,
        expires_at__gt=timezone.now(),
    )


def get_owned_import_draft_for_update(*, user, draft_id) -> ParticipantImportDraft:
    return get_object_or_404(
        ParticipantImportDraft.objects.select_for_update(),
        pk=draft_id,
        owner=user,
        expires_at__gt=timezone.now(),
    )


def get_owned_generated_diploma(*, user, generated_diploma_id) -> GeneratedDiploma:
    return get_object_or_404(
        GeneratedDiploma.objects.select_related(
            "batch",
            "participant_list",
            "participant",
            "template",
        ),
        pk=generated_diploma_id,
        owner=user,
    )


def list_owned_generation_batches(user):
    return DiplomaGenerationBatch.objects.filter(owner=user).select_related(
        "participant_list",
        "template",
    )


def get_owned_generation_batch(user, batch_id) -> DiplomaGenerationBatch:
    return get_object_or_404(
        DiplomaGenerationBatch.objects.select_related(
            "participant_list",
            "template",
        ),
        pk=batch_id,
        owner=user,
    )


def list_generated_diplomas_for_batch(user, batch_id):
    return GeneratedDiploma.objects.filter(
        owner=user,
        batch_id=batch_id,
        batch__owner=user,
    ).select_related(
        "participant",
        "participant_list",
        "template",
        "batch",
    ).order_by("participant_name", "certificate_number")


def list_owned_participant_lists_with_counts(user):
    return (
        ParticipantList.objects.filter(owner=user)
        .annotate(actual_participant_count=Count("participants"))
        .order_by("-updated_at", "name")
    )


def list_owned_templates_for_generation(user):
    return DiplomaTemplate.objects.filter(owner=user).order_by("name")
```

## `apps/diplome/services.py`

Size: 39.2 KB

```python
import csv
import io
import re
import unicodedata
import uuid
from copy import deepcopy
from datetime import date, datetime, timedelta
from io import BytesIO
from pathlib import Path
from zipfile import BadZipFile, ZIP_DEFLATED, ZipFile

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import transaction
from django.http import Http404, HttpResponse
from django.utils import timezone

from apps.media_library.services import (
    require_owned_layout_assets,
    serialize_media_assets,
)
from django.utils.text import slugify
from openpyxl import load_workbook
from openpyxl.utils.exceptions import InvalidFileException

from .models import (
    DiplomaGenerationBatch,
    DiplomaTemplate,
    GeneratedDiploma,
    Participant,
    ParticipantImportDraft,
    ParticipantList,
)
from .pdf_renderer import render_diploma_pdf
from .selectors import (
    get_owned_generation_batch,
    get_owned_generated_diploma,
    get_owned_import_draft_for_update,
    get_owned_participant,
    get_owned_participant_for_update,
    get_owned_participant_list,
    get_owned_participant_list_for_update,
    get_owned_template,
    get_owned_template_for_update,
    list_generated_diplomas_for_batch,
    list_owned_generation_batches,
)
from .validators import MAX_PARTICIPANT_ROWS, validate_layout_json


SAMPLE_PARTICIPANT = {
    "full_name": "Andrei Popescu",
    "date_of_birth": "12.04.1990",
    "place_of_birth": "Brașov",
    "certificate_number": "TTK-2026-001",
}

PARTICIPANT_DATE_ERROR = "Data nașterii trebuie să fie în format DD.MM.YYYY."
PARTICIPANT_COLUMNS = {
    "full_name": {"full_name", "nume complet", "nume si prenume", "nume și prenume"},
    "date_of_birth": {"date_of_birth", "data nasterii", "data nașterii"},
    "place_of_birth": {"place_of_birth", "locul nasterii", "locul nașterii"},
    "certificate_number": {
        "certificate_number",
        "numar certificat",
        "număr certificat",
    },
}


def _typography(*, size: int, color: str = "#164194", bold: bool = False, align: str = "center", font: str = "Lora") -> dict:
    return {
        "fontFamily": font,
        "fontSize": size,
        "bold": bold,
        "italic": False,
        "underline": False,
        "color": color,
        "align": align,
        "lineHeight": 1.18,
        "letterSpacing": 0,
        "textTransform": "none",
    }


def _base_element(*, element_id: str, element_type: str, label: str, x_mm: int, y_mm: int, width_mm: int, height_mm: int, z_index: int, style: dict) -> dict:
    return {
        "id": element_id,
        "type": element_type,
        "label": label,
        "x_mm": x_mm,
        "y_mm": y_mm,
        "width_mm": width_mm,
        "height_mm": height_mm,
        "rotation": 0,
        "zIndex": z_index,
        "locked": False,
        "visible": True,
        "style": style,
    }


def build_blank_layout(*, page_size: str = "A4", orientation: str = "landscape") -> dict:
    width_mm, height_mm = ((297, 210) if orientation == "landscape" else (210, 297))
    return validate_layout_json({
        "version": 2,
        "page": {
            "size": page_size,
            "orientation": orientation,
            "width_mm": width_mm,
            "height_mm": height_mm,
            "grid_mm": 1,
            "major_grid_mm": 10,
            "background": None,
        },
        "elements": [],
    })


def build_default_layout(*, page_size: str = "A4", orientation: str = "landscape") -> dict:
    width_mm, height_mm = ((297, 210) if orientation == "landscape" else (210, 297))

    def sx(value: int) -> int:
        return max(1, round(value * width_mm / 297))

    def sy(value: int) -> int:
        return max(1, round(value * height_mm / 210))

    elements = [
        {
            **_base_element(element_id="title", element_type="text", label="Titlu", x_mm=sx(53), y_mm=sy(28), width_mm=sx(191), height_mm=sy(19), z_index=10, style=_typography(size=46, bold=True)),
            "text": "DIPLOMĂ DE ABSOLVIRE",
        },
        {
            **_base_element(element_id="intro", element_type="text", label="Introducere", x_mm=sx(85), y_mm=sy(54), width_mm=sx(127), height_mm=sy(9), z_index=20, style=_typography(size=16, color="#304253", font="Inter")),
            "text": "Se acordă domnului / doamnei",
        },
        {
            **_base_element(element_id="full_name", element_type="variable", label="Nume complet", x_mm=sx(69), y_mm=sy(66), width_mm=sx(159), height_mm=sy(18), z_index=30, style=_typography(size=38, bold=True)),
            "variable": "full_name",
            "placeholder": "Nume complet",
        },
        {
            **_base_element(element_id="date_of_birth", element_type="variable", label="Data nașterii", x_mm=sx(66), y_mm=sy(91), width_mm=sx(66), height_mm=sy(10), z_index=40, style=_typography(size=16, color="#304253", font="Inter")),
            "variable": "date_of_birth",
            "placeholder": "Data nașterii",
        },
        {
            **_base_element(element_id="place_of_birth", element_type="variable", label="Locul nașterii", x_mm=sx(165), y_mm=sy(91), width_mm=sx(66), height_mm=sy(10), z_index=50, style=_typography(size=16, color="#304253", font="Inter")),
            "variable": "place_of_birth",
            "placeholder": "Locul nașterii",
        },
        {
            **_base_element(element_id="certificate_number", element_type="variable", label="Număr certificat", x_mm=sx(106), y_mm=sy(106), width_mm=sx(85), height_mm=sy(10), z_index=60, style=_typography(size=16, color="#304253", bold=True, font="Inter")),
            "variable": "certificate_number",
            "placeholder": "Număr certificat",
        },
        {
            **_base_element(
                element_id="course_table",
                element_type="table",
                label="Tabel curs",
                x_mm=sx(48),
                y_mm=sy(128),
                width_mm=sx(201),
                height_mm=sy(29),
                z_index=70,
                style={
                    "fontFamily": "Inter",
                    "fontSize": 14,
                    "bold": False,
                    "color": "#304253",
                    "align": "center",
                    "borderColor": "#164194",
                    "headerBackground": "#edf3f9",
                },
            ),
            "columns": ["Denumirea cursului", "Cod curs", "Durată"],
            "rows": [["Inspector SSM", "SSM-01", "80 ore"]],
        },
        {
            **_base_element(element_id="signature_left", element_type="text", label="Semnătură director", x_mm=sx(42), y_mm=sy(173), width_mm=sx(69), height_mm=sy(11), z_index=80, style=_typography(size=14, color="#304253", bold=True, font="Inter")),
            "text": "DIRECTOR GENERAL",
        },
        {
            **_base_element(element_id="signature_right", element_type="text", label="Semnătură responsabil", x_mm=sx(186), y_mm=sy(173), width_mm=sx(69), height_mm=sy(11), z_index=90, style=_typography(size=14, color="#304253", bold=True, font="Inter")),
            "text": "RESPONSABIL CURS",
        },
    ]
    return validate_layout_json({
        "version": 2,
        "page": {
            "size": page_size,
            "orientation": orientation,
            "width_mm": width_mm,
            "height_mm": height_mm,
            "grid_mm": 1,
            "major_grid_mm": 10,
            "background": None,
        },
        "elements": elements,
    })


def create_diploma_template(*, owner, data: dict) -> DiplomaTemplate:
    layout = build_blank_layout(page_size=data["page_size"], orientation=data["orientation"])
    template = DiplomaTemplate(
        owner=owner,
        name=data["name"],
        category=data.get("category", DiplomaTemplate.DEFAULT_CATEGORY),
        description=data.get("description", ""),
        page_size=data["page_size"],
        orientation=data["orientation"],
        page_width_mm=layout["page"]["width_mm"],
        page_height_mm=layout["page"]["height_mm"],
        grid_size_mm=layout["page"]["grid_mm"],
        major_grid_size_mm=layout["page"]["major_grid_mm"],
        layout_json=layout,
    )
    template.full_clean()
    template.save()
    return template


def update_diploma_template_layout(*, owner, template_id, layout: dict) -> DiplomaTemplate:
    normalized = validate_layout_json(layout)
    with transaction.atomic():
        template = get_owned_template_for_update(user=owner, template_id=template_id)
        require_owned_layout_assets(owner=owner, layout=normalized, for_update=True)
        template.layout_json = normalized
        template.full_clean()
        template.save(update_fields=("layout_json", "updated_at"))
    return template


def delete_diploma_template(*, owner, template_id) -> None:
    with transaction.atomic():
        template = get_owned_template_for_update(user=owner, template_id=template_id)
        template.delete()


def build_preview_data() -> dict:
    return deepcopy(SAMPLE_PARTICIPANT)


def _normalize_header(value) -> str:
    text = " ".join(str(value or "").strip().lower().replace("_", " ").split())
    return "".join(
        character
        for character in unicodedata.normalize("NFKD", text)
        if not unicodedata.combining(character)
    )


def _suggest_participant_mapping(headers) -> dict[str, int]:
    aliases = {
        field: {_normalize_header(alias) for alias in values}
        for field, values in PARTICIPANT_COLUMNS.items()
    }
    suggestions = {}
    for field, accepted in aliases.items():
        matches = [
            index
            for index, header in enumerate(headers)
            if _normalize_header(header) in accepted
        ]
        if len(matches) == 1:
            suggestions[field] = matches[0]
    return suggestions


def _strict_date(value) -> tuple[date, str]:
    if isinstance(value, datetime):
        value = value.date()
    if isinstance(value, date):
        return value, value.strftime("%d.%m.%Y")

    text = str(value or "").strip()
    if not re.fullmatch(r"\d{2}\.\d{2}\.\d{4}", text):
        raise ValidationError(PARTICIPANT_DATE_ERROR)
    try:
        parsed = datetime.strptime(text, "%d.%m.%Y").date()
    except ValueError as exc:
        raise ValidationError(PARTICIPANT_DATE_ERROR) from exc
    if parsed.strftime("%d.%m.%Y") != text:
        raise ValidationError(PARTICIPANT_DATE_ERROR)
    return parsed, text


def _display_cell(value) -> str:
    if isinstance(value, datetime):
        return value.strftime("%d.%m.%Y")
    if isinstance(value, date):
        return value.strftime("%d.%m.%Y")
    return str(value or "").strip()


def _validate_participant_row(*, values, column_mapping, source_row):
    raw = {
        field: values[index] if index < len(values) else None
        for field, index in column_mapping.items()
    }
    display = {field: _display_cell(value) for field, value in raw.items()}
    errors = []

    limits = {
        "full_name": (200, "Numele complet"),
        "place_of_birth": (200, "Locul nașterii"),
        "certificate_number": (100, "Numărul certificatului"),
    }
    for field, (max_length, label) in limits.items():
        if not display[field]:
            errors.append(f"{label} este obligatoriu.")
        elif len(display[field]) > max_length:
            errors.append(f"{label} poate avea cel mult {max_length} de caractere.")

    try:
        _, normalized_date = _strict_date(raw["date_of_birth"])
        display["date_of_birth"] = normalized_date
    except ValidationError:
        errors.append(PARTICIPANT_DATE_ERROR)

    row = {"source_row": source_row, **display}
    if errors:
        return None, {**row, "errors": errors}
    return row, None


def _parse_csv_table(content: bytes):
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValidationError("Fișierul CSV trebuie să fie codificat UTF-8.") from exc
    try:
        dialect = csv.Sniffer().sniff(text[:8192], delimiters=",;\t")
        delimiter = dialect.delimiter
    except csv.Error:
        delimiter = ";"
    rows = list(csv.reader(io.StringIO(text, newline=""), delimiter=delimiter))
    if not rows:
        raise ValidationError("Fișierul nu conține niciun rând.")
    return [
        (
            row_number,
            values,
            [{"is_excel_date": False, "number_format": ""} for _ in values],
        )
        for row_number, values in enumerate(rows, start=1)
    ]


def _parse_xlsx_tables(content: bytes, *, first_row_has_headers: bool):
    try:
        workbook = load_workbook(io.BytesIO(content), read_only=True, data_only=True)
    except (BadZipFile, InvalidFileException, OSError, ValueError) as exc:
        raise ValidationError("Fișierul XLSX nu poate fi citit.") from exc
    try:
        worksheet_tables = []
        for worksheet in workbook.worksheets:
            if worksheet.sheet_state != "visible":
                continue
            parsed_rows = []
            for row_number, cells in enumerate(worksheet.iter_rows(), start=1):
                values = [cell.value for cell in cells]
                metadata = [
                    {
                        "is_excel_date": isinstance(cell.value, (date, datetime)),
                        "number_format": str(cell.number_format or ""),
                    }
                    for cell in cells
                ]
                while values and not _display_cell(values[-1]):
                    values.pop()
                    metadata.pop()
                if any(_display_cell(value) for value in values):
                    parsed_rows.append((row_number, values, metadata))
            has_enough_rows = not first_row_has_headers or len(parsed_rows) > 1
            if (
                parsed_rows
                and has_enough_rows
                and max(len(values) for _, values, _ in parsed_rows)
                >= len(PARTICIPANT_COLUMNS)
            ):
                worksheet_tables.append((worksheet.title, parsed_rows))

        if not worksheet_tables:
            raise ValidationError(
                "Fișierul XLSX nu conține nicio foaie cu cel puțin patru coloane."
            )

        return worksheet_tables
    finally:
        workbook.close()


def _participant_upload_tables(*, upload, first_row_has_headers: bool):
    content = upload.read()
    extension = Path(upload.name).suffix.lower()
    if extension == ".csv":
        return [("", _parse_csv_table(content))]
    elif extension == ".xlsx":
        return _parse_xlsx_tables(
            content,
            first_row_has_headers=first_row_has_headers,
        )
    raise ValidationError("Fișierul trebuie să fie în format CSV sau XLSX.")


def _discover_participant_table(*, table_rows, first_row_has_headers: bool) -> dict:
    table_rows = [
        row for row in table_rows if any(_display_cell(value) for value in row[1])
    ]
    if not table_rows:
        raise ValidationError("Fișierul nu conține niciun rând cu date.")

    header_values = table_rows[0][1] if first_row_has_headers else []
    data_rows = table_rows[1:] if first_row_has_headers else table_rows
    if not data_rows:
        raise ValidationError("Fișierul nu conține rânduri de participanți.")
    if len(data_rows) > MAX_PARTICIPANT_ROWS:
        raise ValidationError(
            f"Fișierul poate conține cel mult {MAX_PARTICIPANT_ROWS} de participanți."
        )

    column_count = max(len(values) for _, values, _ in table_rows)
    if column_count < len(PARTICIPANT_COLUMNS):
        raise ValidationError("Fișierul trebuie să conțină cel puțin patru coloane.")

    columns = []
    for index in range(column_count):
        label = _display_cell(header_values[index]) if index < len(header_values) else ""
        if not label:
            label = f"Coloana {index + 1}"
        samples = []
        for _, values, _ in data_rows:
            sample = _display_cell(values[index]) if index < len(values) else ""
            if sample and sample not in samples:
                samples.append(sample)
            if len(samples) == 2:
                break
        sample_text = ", ".join(samples)
        display_label = f"{label} — ex. {sample_text}" if sample_text else label
        columns.append(
            {
                "index": index,
                "label": label,
                "display_label": display_label,
                "samples": samples,
            }
        )

    source_rows = []
    for source_row, values, metadata in data_rows:
        source_rows.append(
            {
                "source_row": source_row,
                "values": [_display_cell(value) for value in values],
                "metadata": metadata,
            }
        )
    return {
        "columns": columns,
        "source_rows": source_rows,
        "suggested_mapping": (
            _suggest_participant_mapping(header_values)
            if first_row_has_headers
            else {}
        ),
    }


def discover_participant_upload(
    *,
    upload,
    first_row_has_headers: bool,
    worksheet_name: str | None = None,
) -> dict:
    tables = _participant_upload_tables(
        upload=upload,
        first_row_has_headers=first_row_has_headers,
    )
    if worksheet_name is not None:
        tables = [table for table in tables if table[0] == worksheet_name]
        if not tables:
            raise ValidationError("Foaia XLSX selectată nu este disponibilă.")
    elif len(tables) > 1:
        raise ValidationError("Selectează foaia XLSX care trebuie importată.")
    _, table_rows = tables[0]
    return _discover_participant_table(
        table_rows=table_rows,
        first_row_has_headers=first_row_has_headers,
    )


def validate_participant_mapping(*, source_rows, column_mapping) -> dict:
    expected_fields = set(PARTICIPANT_COLUMNS)
    if set(column_mapping) != expected_fields:
        raise ValidationError("Toate cele patru câmpuri trebuie asociate unei coloane.")
    try:
        normalized_mapping = {
            field: int(index) for field, index in column_mapping.items()
        }
    except (TypeError, ValueError) as exc:
        raise ValidationError("Asocierea coloanelor nu este validă.") from exc
    if len(set(normalized_mapping.values())) != len(normalized_mapping):
        raise ValidationError("Fiecare câmp trebuie asociat unei coloane diferite.")

    valid_rows = []
    invalid_rows = []
    warnings = []
    seen_certificates = set()
    for source in source_rows:
        values = source["values"]
        valid, invalid = _validate_participant_row(
            values=values,
            column_mapping=normalized_mapping,
            source_row=source["source_row"],
        )
        if invalid:
            invalid_rows.append(invalid)
            continue
        certificate = valid["certificate_number"].casefold()
        if certificate in seen_certificates:
            warnings.append(
                f"Rândul {source['source_row']}: numărul de certificat este duplicat în fișier."
            )
        seen_certificates.add(certificate)
        valid_rows.append(valid)
    return {
        "valid_rows": valid_rows,
        "invalid_rows": invalid_rows,
        "warnings": warnings,
    }


def parse_participant_upload(*, upload, worksheet_name: str | None = None) -> dict:
    discovered = discover_participant_upload(
        upload=upload,
        first_row_has_headers=True,
        worksheet_name=worksheet_name,
    )
    if set(discovered["suggested_mapping"]) != set(PARTICIPANT_COLUMNS):
        raise ValidationError("Coloanele trebuie asociate înainte de validarea participanților.")
    return validate_participant_mapping(
        source_rows=discovered["source_rows"],
        column_mapping=discovered["suggested_mapping"],
    )


def create_participant_import_draft(*, owner, data: dict) -> ParticipantImportDraft:
    tables = _participant_upload_tables(
        upload=data["source_file"],
        first_row_has_headers=data.get("first_row_has_headers", False),
    )
    discovered_sheets = [
        {
            "name": sheet_name,
            **_discover_participant_table(
                table_rows=table_rows,
                first_row_has_headers=data.get("first_row_has_headers", False),
            ),
        }
        for sheet_name, table_rows in tables
    ]
    discovered = discovered_sheets[0] if len(discovered_sheets) == 1 else None
    return ParticipantImportDraft.objects.create(
        owner=owner,
        list_name=data["list_name"],
        description=data.get("description", ""),
        course_name=data.get("course_name", ""),
        source_file_name=Path(data["source_file"].name).name[:255],
        source_sheets_json=discovered_sheets if len(discovered_sheets) > 1 else [],
        source_columns_json=discovered["columns"] if discovered else [],
        source_rows_json=discovered["source_rows"] if discovered else [],
        column_mapping_json=discovered["suggested_mapping"] if discovered else {},
        expires_at=timezone.now() + timedelta(hours=24),
    )


def select_participant_import_sheet(
    *, owner, draft_id, sheet_index: int
) -> ParticipantImportDraft:
    with transaction.atomic():
        draft = get_owned_import_draft_for_update(user=owner, draft_id=draft_id)
        if sheet_index < 0:
            raise ValidationError("Foaia XLSX selectată nu este disponibilă.")
        try:
            selected = draft.source_sheets_json[sheet_index]
        except (IndexError, TypeError):
            raise ValidationError("Foaia XLSX selectată nu este disponibilă.")
        draft.source_columns_json = selected["columns"]
        draft.source_rows_json = selected["source_rows"]
        draft.column_mapping_json = selected["suggested_mapping"]
        draft.save(
            update_fields=(
                "source_columns_json",
                "source_rows_json",
                "column_mapping_json",
            )
        )
        return draft


def apply_participant_import_mapping(*, owner, draft_id, column_mapping) -> ParticipantImportDraft:
    with transaction.atomic():
        draft = get_owned_import_draft_for_update(user=owner, draft_id=draft_id)
        available_indexes = {
            int(column["index"]) for column in draft.source_columns_json
        }
        try:
            requested_indexes = {int(index) for index in column_mapping.values()}
        except (TypeError, ValueError) as exc:
            raise ValidationError("Asocierea coloanelor nu este validă.") from exc
        if not requested_indexes.issubset(available_indexes):
            raise ValidationError("Asocierea conține o coloană inexistentă.")
        parsed = validate_participant_mapping(
            source_rows=draft.source_rows_json,
            column_mapping=column_mapping,
        )
        draft.column_mapping_json = {
            field: int(index) for field, index in column_mapping.items()
        }
        draft.mapping_confirmed = True
        draft.valid_rows_json = parsed["valid_rows"]
        draft.invalid_rows_json = parsed["invalid_rows"]
        draft.warnings_json = parsed["warnings"]
        draft.save(
            update_fields=(
                "column_mapping_json",
                "mapping_confirmed",
                "valid_rows_json",
                "invalid_rows_json",
                "warnings_json",
            )
        )
        return draft


def confirm_participant_import(*, owner, draft_id) -> ParticipantList:
    with transaction.atomic():
        draft = get_owned_import_draft_for_update(user=owner, draft_id=draft_id)
        if not draft.mapping_confirmed:
            raise ValidationError("Coloanele trebuie asociate înainte de confirmarea importului.")
        if not draft.valid_rows_json:
            raise ValidationError("Importul nu conține niciun rând valid.")
        participant_list = ParticipantList.objects.create(
            owner=owner,
            name=draft.list_name,
            description=draft.description,
            course_name=draft.course_name,
            source_file_name=draft.source_file_name,
            participant_count=len(draft.valid_rows_json),
        )
        participants = []
        for row in draft.valid_rows_json:
            parsed_date, _ = _strict_date(row["date_of_birth"])
            participants.append(
                Participant(
                    owner=owner,
                    participant_list=participant_list,
                    full_name=row["full_name"],
                    date_of_birth=parsed_date,
                    place_of_birth=row["place_of_birth"],
                    certificate_number=row["certificate_number"],
                    source_row=row["source_row"],
                )
            )
        Participant.objects.bulk_create(participants)
        draft.delete()
        return participant_list


def delete_participant_list(*, owner, participant_list_id) -> None:
    with transaction.atomic():
        participant_list = get_owned_participant_list_for_update(
            user=owner,
            participant_list_id=participant_list_id,
        )
        participant_list.delete()


def build_diploma_preview_context(
    *,
    owner,
    participant_list_id,
    participant_id,
    template_id,
) -> dict:
    try:
        participant_list_id = uuid.UUID(str(participant_list_id))
        participant_id = uuid.UUID(str(participant_id))
        template_id = uuid.UUID(str(template_id))
    except (TypeError, ValueError, AttributeError) as exc:
        raise Http404("Selecția pentru previzualizare nu este validă.") from exc
    participant_list = get_owned_participant_list(
        user=owner,
        participant_list_id=participant_list_id,
    )
    participant = get_owned_participant(user=owner, participant_id=participant_id)
    template = get_owned_template(user=owner, template_id=template_id)
    if participant.participant_list_id != participant_list.pk:
        raise Http404("Participantul nu aparține listei selectate.")
    return {
        "participant_list": participant_list,
        "participant": participant,
        "diploma_template": template,
        "layout": validate_layout_json(template.layout_json),
        "media_assets": serialize_media_assets(
            require_owned_layout_assets(owner=owner, layout=template.layout_json).values()
        ),
        "participant_data": {
            "full_name": participant.full_name,
            "date_of_birth": participant.date_of_birth.strftime("%d.%m.%Y"),
            "place_of_birth": participant.place_of_birth,
            "certificate_number": participant.certificate_number,
        },
    }


def generate_single_diploma(
    *,
    owner,
    participant_list_id,
    participant_id,
    template_id,
) -> GeneratedDiploma:
    stored_file_name = ""
    storage = None
    try:
        with transaction.atomic():
            participant_list = get_owned_participant_list_for_update(
                user=owner,
                participant_list_id=participant_list_id,
            )
            participant = get_owned_participant_for_update(
                user=owner,
                participant_id=participant_id,
            )
            template = get_owned_template_for_update(
                user=owner,
                template_id=template_id,
            )
            if participant.participant_list_id != participant_list.pk:
                raise Http404("Participantul nu aparține listei selectate.")

            pdf_bytes = render_diploma_pdf(template=template, participant=participant)
            generated = GeneratedDiploma(
                owner=owner,
                participant_list=participant_list,
                participant=participant,
                template=template,
                certificate_number=participant.certificate_number,
                participant_name=participant.full_name,
                participant_list_name=participant_list.name,
                template_name=template.name,
            )
            generated.pdf_file.save(
                "diploma.pdf",
                ContentFile(pdf_bytes),
                save=False,
            )
            storage = generated.pdf_file.storage
            stored_file_name = generated.pdf_file.name
            generated.full_clean()
            generated.save()
            return generated
    except Exception:
        if storage is not None and stored_file_name:
            storage.delete(stored_file_name)
        raise


def get_generated_diploma_download(*, owner, generated_diploma_id) -> GeneratedDiploma:
    return get_owned_generated_diploma(
        user=owner,
        generated_diploma_id=generated_diploma_id,
    )


def build_generated_diploma_filename(generated_diploma: GeneratedDiploma) -> str:
    certificate = _safe_filename_part(
        generated_diploma.certificate_number,
        fallback="certificat",
    )
    participant = _safe_filename_part(
        generated_diploma.participant_name,
        fallback="participant",
    )
    safe_suffix = "_".join(filter(None, (certificate, participant))) or "diploma"
    return f"diploma_{safe_suffix[:180]}.pdf"


def _safe_filename_part(value, *, fallback: str) -> str:
    separated = re.sub(r"[^\w]+", "-", str(value or ""), flags=re.UNICODE)
    normalized = slugify(separated, allow_unicode=False).replace("-", "_")
    normalized = re.sub(r"[^a-zA-Z0-9_]", "_", normalized)
    normalized = re.sub(r"_+", "_", normalized).strip("_")
    return normalized or fallback


def _batch_pdf_filename(participant: Participant) -> str:
    certificate = _safe_filename_part(
        participant.certificate_number,
        fallback="certificat",
    )
    participant_name = _safe_filename_part(
        participant.full_name,
        fallback="participant",
    )
    return f"{certificate[:80]}_{participant_name[:120]}.pdf"


def _available_batch_pdf_filename(*, batch, participant, storage) -> str:
    original = _batch_pdf_filename(participant)
    stem = original.removesuffix(".pdf")
    candidate = original
    suffix = 2
    while storage.exists(f"{batch.output_folder}/{candidate}"):
        candidate = f"{stem[:190]}_{suffix}.pdf"
        suffix += 1
    return candidate


def create_generation_batch(owner, participant_list_id, template_id):
    with transaction.atomic():
        participant_list = get_owned_participant_list_for_update(
            user=owner,
            participant_list_id=participant_list_id,
        )
        template = get_owned_template_for_update(
            user=owner,
            template_id=template_id,
        )
        normalized_layout = validate_layout_json(template.layout_json)
        require_owned_layout_assets(owner=owner, layout=normalized_layout)
        total_count = participant_list.participants.filter(owner=owner).count()
        if total_count == 0:
            raise ValidationError("Lista selectată nu conține participanți.")

        batch = DiplomaGenerationBatch(
            owner=owner,
            participant_list=participant_list,
            template=template,
            participant_list_name=participant_list.name,
            template_name=template.name,
            total_count=total_count,
        )
        batch.output_folder = (
            f"diplomas/{owner.pk}/{participant_list.pk}/{batch.pk}"
        )
        batch.full_clean()
        batch.save()
        return batch


def generate_batch_participant_pdf(batch, participant):
    if participant.owner_id != batch.owner_id:
        raise ValidationError("Participantul nu aparține utilizatorului lotului.")
    if participant.participant_list_id != batch.participant_list_id:
        raise ValidationError("Participantul nu aparține listei lotului.")

    pdf_bytes = render_diploma_pdf(
        template=batch.template,
        participant=participant,
    )
    generated = GeneratedDiploma(
        owner_id=batch.owner_id,
        participant_list=batch.participant_list,
        participant=participant,
        template=batch.template,
        batch=batch,
        certificate_number=participant.certificate_number,
        participant_name=participant.full_name,
        participant_list_name=batch.participant_list_display_name,
        template_name=batch.template_display_name,
    )
    storage = generated.pdf_file.storage
    stored_file_name = ""
    try:
        filename = _available_batch_pdf_filename(
            batch=batch,
            participant=participant,
            storage=storage,
        )
        generated.pdf_file.save(filename, ContentFile(pdf_bytes), save=False)
        stored_file_name = generated.pdf_file.name
        generated.full_clean()
        generated.save()
        return generated
    except Exception:
        if stored_file_name:
            storage.delete(stored_file_name)
        raise


def _participant_batch_error(participant) -> dict:
    return {
        "participant_id": str(participant.pk),
        "participant_name": participant.full_name,
        "certificate_number": participant.certificate_number,
        "message": "PDF-ul nu a putut fi generat pentru acest participant.",
    }


def finalize_generation_batch(batch):
    success_count = batch.generated_diplomas.count()
    failed_count = max(batch.total_count - success_count, 0)
    if success_count == batch.total_count:
        status = DiplomaGenerationBatch.Status.COMPLETED
    elif success_count:
        status = DiplomaGenerationBatch.Status.COMPLETED_WITH_ERRORS
    else:
        status = DiplomaGenerationBatch.Status.FAILED

    batch.status = status
    batch.success_count = success_count
    batch.failed_count = failed_count
    batch.completed_at = timezone.now()
    batch.save(
        update_fields=(
            "status",
            "success_count",
            "failed_count",
            "error_summary",
            "completed_at",
            "updated_at",
        )
    )
    return batch


def run_generation_batch(batch_id):
    with transaction.atomic():
        batch = (
            DiplomaGenerationBatch.objects.select_for_update(of=("self",))
            .select_related(
                "owner",
                "participant_list",
                "template",
            )
            .get(pk=batch_id)
        )
        if batch.status in {
            DiplomaGenerationBatch.Status.COMPLETED,
            DiplomaGenerationBatch.Status.COMPLETED_WITH_ERRORS,
            DiplomaGenerationBatch.Status.FAILED,
            DiplomaGenerationBatch.Status.RUNNING,
        }:
            return batch
        batch.status = DiplomaGenerationBatch.Status.RUNNING
        batch.started_at = timezone.now()
        batch.success_count = 0
        batch.failed_count = 0
        batch.error_summary = []
        batch.save(
            update_fields=(
                "status",
                "started_at",
                "success_count",
                "failed_count",
                "error_summary",
                "updated_at",
            )
        )

    participants = Participant.objects.filter(
        owner_id=batch.owner_id,
        participant_list_id=batch.participant_list_id,
    ).order_by("source_row", "full_name")
    errors = []
    success_count = 0
    attempted_count = 0
    try:
        for participant in participants.iterator():
            attempted_count += 1
            try:
                generate_batch_participant_pdf(batch, participant)
                success_count += 1
            except Exception:
                errors.append(_participant_batch_error(participant))
            DiplomaGenerationBatch.objects.filter(pk=batch.pk).update(
                success_count=success_count,
                failed_count=attempted_count - success_count,
                error_summary=errors,
                updated_at=timezone.now(),
            )
    except Exception:
        errors.append(
            {
                "message": "Generarea lotului a fost întreruptă înainte de finalizare."
            }
        )

    batch.refresh_from_db()
    batch.error_summary = errors
    return finalize_generation_batch(batch)


def _mark_pending_generation_batch_failed(batch_id):
    with transaction.atomic():
        batch = (
            DiplomaGenerationBatch.objects.select_for_update(of=("self",))
            .filter(
                pk=batch_id,
                status=DiplomaGenerationBatch.Status.PENDING,
            )
            .first()
        )
        if batch is None:
            return
        batch.status = DiplomaGenerationBatch.Status.FAILED
        batch.failed_count = batch.total_count
        batch.error_summary = [
            {"message": "Generarea lotului nu a putut porni."}
        ]
        batch.completed_at = timezone.now()
        batch.save(
            update_fields=(
                "status",
                "failed_count",
                "error_summary",
                "completed_at",
                "updated_at",
            )
        )


def _run_pending_generation_batch(batch_id):
    try:
        return run_generation_batch(batch_id)
    except Exception:
        _mark_pending_generation_batch_failed(batch_id)
        raise


def generate_diploma_batch(owner, participant_list_id, template_id):
    batch = create_generation_batch(owner, participant_list_id, template_id)
    return _run_pending_generation_batch(batch.pk)


def resume_generation_batch(owner, batch_id):
    batch = get_owned_generation_batch(owner, batch_id)
    if batch.status != DiplomaGenerationBatch.Status.PENDING:
        raise ValidationError(
            "Doar loturile aflate în așteptare pot fi reluate."
        )
    return _run_pending_generation_batch(batch.pk)


def build_batch_zip_response(owner, batch_id):
    batch = get_owned_generation_batch(owner, batch_id)
    generated_diplomas = list_generated_diplomas_for_batch(owner, batch.pk)
    archive_buffer = BytesIO()
    used_names = set()
    with ZipFile(archive_buffer, mode="w", compression=ZIP_DEFLATED) as archive:
        for generated in generated_diplomas:
            try:
                if not generated.pdf_file.storage.exists(generated.pdf_file.name):
                    continue
                with generated.pdf_file.open("rb") as pdf_file:
                    content = pdf_file.read()
            except (OSError, ValueError):
                continue

            archive_name = Path(generated.pdf_file.name).name
            archive_name = re.sub(r"[^a-zA-Z0-9_.-]", "_", archive_name)
            stem = Path(archive_name).stem or "diploma"
            suffix = Path(archive_name).suffix.lower() or ".pdf"
            unique_name = f"{stem}{suffix}"
            duplicate = 2
            while unique_name.casefold() in used_names:
                unique_name = f"{stem}_{duplicate}{suffix}"
                duplicate += 1
            used_names.add(unique_name.casefold())
            archive.writestr(unique_name, content)

    list_name = _safe_filename_part(
        batch.participant_list_display_name,
        fallback="lista",
    )
    archive_filename = (
        f"diplome_{list_name[:140]}_{batch.created_at:%Y-%m-%d}.zip"
    )
    response = HttpResponse(
        archive_buffer.getvalue(),
        content_type="application/zip",
    )
    response["Content-Disposition"] = f'attachment; filename="{archive_filename}"'
    return response


def build_generation_history_context(owner, filters):
    batches = list_owned_generation_batches(owner)
    participant_list = filters.get("participant_list")
    template = filters.get("template")
    status = filters.get("status")
    created_date = filters.get("date")
    if participant_list:
        batches = batches.filter(participant_list=participant_list)
    if template:
        batches = batches.filter(template=template)
    if status:
        batches = batches.filter(status=status)
    if created_date:
        batches = batches.filter(created_at__date=created_date)
    return {"batches": batches}
```

## `apps/diplome/static/diplome/generation.js`

Size: 3.3 KB

```javascript
(function () {
    "use strict";

    const listSelect = document.querySelector("[data-generation-list]");
    const participantTable = document.querySelector("[data-participant-table]");
    if (!listSelect || !participantTable) return;

    const participantRows = participantTable
        ? Array.from(participantTable.querySelectorAll("[data-participant-row]"))
        : [];
    const participantCount = participantTable.querySelector("[data-participant-count]");
    const participantEmpty = participantTable.querySelector("[data-participant-empty]");
    const participantTableBody = participantTable.querySelector("[data-participant-rows]");
    const participantScroll = participantTable.querySelector("[data-participant-scroll]");

    function syncSelectedRow() {
        let selectedCount = 0;
        participantRows.forEach((row) => {
            const checkbox = row.querySelector("[data-participant-checkbox]");
            const isSelected = checkbox.checked;
            if (!row.hidden && isSelected) selectedCount += 1;
            row.classList.toggle("bg-primary/10", isSelected);
            row.classList.toggle("hover:bg-base-200/70", !isSelected);
            row.setAttribute("aria-selected", String(isSelected));
        });
        participantCount.textContent = String(selectedCount);
    }

    function syncParticipantTable() {
        if (!participantTable) return;

        const listId = listSelect.value;
        let visibleCount = 0;
        participantRows.forEach((row) => {
            const isVisible = Boolean(listId && row.dataset.participantListId === listId);
            row.hidden = !isVisible;
            if (!isVisible) row.querySelector("[data-participant-checkbox]").checked = false;
            if (isVisible) visibleCount += 1;
        });
        participantTableBody.hidden = visibleCount === 0;
        participantEmpty.hidden = visibleCount > 0;
        participantEmpty.textContent = listId
            ? "Lista selectată nu conține participanți."
            : "Selectează mai întâi o listă cu participanți.";
        syncSelectedRow();
        const selectedRow = participantRows.find(
            (row) => !row.hidden && row.querySelector("[data-participant-checkbox]").checked
        );
        if (selectedRow) {
            participantScroll.scrollTop = Math.max(
                0,
                selectedRow.offsetTop - participantScroll.clientHeight / 2
            );
        }
    }

    function selectOnly(checkbox) {
        participantRows.forEach((row) => {
            const rowCheckbox = row.querySelector("[data-participant-checkbox]");
            if (rowCheckbox !== checkbox) rowCheckbox.checked = false;
        });
        syncSelectedRow();
    }

    participantRows.forEach((row) => {
        const checkbox = row.querySelector("[data-participant-checkbox]");
        checkbox.addEventListener("change", () => {
            if (checkbox.checked) selectOnly(checkbox);
            else syncSelectedRow();
        });
        row.addEventListener("click", (event) => {
            if (row.hidden) return;
            if (event.target !== checkbox) {
                checkbox.checked = true;
                selectOnly(checkbox);
            }
        });
    });

    listSelect.addEventListener("change", syncParticipantTable);
    syncParticipantTable();
})();
```

## `apps/diplome/static/diplome/participant_import.js`

Size: 1.4 KB

```javascript
(() => {
    const form = document.querySelector("[data-participant-import-form]");
    const toast = document.querySelector("[data-participant-import-toast]");
    const toastMessage = toast?.querySelector("[data-participant-import-toast-message]");
    const listName = form?.querySelector("#id_list_name");
    const sourceFile = form?.querySelector("#id_source_file");
    let hideTimer;

    if (!form || !toast || !toastMessage || !listName || !sourceFile) {
        return;
    }

    const showError = (message, field) => {
        window.clearTimeout(hideTimer);
        toastMessage.textContent = message;
        toast.classList.remove("hidden");
        field.setAttribute("aria-invalid", "true");
        field.focus();
        hideTimer = window.setTimeout(() => toast.classList.add("hidden"), 5000);
    };

    listName.addEventListener("input", () => listName.removeAttribute("aria-invalid"));
    sourceFile.addEventListener("change", () => sourceFile.removeAttribute("aria-invalid"));

    form.addEventListener("submit", (event) => {
        if (!listName.value.trim()) {
            event.preventDefault();
            showError("Numele listei este obligatoriu.", listName);
            return;
        }
        if (!sourceFile.files.length) {
            event.preventDefault();
            showError("Selectează un fișier CSV sau XLSX.", sourceFile);
        }
    });
})();
```

## `apps/diplome/static/diplome/participant_mapping.js`

Size: 1.7 KB

```javascript
(() => {
    "use strict";

    const form = document.querySelector("[data-mapping-form]");
    if (!form) return;

    const selects = Array.from(form.querySelectorAll("[data-mapping-select]"));
    const mappedCount = form.querySelector("[data-mapped-count]");

    function refreshMappingState() {
        const selectedValues = selects.map((select) => select.value).filter(Boolean);

        selects.forEach((select) => {
            Array.from(select.options).forEach((option) => {
                option.disabled = Boolean(
                    option.value &&
                    option.value !== select.value &&
                    selectedValues.includes(option.value)
                );
            });

            const row = select.closest("[data-mapping-row]");
            const isMapped = Boolean(select.value);
            row.classList.toggle("border-base-300", !isMapped);
            row.classList.toggle("border-primary", isMapped);
            row.classList.toggle("bg-base-100", !isMapped);
            row.classList.toggle("bg-primary/5", isMapped);
            row.querySelector("[data-mapped-icon]").classList.toggle("hidden", !isMapped);
            row.querySelector("[data-ignored-icon]").classList.toggle("hidden", isMapped);
            row.querySelector("[data-status-label]").textContent = isMapped ? "Asociată" : "Ignorată";
            row.querySelector("[data-mapping-status]").classList.toggle("text-success", isMapped);
        });

        if (mappedCount) mappedCount.textContent = String(new Set(selectedValues).size);
    }

    selects.forEach((select) => select.addEventListener("change", refreshMappingState));
    refreshMappingState();
})();
```

## `apps/diplome/static/diplome/template_editor.css`

Size: 26.9 KB

```css
.diploma-editor {
    --editor-border: var(--tuvtk-border-default);
    --editor-muted: var(--tuvtk-panel-muted-bg);
    --editor-workspace: #eef2f6;
    --editor-selected: var(--tuvtk-brand-primary);
    display: grid;
    min-height: 0;
    height: 100%;
    overflow: hidden;
    border: 1px solid var(--editor-border);
    background: var(--tuvtk-panel-bg);
    grid-template-rows: auto auto minmax(0, 1fr) auto;
}

body:has(.diploma-editor) .drawer-content > main {
    overflow: hidden;
}

body:has(.diploma-editor) .drawer-content > main > div {
    height: 100%;
    max-width: none;
}

@media (min-width: 1024px) {
    body:has(.diploma-editor) .drawer-content > main > div {
        padding: 0;
    }

    body:has(.diploma-editor) .diploma-editor {
        border-block: 0;
        border-right: 0;
    }
}

.editor-heading,
.preview-heading {
    display: flex;
    min-width: 0;
    align-items: flex-end;
    justify-content: space-between;
    gap: 1rem;
    border-bottom: 1px solid var(--editor-border);
    background: var(--tuvtk-panel-bg);
    padding: 0.9rem 1rem;
}

.editor-heading h1,
.preview-heading h1 {
    margin-top: 0.25rem;
    color: var(--tuvtk-heading-text);
    font-size: 1.4rem;
    font-weight: 750;
    line-height: 1.2;
}

.editor-heading p,
.preview-heading p {
    margin-top: 0.25rem;
    color: var(--tuvtk-muted-text);
    font-size: 0.78rem;
}

.editor-heading-actions {
    display: flex;
    flex: none;
    flex-wrap: wrap;
    justify-content: flex-end;
    margin-left: auto;
    gap: 0.5rem;
}

.editor-toolbar {
    position: relative;
    z-index: 20;
    display: flex;
    min-height: 3.2rem;
    align-items: center;
    gap: 0.35rem;
    overflow: visible;
    border-bottom: 1px solid var(--editor-border);
    background: var(--tuvtk-panel-bg);
    padding: 0.45rem 0.65rem;
    scrollbar-width: thin;
}

.editor-tool,
.editor-tool-field {
    display: inline-flex;
    min-height: 2.1rem;
    flex: none;
    align-items: center;
    justify-content: center;
    gap: 0.35rem;
    border: 1px solid var(--editor-border);
    border-radius: var(--radius-field);
    background: var(--tuvtk-panel-bg);
    padding: 0.35rem 0.55rem;
    color: var(--tuvtk-body-text);
    font-size: 0.75rem;
    font-weight: 600;
    line-height: 1;
}

button.editor-tool {
    cursor: pointer;
}

.editor-tool:hover:not(:disabled),
.editor-tool.is-active {
    border-color: var(--tuvtk-brand-primary);
    background: var(--tuvtk-control-hover-bg);
    color: var(--tuvtk-brand-primary);
}

.editor-tool:disabled {
    cursor: not-allowed;
    opacity: 0.42;
}

.editor-tool-field select {
    border: 0;
    background: transparent;
    color: inherit;
    font: inherit;
    outline: none;
}

.editor-zoom-controls {
    display: inline-flex;
    flex: none;
    align-items: stretch;
    gap: 0.25rem;
}

.editor-zoom-button {
    width: 2.1rem;
    padding-inline: 0;
    font-size: 1rem;
}

.editor-toolbar-divider {
    width: 1px;
    height: 1.75rem;
    flex: none;
    margin-inline: 0.2rem;
    background: var(--editor-border);
}

.editor-workspace {
    display: grid;
    min-width: 0;
    min-height: 0;
    grid-template-columns: 16rem minmax(28rem, 1fr) 18rem;
}

.editor-panel {
    position: relative;
    z-index: 10;
    display: flex;
    min-width: 0;
    min-height: 0;
    flex-direction: column;
    background: var(--tuvtk-panel-bg);
}

.editor-layers-panel {
    border-right: 1px solid var(--editor-border);
}

.editor-inspector-panel {
    border-left: 1px solid var(--editor-border);
}

.editor-inspector-tabs {
    display: grid;
    min-height: 2.8rem;
    flex: none;
    border-bottom: 1px solid var(--editor-border);
    background: var(--editor-muted);
    grid-template-columns: repeat(2, minmax(0, 1fr));
}

.editor-inspector-tab {
    position: relative;
    cursor: pointer;
    padding: 0.65rem 0.5rem;
    color: var(--tuvtk-muted-text);
    font-size: 0.72rem;
    font-weight: 700;
}

.editor-inspector-tab + .editor-inspector-tab {
    border-left: 1px solid var(--editor-border);
}

.editor-inspector-tab:hover,
.editor-inspector-tab:focus-visible {
    background: var(--tuvtk-control-hover-bg);
    color: var(--tuvtk-brand-primary);
    outline: none;
}

.editor-inspector-tab.is-active {
    background: var(--tuvtk-panel-bg);
    color: var(--tuvtk-brand-primary);
}

.editor-inspector-tab.is-active::after {
    position: absolute;
    right: 0.65rem;
    bottom: -1px;
    left: 0.65rem;
    height: 2px;
    background: var(--editor-selected);
    content: "";
}

.editor-inspector-pane {
    display: flex;
    min-width: 0;
    min-height: 0;
    flex: 1;
    flex-direction: column;
}

.editor-inspector-pane[hidden] {
    display: none;
}

.editor-inspector-pane-properties .editor-properties {
    flex: 1;
}

.editor-inspector-pane-elements {
    overflow-y: auto;
}

.editor-element-library {
    display: grid;
    gap: 1rem;
    padding: 0.65rem;
}

.editor-element-actions {
    display: grid;
    gap: 0.35rem;
}

.editor-element-action {
    display: grid;
    min-width: 0;
    cursor: pointer;
    align-items: center;
    gap: 0.6rem;
    border: 1px solid var(--editor-border);
    border-radius: var(--radius-field);
    background: var(--tuvtk-panel-bg);
    padding: 0.5rem;
    text-align: left;
    grid-template-columns: 2rem minmax(0, 1fr);
}

.editor-element-action:hover,
.editor-element-action:focus-visible {
    border-color: var(--editor-selected);
    background: var(--tuvtk-control-hover-bg);
    outline: none;
}

.editor-element-action > span:last-child {
    display: grid;
    min-width: 0;
    gap: 0.1rem;
}

.editor-element-action strong {
    color: var(--tuvtk-heading-text);
    font-size: 0.72rem;
}

.editor-element-action small {
    overflow: hidden;
    color: var(--tuvtk-muted-text);
    font-size: 0.62rem;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.editor-element-icon {
    display: grid;
    width: 2rem;
    height: 2rem;
    place-items: center;
    border: 1px solid var(--editor-border);
    background: var(--editor-muted);
    color: var(--tuvtk-brand-primary);
    font-size: 0.85rem;
    font-weight: 750;
}

.editor-variable-library {
    border-top: 1px solid var(--editor-border);
    padding-top: 0.75rem;
}

.editor-variable-library h3 {
    margin-bottom: 0.5rem;
    color: var(--tuvtk-heading-text);
    font-size: 0.68rem;
    font-weight: 750;
}

.editor-variable-library > div {
    display: grid;
    gap: 0.3rem;
    grid-template-columns: repeat(2, minmax(0, 1fr));
}

.editor-variable-library button {
    min-height: 2rem;
    cursor: pointer;
    border: 1px solid var(--editor-border);
    border-radius: var(--radius-field);
    padding: 0.35rem;
    color: var(--tuvtk-body-text);
    font-size: 0.62rem;
    line-height: 1.2;
}

.editor-variable-library button:hover,
.editor-variable-library button:focus-visible {
    border-color: var(--editor-selected);
    color: var(--tuvtk-brand-primary);
    outline: none;
}

.editor-panel-title {
    display: flex;
    min-height: 2.8rem;
    flex: none;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid var(--editor-border);
    padding: 0.65rem 0.75rem;
}

.editor-panel-title h2 {
    font-size: 0.8rem;
    font-weight: 750;
}

.editor-layers {
    min-height: 0;
    flex: 1;
    overflow-y: auto;
}

.editor-layer {
    display: grid;
    min-height: 2.75rem;
    cursor: pointer;
    align-items: center;
    gap: 0.3rem;
    border-bottom: 1px solid var(--editor-border);
    padding: 0.45rem 0.45rem;
    grid-template-columns: 1.1rem minmax(0, 1fr) repeat(4, 1.6rem);
}

.editor-layer:hover {
    background: var(--tuvtk-control-hover-bg);
}

.editor-layer.is-selected {
    background: var(--tuvtk-primary-tint-bg);
    box-shadow: inset 3px 0 var(--editor-selected);
}

.editor-layer-drag {
    color: var(--tuvtk-muted-text);
    font-size: 0.75rem;
    letter-spacing: -0.1em;
}

.editor-layer-name {
    overflow: hidden;
    color: var(--tuvtk-body-text);
    font-size: 0.76rem;
    font-weight: 600;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.editor-layer button {
    display: grid;
    width: 1.6rem;
    height: 1.6rem;
    cursor: pointer;
    place-items: center;
    border-radius: var(--radius-field);
    color: var(--tuvtk-muted-text);
    font-size: 0.75rem;
}

.editor-layer button:hover {
    background: var(--tuvtk-panel-bg);
    color: var(--tuvtk-brand-primary);
}

.editor-layer-actions {
    display: grid;
    flex: none;
    gap: 0.35rem;
    border-top: 1px solid var(--editor-border);
    padding: 0.55rem;
}

.editor-align-actions {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.25rem;
    border-top: 1px solid var(--editor-border);
    padding: 0.45rem;
}

.editor-align-actions button {
    min-height: 1.8rem;
    border: 1px solid var(--editor-border);
    border-radius: var(--radius-field);
    font-size: 0.8rem;
}

.editor-align-actions button:disabled {
    cursor: not-allowed;
    opacity: 0.35;
}

.editor-guide-controls {
    display: grid;
    gap: 0.35rem;
    border-top: 1px solid var(--editor-border);
    padding: 0.5rem;
}

.editor-guide-input-row {
    display: grid;
    grid-template-columns: minmax(0, 1fr) 2.4rem 2.4rem;
    gap: 0.3rem;
}

.editor-guide-input-row label {
    display: grid;
    gap: 0.2rem;
    color: var(--tuvtk-muted-text);
    font-size: 0.65rem;
}

.editor-guide-input-row input,
.editor-guide-input-row button,
.editor-custom-guides button {
    min-width: 0;
    border: 1px solid var(--editor-border);
    border-radius: var(--radius-field);
    background: var(--tuvtk-panel-bg);
    padding: 0.3rem 0.4rem;
    font-size: 0.7rem;
}

.editor-guide-controls small {
    color: var(--tuvtk-muted-text);
    font-size: 0.62rem;
    line-height: 1.25;
}

.editor-custom-guides {
    display: flex;
    flex-wrap: wrap;
    gap: 0.25rem;
}

.editor-custom-guides button {
    color: var(--tuvtk-brand-primary);
}

.editor-layer-actions button {
    min-height: 2rem;
    cursor: pointer;
    border: 1px solid var(--editor-border);
    border-radius: var(--radius-field);
    color: var(--tuvtk-body-text);
    font-size: 0.7rem;
    font-weight: 600;
    text-align: left;
    padding-inline: 0.65rem;
}

.editor-layer-actions button:hover {
    border-color: var(--tuvtk-brand-primary);
    color: var(--tuvtk-brand-primary);
}

.editor-canvas-viewport {
    min-width: 0;
    min-height: 0;
    overflow: scroll;
    overscroll-behavior: contain;
    background: var(--editor-workspace);
    padding: 1rem;
    scrollbar-color: var(--scrollbar-thumb) var(--editor-muted);
    scrollbar-gutter: stable;
    scrollbar-width: auto;
}

.editor-canvas-viewport::-webkit-scrollbar {
    width: 12px;
    height: 12px;
}

.editor-canvas-viewport::-webkit-scrollbar-track,
.editor-canvas-viewport::-webkit-scrollbar-corner {
    background: var(--editor-muted);
}

.editor-canvas-viewport::-webkit-scrollbar-thumb {
    border: 3px solid var(--editor-muted);
    border-radius: 9999px;
    background: var(--scrollbar-thumb);
}

.editor-canvas-shell {
    position: relative;
    margin: 0 auto;
}

.editor-ruler-corner {
    position: absolute;
    z-index: 6;
    top: 0;
    left: 0;
    width: 1.7rem;
    height: 1.7rem;
    border-right: 1px solid var(--editor-border);
    border-bottom: 1px solid var(--editor-border);
    background: var(--editor-muted);
}

.editor-ruler {
    position: absolute;
    z-index: 5;
    overflow: hidden;
    background-color: var(--editor-muted);
    color: var(--tuvtk-muted-text);
    font-size: 0.58rem;
    pointer-events: none;
}

.editor-ruler-top {
    top: 0;
    left: 1.7rem;
    height: 1.7rem;
    border-bottom: 1px solid var(--editor-border);
    background-image: linear-gradient(90deg, transparent calc(100% - 1px), #aebbc6 0);
}

.editor-ruler-left {
    top: 1.7rem;
    left: 0;
    width: 1.7rem;
    border-right: 1px solid var(--editor-border);
    background-image: linear-gradient(180deg, transparent calc(100% - 1px), #aebbc6 0);
}

.editor-ruler-label {
    position: absolute;
    line-height: 1;
}

.editor-ruler-top .editor-ruler-label {
    top: 0.15rem;
    transform: translateX(2px);
}

.editor-ruler-left .editor-ruler-label {
    left: 0.12rem;
    transform: translateY(2px);
}

.editor-stage {
    position: absolute;
    top: 1.7rem;
    left: 1.7rem;
    transform-origin: top left;
}

.diploma-canvas {
    position: relative;
    overflow: hidden;
    background-color: #ffffff;
    box-shadow: 0 4px 14px rgb(23 33 43 / 0.18);
    outline: 1px solid #b8c4cf;
    touch-action: none;
}

.diploma-canvas.has-grid {
    background-image:
        linear-gradient(to right, rgb(22 65 148 / 0.16) 1px, transparent 1px),
        linear-gradient(to bottom, rgb(22 65 148 / 0.16) 1px, transparent 1px),
        linear-gradient(to right, rgb(22 65 148 / 0.055) 1px, transparent 1px),
        linear-gradient(to bottom, rgb(22 65 148 / 0.055) 1px, transparent 1px);
    background-size:
        var(--major-grid-size) var(--major-grid-size),
        var(--major-grid-size) var(--major-grid-size),
        var(--minor-grid-size) var(--minor-grid-size),
        var(--minor-grid-size) var(--minor-grid-size);
}

.diploma-element {
    position: absolute;
    display: flex;
    overflow: hidden;
    align-items: center;
    box-sizing: border-box;
    cursor: move;
    user-select: none;
    transform-origin: center;
}

.diploma-element.is-hidden {
    display: none;
}

.diploma-element.is-locked {
    cursor: not-allowed;
}

.diploma-element.is-selected {
    overflow: visible;
    outline: 2px solid var(--editor-selected);
    outline-offset: 1px;
}

.diploma-element-content {
    width: 100%;
    max-height: 100%;
    overflow: hidden;
    line-height: 1.18;
    white-space: pre-wrap;
}

.diploma-list {
    width: 100%;
    max-height: 100%;
    margin: 0;
    overflow: hidden;
    box-sizing: border-box;
}

.diploma-list li {
    padding-inline-start: 0.25em;
}

.diploma-element-table {
    align-items: stretch;
}

.diploma-element-table table {
    width: 100%;
    height: 100%;
    border-collapse: collapse;
    table-layout: fixed;
}

.diploma-element-table th,
.diploma-element-table td {
    overflow: hidden;
    border: 1px solid var(--element-border, #164194);
    padding: 0.25rem;
    text-overflow: ellipsis;
}

.diploma-element-table th {
    background: var(--element-header, #edf3f9);
}

.diploma-placeholder {
    display: grid;
    width: 100%;
    height: 100%;
    place-items: center;
    border: 1px dashed var(--tuvtk-border-hover);
    background: var(--tuvtk-panel-muted-bg);
    color: var(--tuvtk-muted-text);
    font-family: Inter, "Segoe UI", sans-serif;
    font-size: 0.8rem;
}

.diploma-media {
    display: block;
    width: 100%;
    height: 100%;
    pointer-events: none;
    user-select: none;
}

.diploma-icon {
    display: grid;
    width: 100%;
    height: 100%;
    place-items: center;
    line-height: 1;
}

.diploma-icon-svg {
    display: block;
    width: 100%;
    height: 100%;
    overflow: visible;
}

.editor-resize-handle {
    position: absolute;
    right: -6px;
    bottom: -6px;
    width: 11px;
    height: 11px;
    cursor: nwse-resize;
    border: 2px solid #ffffff;
    background: var(--editor-selected);
    box-shadow: 0 0 0 1px var(--editor-selected);
}

.editor-guide {
    position: absolute;
    z-index: 2000;
    background: var(--tuvtk-brand-secondary);
    pointer-events: none;
}

.editor-guide-x {
    top: 0;
    bottom: 0;
    left: 50%;
    width: 1px;
}

.editor-guide-y {
    right: 0;
    left: 0;
    top: 50%;
    height: 1px;
}

.editor-guide-custom {
    z-index: 1999;
    background: repeating-linear-gradient(
        to bottom,
        var(--tuvtk-brand-secondary) 0 5px,
        transparent 5px 9px
    );
}

.editor-guide-custom.editor-guide-y {
    background: repeating-linear-gradient(
        to right,
        var(--tuvtk-brand-secondary) 0 5px,
        transparent 5px 9px
    );
}

.editor-checkbox-field {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    margin-top: 0.5rem;
    font-size: 0.72rem;
}

.editor-properties {
    min-height: 0;
    overflow-y: auto;
    padding: 0 0.75rem 1rem;
}

.editor-properties section {
    border-bottom: 1px solid var(--editor-border);
    padding-block: 0.8rem;
}

.editor-properties h3 {
    margin-bottom: 0.65rem;
    color: var(--tuvtk-heading-text);
    font-size: 0.72rem;
    font-weight: 750;
}

.editor-field-grid {
    display: grid;
    gap: 0.5rem;
    grid-template-columns: repeat(2, minmax(0, 1fr));
}

.editor-field,
.editor-field-grid label {
    display: grid;
    min-width: 0;
    gap: 0.25rem;
    color: var(--tuvtk-muted-text);
    font-size: 0.66rem;
    font-weight: 600;
}

.editor-field + .editor-field,
.editor-field-grid + .editor-field,
.editor-field + .editor-field-grid {
    margin-top: 0.55rem;
}

.editor-field input,
.editor-field select,
.editor-field textarea,
.editor-field-grid input,
.editor-field-grid select {
    width: 100%;
    min-height: 2rem;
    border: 1px solid var(--editor-border);
    border-radius: var(--radius-field);
    background: var(--tuvtk-panel-bg);
    padding: 0.35rem 0.45rem;
    color: var(--tuvtk-body-text);
    font-size: 0.72rem;
    font-weight: 500;
}

.editor-field textarea {
    min-height: 4.5rem;
    resize: vertical;
}

.editor-toggle-row {
    display: flex;
    gap: 0.35rem;
    margin-top: 0.55rem;
}

.editor-toggle-row button {
    display: grid;
    width: 2rem;
    height: 2rem;
    cursor: pointer;
    place-items: center;
    border: 1px solid var(--editor-border);
    border-radius: var(--radius-field);
    color: var(--tuvtk-body-text);
}

.editor-toggle-row button[aria-pressed="true"] {
    border-color: var(--tuvtk-brand-primary);
    background: var(--tuvtk-brand-primary);
    color: #ffffff;
}

.editor-empty-properties {
    padding: 1rem;
    color: var(--tuvtk-muted-text);
    font-size: 0.75rem;
    line-height: 1.5;
}

.editor-media-current-preview {
    display: grid;
    min-height: 3.5rem;
    align-items: center;
    gap: 0.55rem;
    margin-bottom: 0.6rem;
    border: 1px solid var(--editor-border);
    background: var(--editor-muted);
    padding: 0.4rem;
    grid-template-columns: 3rem minmax(0, 1fr);
}

.editor-media-current-preview img {
    width: 3rem;
    height: 2.7rem;
    background: #ffffff;
    object-fit: contain;
}

.editor-media-current-preview span:not(.editor-media-current-unavailable) {
    display: grid;
    min-width: 0;
    gap: 0.15rem;
}

.editor-media-current-preview strong,
.editor-media-current-preview small {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.editor-media-current-preview strong {
    color: var(--tuvtk-heading-text);
    font-size: 0.7rem;
}

.editor-media-current-preview small,
.editor-media-current-unavailable {
    color: var(--tuvtk-muted-text);
    font-size: 0.62rem;
}

.editor-media-current-unavailable {
    grid-column: 1 / -1;
    padding: 0.5rem;
    text-align: center;
}

.editor-media-property-actions {
    display: grid;
    gap: 0.35rem;
    margin-block: 0.55rem;
    grid-template-columns: minmax(0, 1fr) auto;
}

.editor-media-property-actions button,
.editor-media-secondary-action {
    min-height: 1.9rem;
    cursor: pointer;
    border: 1px solid var(--editor-border);
    border-radius: var(--radius-field);
    padding-inline: 0.5rem;
    color: var(--tuvtk-body-text);
    font-size: 0.65rem;
    font-weight: 650;
}

.editor-media-property-actions button:hover:not(:disabled),
.editor-media-secondary-action:hover:not(:disabled) {
    border-color: var(--tuvtk-brand-primary);
    color: var(--tuvtk-brand-primary);
}

.editor-media-property-actions .is-danger {
    color: var(--color-error);
}

.editor-media-picker[hidden] {
    display: none;
}

.editor-media-picker {
    position: fixed;
    z-index: 1000;
    inset: 0;
    display: grid;
    place-items: center;
    padding: 1rem;
}

.editor-media-picker-backdrop {
    position: absolute;
    inset: 0;
    border: 0;
    background: rgb(23 33 43 / 0.55);
    cursor: default;
}

.editor-media-picker-panel {
    position: relative;
    display: grid;
    width: min(58rem, 100%);
    max-height: min(44rem, calc(100dvh - 2rem));
    overflow: hidden;
    border: 1px solid var(--editor-border);
    background: var(--tuvtk-panel-bg);
    box-shadow: 0 18px 55px rgb(23 33 43 / 0.28);
    grid-template-rows: auto minmax(0, 1fr) auto;
}

.editor-media-picker-header,
.editor-media-picker-footer,
.editor-media-library-toolbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
}

.editor-media-picker-header {
    border-bottom: 1px solid var(--editor-border);
    padding: 0.8rem 0.9rem;
}

.editor-media-picker-header h2 {
    color: var(--tuvtk-heading-text);
    font-size: 0.95rem;
    font-weight: 750;
}

.editor-media-picker-header p,
.editor-media-upload > p {
    margin-top: 0.15rem;
    color: var(--tuvtk-muted-text);
    font-size: 0.68rem;
}

.editor-media-picker-close {
    display: grid;
    width: 2rem;
    height: 2rem;
    flex: none;
    cursor: pointer;
    place-items: center;
    border-radius: var(--radius-field);
    color: var(--tuvtk-muted-text);
    font-size: 1.3rem;
}

.editor-media-picker-close:hover {
    background: var(--tuvtk-control-hover-bg);
    color: var(--tuvtk-brand-primary);
}

.editor-media-picker-body {
    display: grid;
    min-height: 0;
    grid-template-columns: minmax(0, 1fr) 16rem;
}

.editor-media-library {
    min-width: 0;
    min-height: 0;
    overflow-y: auto;
    padding: 0.8rem;
}

.editor-media-library-toolbar {
    margin-bottom: 0.65rem;
    color: var(--tuvtk-heading-text);
    font-size: 0.73rem;
}

.editor-media-feedback,
.editor-media-upload-error {
    margin-bottom: 0.65rem;
    border: 1px solid var(--tuvtk-border-default);
    background: var(--tuvtk-panel-muted-bg);
    padding: 0.45rem 0.55rem;
    color: var(--tuvtk-muted-text);
    font-size: 0.67rem;
    line-height: 1.35;
}

.editor-media-feedback.is-error,
.editor-media-upload-error {
    border-color: var(--color-error);
    color: var(--color-error);
}

.editor-media-picker-grid {
    display: grid;
    gap: 0.55rem;
    grid-template-columns: repeat(auto-fill, minmax(9.5rem, 1fr));
}

.editor-media-card {
    display: grid;
    min-width: 0;
    cursor: pointer;
    overflow: hidden;
    border: 1px solid var(--editor-border);
    border-radius: var(--radius-field);
    background: var(--tuvtk-panel-bg);
    text-align: left;
}

.editor-media-card:hover,
.editor-media-card:focus-visible,
.editor-media-card.is-selected {
    border-color: var(--editor-selected);
    outline: none;
    box-shadow: 0 0 0 2px rgb(22 65 148 / 0.14);
}

.editor-media-card.is-selected {
    background: var(--tuvtk-primary-tint-bg);
}

.editor-media-card-preview {
    display: grid;
    height: 6rem;
    place-items: center;
    border-bottom: 1px solid var(--editor-border);
    background: var(--editor-muted);
    padding: 0.35rem;
}

.editor-media-card-preview img {
    width: 100%;
    height: 100%;
    object-fit: contain;
}

.editor-media-card-copy {
    display: grid;
    min-width: 0;
    gap: 0.15rem;
    padding: 0.45rem 0.5rem;
}

.editor-media-card-copy strong,
.editor-media-card-copy small {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.editor-media-card-copy strong {
    color: var(--tuvtk-heading-text);
    font-size: 0.7rem;
}

.editor-media-card-copy small {
    color: var(--tuvtk-muted-text);
    font-size: 0.6rem;
}

.editor-media-picker-empty {
    display: grid;
    min-height: 12rem;
    place-content: center;
    gap: 0.3rem;
    border: 1px dashed var(--tuvtk-border-hover);
    color: var(--tuvtk-muted-text);
    font-size: 0.72rem;
    text-align: center;
}

.editor-media-picker-empty[hidden] {
    display: none;
}

.editor-media-picker-empty strong {
    color: var(--tuvtk-heading-text);
}

.editor-media-upload {
    overflow-y: auto;
    border-left: 1px solid var(--editor-border);
    background: var(--editor-muted);
    padding: 0.8rem;
}

.editor-media-upload h3 {
    color: var(--tuvtk-heading-text);
    font-size: 0.75rem;
    font-weight: 750;
}

.editor-media-upload form {
    margin-top: 0.75rem;
}

.editor-media-upload input[type="file"] {
    padding: 0.25rem;
    font-size: 0.62rem;
}

.editor-media-picker-footer {
    min-height: 3.25rem;
    border-top: 1px solid var(--editor-border);
    padding: 0.6rem 0.9rem;
    color: var(--tuvtk-muted-text);
    font-size: 0.68rem;
}

.editor-media-picker-footer > div {
    display: flex;
    gap: 0.45rem;
}

.editor-statusbar {
    position: sticky;
    z-index: 30;
    bottom: 0;
    display: grid;
    min-height: 2.8rem;
    align-items: center;
    border-top: 1px solid var(--editor-border);
    background: var(--tuvtk-panel-bg);
    color: var(--tuvtk-muted-text);
    font-size: 0.7rem;
    grid-template-columns: repeat(4, minmax(0, 1fr));
}

.editor-statusbar > span {
    display: flex;
    min-height: 1.8rem;
    align-items: center;
    justify-content: center;
    gap: 0.35rem;
    border-right: 1px solid var(--editor-border);
}

.editor-statusbar > span:last-child {
    border-right: 0;
}

.editor-save-status i {
    width: 0.65rem;
    height: 0.65rem;
    border-radius: 50%;
    background: var(--color-success);
}

.editor-save-status.is-dirty i {
    background: var(--color-warning);
}

.editor-save-status.is-saving i {
    background: var(--color-info);
}

.editor-save-status.is-error i {
    background: var(--color-error);
}

.diploma-preview-page {
    overflow: hidden;
    border: 1px solid var(--tuvtk-border-default);
    background: var(--tuvtk-panel-bg);
}

.preview-workspace {
    min-height: calc(100dvh - 15rem);
    overflow: auto;
    background: #eef2f6;
    padding: 2rem;
}

.preview-canvas-frame {
    position: relative;
    margin: 0 auto;
    transform-origin: top left;
}

.preview-canvas .diploma-element {
    cursor: default;
}

@media (max-width: 1199px) {
    .editor-workspace {
        grid-template-columns: 10.5rem minmax(28rem, 1fr) 16rem;
    }
}

@media (max-width: 899px) {
    .diploma-editor {
        min-height: 0;
        overflow: hidden;
    }

    .editor-heading,
    .preview-heading {
        align-items: flex-start;
        flex-direction: column;
    }

    .editor-heading-actions {
        align-self: flex-end;
    }

    .editor-workspace {
        min-height: 0;
        grid-template-columns: 10rem minmax(42rem, 1fr) 16rem;
        overflow-x: auto;
    }

    .editor-statusbar {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .editor-statusbar > span:nth-child(2) {
        border-right: 0;
    }

    .editor-media-picker {
        align-items: start;
        padding: 0.5rem;
    }

    .editor-media-picker-panel {
        max-height: calc(100dvh - 1rem);
    }

    .editor-media-picker-body {
        overflow-y: auto;
        grid-template-columns: 1fr;
    }

    .editor-media-library,
    .editor-media-upload {
        overflow: visible;
    }

    .editor-media-upload {
        border-top: 1px solid var(--editor-border);
        border-left: 0;
    }

    .editor-media-picker-footer {
        align-items: flex-start;
        flex-direction: column;
    }

    .editor-media-picker-footer > div {
        width: 100%;
        justify-content: flex-end;
    }
}
```

## `apps/diplome/static/diplome/template_editor.js`

Size: 73.5 KB

```javascript
(function () {
    "use strict";

    const root = document.getElementById("diploma-editor");
    if (!root || !window.DiplomaRenderer) return;
    const { mmToPx, pxToMm, pagePixelSize } = window.DiplomaRenderer;

    const layoutNode = document.getElementById("diploma-layout-data");
    const assetsNode = document.getElementById("diploma-media-assets-data");
    const canvas = document.getElementById("diploma-canvas");
    const stage = document.getElementById("editor-stage");
    const shell = document.getElementById("editor-canvas-shell");
    const viewport = document.getElementById("editor-canvas-viewport");
    const layersNode = document.getElementById("editor-layers");
    const propertiesNode = document.getElementById("editor-properties");
    const emptyPropertiesNode = document.getElementById("editor-empty-properties");
    const multiPropertiesNode = document.getElementById("editor-multi-properties");
    const topRuler = document.getElementById("editor-ruler-top");
    const leftRuler = document.getElementById("editor-ruler-left");
    const guideX = canvas.querySelector(".editor-guide-x");
    const guideY = canvas.querySelector(".editor-guide-y");
    const saveForm = document.getElementById("editor-save-form");
    const discardForm = document.getElementById("editor-discard-form");
    const mediaPicker = document.getElementById("editor-media-picker");
    const mediaPickerGrid = document.getElementById("editor-media-picker-grid");
    const mediaPickerEmpty = document.getElementById("editor-media-picker-empty");
    const mediaPickerFeedback = document.getElementById("editor-media-picker-feedback");
    const mediaPickerSelection = document.getElementById("editor-media-picker-selection");
    const mediaUploadForm = document.getElementById("editor-media-upload-form");
    const mediaUploadError = document.getElementById("editor-media-upload-error");
    const mediaPreviewNode = document.getElementById("editor-media-current-preview");
    const iconPreviewNode = document.getElementById("editor-icon-current-preview");
    const customGuidesNode = document.getElementById("editor-custom-guides");
    const guidePositionNode = document.getElementById("editor-guide-position");
    const inspectorTabs = Array.from(root.querySelectorAll("[data-inspector-tab]"));
    const inspectorPanels = Array.from(root.querySelectorAll("[data-inspector-panel]"));
    const confirmDialog = document.getElementById("editor-confirm-dialog");
    const confirmTitle = document.getElementById("editor-confirm-title");
    const confirmMessage = document.getElementById("editor-confirm-message");
    const confirmAccept = confirmDialog.querySelector("[data-confirm-accept]");
    const confirmCancel = document.getElementById("editor-confirm-cancel");
    const mediaAssets = assetsNode ? JSON.parse(assetsNode.textContent) : [];
    const mediaAssetsById = new Map(mediaAssets.map((asset) => [asset.id, asset]));
    const FITTABLE_TYPES = new Set(["text", "variable", "list", "image", "icon"]);
    const MIN_ZOOM = 0.1;
    const MAX_ZOOM = 2.5;
    const ZOOM_STEP = 0.1;
    const RULER_SIZE_PX = 27;
    let isDraftTemplate = root.dataset.isDraftTemplate === "true";

    const state = {
        layout: JSON.parse(layoutNode.textContent),
        selectedId: null,
        selectedIds: [],
        zoom: 0.75,
        zoomMode: "fit",
        gridVisible: true,
        guidesVisible: true,
        dirty: false,
        saving: false,
        leaving: false,
        revision: 0,
        history: [],
        historyIndex: 0,
        savedSnapshot: "",
    };
    state.layout.guides ??= { vertical: [], horizontal: [] };
    const pickerState = {
        mode: null,
        selectedAssetId: null,
        returnFocus: null,
    };
    state.layout.elements.forEach((element) => {
        if (["text", "variable", "list"].includes(element.type)) {
            element.style.lineHeight ??= 1.18;
            element.style.letterSpacing ??= 0;
            element.style.textTransform ??= "none";
        }
    });
    state.selectedId = state.layout.elements.find((item) => item.id === "full_name")?.id
        || state.layout.elements[0]?.id
        || null;
    state.selectedIds = state.selectedId ? [state.selectedId] : [];
    state.savedSnapshot = JSON.stringify(state.layout);
    state.history = [state.savedSnapshot];

    const VARIABLE_LABELS = {
        full_name: "Nume complet",
        date_of_birth: "Data nașterii",
        place_of_birth: "Locul nașterii",
        certificate_number: "Număr certificat",
    };

    const assetSelect = propertiesNode.querySelector('[data-prop="assetId"]');

    function assetKindLabel(asset) {
        return asset.kind === "svg" ? "SVG" : "Raster";
    }

    function assetDetails(asset) {
        const dimensions = asset.width && asset.height
            ? `${asset.width} × ${asset.height} px`
            : "Dimensiuni nespecificate";
        const size = Number.isFinite(asset.sizeBytes)
            ? `${Math.max(1, Math.round(asset.sizeBytes / 1024))} KB`
            : "";
        return [assetKindLabel(asset), dimensions, size].filter(Boolean).join(" · ");
    }

    function selectedElement() {
        return state.layout.elements.find((element) => element.id === state.selectedId) || null;
    }

    function selectedElements() {
        const ids = new Set(state.selectedIds);
        return state.layout.elements.filter((element) => ids.has(element.id));
    }

    function setSelection(ids) {
        const existing = new Set(state.layout.elements.map((element) => element.id));
        state.selectedIds = [...new Set(ids)].filter((id) => existing.has(id));
        state.selectedId = state.selectedIds.length === 1 ? state.selectedIds[0] : null;
    }

    function snap(value) {
        return Math.round(value / state.layout.page.grid_mm) * state.layout.page.grid_mm;
    }

    function clamp(value, minimum, maximum) {
        return Math.min(Math.max(value, minimum), maximum);
    }

    function setInspectorTab(tabName, { focus = false } = {}) {
        const activeTab = inspectorTabs.find((tab) => tab.dataset.inspectorTab === tabName);
        const activePanel = inspectorPanels.find((panel) => panel.dataset.inspectorPanel === tabName);
        if (!activeTab || !activePanel) return;

        inspectorTabs.forEach((tab) => {
            const isActive = tab === activeTab;
            tab.classList.toggle("is-active", isActive);
            tab.setAttribute("aria-selected", String(isActive));
            tab.tabIndex = isActive ? 0 : -1;
        });
        inspectorPanels.forEach((panel) => {
            panel.hidden = panel !== activePanel;
        });
        if (focus) activeTab.focus();
    }

    function viewportContentSize() {
        const style = window.getComputedStyle(viewport);
        const horizontalPadding = Number.parseFloat(style.paddingLeft)
            + Number.parseFloat(style.paddingRight);
        const verticalPadding = Number.parseFloat(style.paddingTop)
            + Number.parseFloat(style.paddingBottom);
        return {
            width: Math.max(1, viewport.clientWidth - horizontalPadding),
            height: Math.max(1, viewport.clientHeight - verticalPadding),
        };
    }

    function fittedPageZoom() {
        const pageSize = pagePixelSize(state.layout);
        const available = viewportContentSize();
        return clamp(Math.min(
            (available.width - RULER_SIZE_PX) / pageSize.width,
            (available.height - RULER_SIZE_PX) / pageSize.height,
            1
        ), MIN_ZOOM, MAX_ZOOM);
    }

    function syncZoomControl() {
        const control = root.querySelector('[data-action="zoom"]');
        const customOption = control.querySelector("[data-zoom-custom]");
        if (state.zoomMode === "fit") {
            customOption.hidden = true;
            control.value = "fit";
            return;
        }

        const matchingOption = Array.from(control.options).find((option) => (
            option !== customOption
            && Number.isFinite(Number.parseFloat(option.value))
            && Math.abs(Number.parseFloat(option.value) - state.zoom) < 0.001
        ));
        if (matchingOption) {
            customOption.hidden = true;
            control.value = matchingOption.value;
            return;
        }

        customOption.value = state.zoom.toFixed(2);
        customOption.textContent = `${Math.round(state.zoom * 100)}%`;
        customOption.hidden = false;
        control.value = customOption.value;
    }

    function setZoom(nextZoom, anchor = {}) {
        const previousZoom = state.zoom;
        const viewportRect = viewport.getBoundingClientRect();
        const stageRect = stage.getBoundingClientRect();
        const clientX = anchor.clientX ?? viewportRect.left + viewportRect.width / 2;
        const clientY = anchor.clientY ?? viewportRect.top + viewportRect.height / 2;
        const pageX = (clientX - stageRect.left) / previousZoom;
        const pageY = (clientY - stageRect.top) / previousZoom;

        state.zoomMode = "manual";
        state.zoom = clamp(Math.round(nextZoom * 100) / 100, MIN_ZOOM, MAX_ZOOM);
        renderCanvas();
        renderStatus();
        window.requestAnimationFrame(() => {
            const updatedStageRect = stage.getBoundingClientRect();
            viewport.scrollLeft += updatedStageRect.left + pageX * state.zoom - clientX;
            viewport.scrollTop += updatedStageRect.top + pageY * state.zoom - clientY;
        });
    }

    function changeZoom(direction, anchor = {}) {
        setZoom(state.zoom + direction * ZOOM_STEP, anchor);
    }

    function fitPage() {
        state.zoomMode = "fit";
        state.zoom = fittedPageZoom();
        renderCanvas();
        renderStatus();
        window.requestAnimationFrame(() => viewport.scrollTo({ left: 0, top: 0 }));
    }

    function refreshFittedZoom() {
        if (state.zoomMode !== "fit") return;
        const nextZoom = fittedPageZoom();
        if (Math.abs(nextZoom - state.zoom) < 0.005) return;
        state.zoom = nextZoom;
        renderCanvas();
        renderStatus();
    }

    function uniqueId(prefix) {
        return `${prefix}_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 6)}`;
    }

    function typography(size = 24, bold = false) {
        return {
            fontFamily: "Lora",
            fontSize: size,
            bold,
            italic: false,
            underline: false,
            color: "#164194",
            align: "center",
            lineHeight: 1.18,
            letterSpacing: 0,
            textTransform: "none",
        };
    }

    function baseElement(type, label, width_mm, height_mm) {
        const page = state.layout.page;
        return {
            id: uniqueId("el"),
            type,
            label,
            x_mm: snap(Math.max(0, (page.width_mm - width_mm) / 2)),
            y_mm: snap(Math.max(0, (page.height_mm - height_mm) / 2)),
            width_mm,
            height_mm,
            rotation: 0,
            zIndex: Math.min(1000, Math.max(1, ...state.layout.elements.map((item) => item.zIndex + 1))),
            locked: false,
            visible: true,
        };
    }

    function layoutSnapshot() {
        return JSON.stringify(state.layout);
    }

    function renderHistoryControls() {
        root.querySelector('[data-action="undo"]').disabled = state.historyIndex <= 0;
        root.querySelector('[data-action="redo"]').disabled = state.historyIndex >= state.history.length - 1;
    }

    function recordHistory() {
        const snapshot = layoutSnapshot();
        if (snapshot === state.history[state.historyIndex]) return;
        state.history.splice(state.historyIndex + 1);
        state.history.push(snapshot);
        if (state.history.length > 100) state.history.shift();
        state.historyIndex = state.history.length - 1;
    }

    function updateDirtyStatus() {
        state.dirty = layoutSnapshot() !== state.savedSnapshot;
        setSaveStatus(
            state.dirty ? "dirty" : "saved",
            state.dirty ? "Modificări nesalvate" : "Modificări salvate",
        );
    }

    function markDirty() {
        recordHistory();
        state.revision += 1;
        updateDirtyStatus();
        renderHistoryControls();
    }

    function restoreHistory(offset) {
        const targetIndex = state.historyIndex + offset;
        if (targetIndex < 0 || targetIndex >= state.history.length) return;
        state.historyIndex = targetIndex;
        state.layout = JSON.parse(state.history[state.historyIndex]);
        setSelection(state.selectedIds);
        state.revision += 1;
        updateDirtyStatus();
        renderAll();
    }

    function setSaveStatus(mode, label) {
        const node = root.querySelector('[data-status="save"]');
        node.classList.remove("is-dirty", "is-saving", "is-error");
        if (mode !== "saved") node.classList.add(`is-${mode}`);
        node.querySelector("strong").textContent = label;
    }

    function renderRulers() {
        const page = state.layout.page;
        const pageSize = pagePixelSize(state.layout);
        topRuler.replaceChildren();
        leftRuler.replaceChildren();
        topRuler.style.width = `${pageSize.width * state.zoom}px`;
        leftRuler.style.height = `${pageSize.height * state.zoom}px`;
        topRuler.style.backgroundSize = `${mmToPx(page.grid_mm) * state.zoom}px 100%`;
        leftRuler.style.backgroundSize = `100% ${mmToPx(page.grid_mm) * state.zoom}px`;
        for (let value = 0; value <= page.width_mm; value += page.major_grid_mm) {
            const label = document.createElement("span");
            label.className = "editor-ruler-label";
            label.style.left = `${mmToPx(value) * state.zoom}px`;
            label.textContent = String(value);
            topRuler.appendChild(label);
        }
        for (let value = 0; value <= page.height_mm; value += page.major_grid_mm) {
            const label = document.createElement("span");
            label.className = "editor-ruler-label";
            label.style.top = `${mmToPx(value) * state.zoom}px`;
            label.textContent = String(value);
            leftRuler.appendChild(label);
        }
    }

    function renderCustomGuides() {
        canvas.querySelectorAll(".editor-guide-custom").forEach((node) => node.remove());
        const appendGuide = (orientation, position) => {
            const guide = document.createElement("div");
            guide.className = `editor-guide editor-guide-custom ${orientation === "vertical" ? "editor-guide-x" : "editor-guide-y"}`;
            guide.dataset.guideOrientation = orientation;
            guide.dataset.guidePosition = String(position);
            guide.hidden = !state.guidesVisible;
            if (orientation === "vertical") guide.style.left = `${mmToPx(position)}px`;
            else guide.style.top = `${mmToPx(position)}px`;
            canvas.appendChild(guide);
        };
        state.layout.guides.vertical.forEach((position) => appendGuide("vertical", position));
        state.layout.guides.horizontal.forEach((position) => appendGuide("horizontal", position));
    }

    function renderGuideControls() {
        customGuidesNode.replaceChildren();
        const addChip = (orientation, position) => {
            const button = document.createElement("button");
            button.type = "button";
            button.textContent = `${orientation === "vertical" ? "V" : "O"} ${position} mm ×`;
            button.title = "Elimină ghidajul";
            button.addEventListener("click", () => {
                state.layout.guides[orientation] = state.layout.guides[orientation]
                    .filter((value) => value !== position);
                markDirty();
                renderCanvas();
                renderGuideControls();
            });
            customGuidesNode.appendChild(button);
        };
        state.layout.guides.vertical.forEach((position) => addChip("vertical", position));
        state.layout.guides.horizontal.forEach((position) => addChip("horizontal", position));
    }

    function addCustomGuide(orientation) {
        const limit = orientation === "vertical"
            ? state.layout.page.width_mm
            : state.layout.page.height_mm;
        const position = clamp(Number.parseInt(guidePositionNode.value, 10) || 0, 0, limit);
        if (!state.layout.guides[orientation].includes(position)) {
            state.layout.guides[orientation].push(position);
            state.layout.guides[orientation].sort((left, right) => left - right);
            markDirty();
        }
        state.guidesVisible = true;
        const toggle = root.querySelector('[data-action="toggle-guides"]');
        toggle.classList.add("is-active");
        toggle.setAttribute("aria-pressed", "true");
        renderCanvas();
        renderGuideControls();
    }

    function renderCanvas() {
        const page = state.layout.page;
        const pageSize = pagePixelSize(state.layout);
        if (state.zoomMode === "fit") state.zoom = fittedPageZoom();
        window.DiplomaRenderer.render(canvas, state.layout, {
            editable: true,
            selectedId: state.selectedId,
            selectedIds: state.selectedIds,
            assets: mediaAssetsById,
        });
        renderCustomGuides();
        canvas.classList.toggle("has-grid", state.gridVisible);
        stage.style.transform = `scale(${state.zoom})`;
        stage.style.width = `${pageSize.width}px`;
        stage.style.height = `${pageSize.height}px`;
        shell.style.width = `${pageSize.width * state.zoom + 27}px`;
        shell.style.height = `${pageSize.height * state.zoom + 27}px`;
        renderRulers();
    }

    function fittedMediaSize(element) {
        if (element.type === "icon" && !element.assetId) {
            const size = Math.min(element.width_mm, element.height_mm);
            return { width_mm: size, height_mm: size };
        }
        const asset = mediaAssetsById.get(element.assetId);
        if (!asset?.width || !asset?.height) return null;
        if (element.type === "image" && element.style.fit !== "contain") return null;
        const ratio = asset.width / asset.height;
        if (element.width_mm / element.height_mm > ratio) {
            return {
                width_mm: Math.max(1, Math.ceil(element.height_mm * ratio)),
                height_mm: element.height_mm,
            };
        }
        return {
            width_mm: element.width_mm,
            height_mm: Math.max(1, Math.ceil(element.width_mm / ratio)),
        };
    }

    function measuredContentSize(element) {
        const elementNode = canvas.querySelector(`[data-element-id="${CSS.escape(element.id)}"]`);
        const contentNode = elementNode?.firstElementChild;
        if (!contentNode) return null;
        const originalStyle = contentNode.getAttribute("style");
        contentNode.style.width = "max-content";
        contentNode.style.height = "auto";
        contentNode.style.flex = "none";
        contentNode.style.maxWidth = "none";
        contentNode.style.maxHeight = "none";
        contentNode.style.overflow = "visible";
        const maxWidth = mmToPx(state.layout.page.width_mm - element.x_mm);
        let width = Math.min(contentNode.scrollWidth + 2, maxWidth);
        if (contentNode.scrollWidth > maxWidth) contentNode.style.width = `${maxWidth}px`;
        const height = contentNode.scrollHeight + 2;
        if (originalStyle === null) contentNode.removeAttribute("style");
        else contentNode.setAttribute("style", originalStyle);
        return {
            width_mm: Math.max(1, Math.ceil(pxToMm(width))),
            height_mm: Math.max(1, Math.ceil(pxToMm(height))),
        };
    }

    function fitElementToContent(element) {
        if (!element || element.locked || !FITTABLE_TYPES.has(element.type)) return false;
        const size = ["text", "variable", "list"].includes(element.type)
            ? measuredContentSize(element)
            : fittedMediaSize(element);
        if (!size) return false;
        const width = clamp(size.width_mm, 1, state.layout.page.width_mm - element.x_mm);
        const height = clamp(size.height_mm, 1, state.layout.page.height_mm - element.y_mm);
        if (width === element.width_mm && height === element.height_mm) return false;
        element.width_mm = width;
        element.height_mm = height;
        return true;
    }

    function fitSelectedToContent() {
        const element = selectedElement();
        if (!fitElementToContent(element)) return;
        markDirty();
        renderAll();
    }

    function iconButton(label, text, action) {
        const button = document.createElement("button");
        button.type = "button";
        button.title = label;
        button.setAttribute("aria-label", label);
        button.textContent = text;
        button.addEventListener("click", (event) => {
            event.stopPropagation();
            action();
        });
        return button;
    }

    function replaceMediaAssets(assets) {
        mediaAssets.splice(0, mediaAssets.length, ...assets);
        mediaAssetsById.clear();
        mediaAssets.forEach((asset) => mediaAssetsById.set(asset.id, asset));
    }

    function renderAssetSelect(element) {
        assetSelect.replaceChildren();
        mediaAssets.forEach((asset) => {
            const option = document.createElement("option");
            option.value = asset.id;
            option.textContent = asset.name;
            assetSelect.appendChild(option);
        });
        if (element.assetId && !mediaAssetsById.has(element.assetId)) {
            const missingOption = document.createElement("option");
            missingOption.value = element.assetId;
            missingOption.textContent = "Fișier media indisponibil";
            assetSelect.prepend(missingOption);
        }
        if (!assetSelect.options.length) {
            const emptyOption = document.createElement("option");
            emptyOption.value = "";
            emptyOption.textContent = "Niciun fișier disponibil";
            emptyOption.disabled = true;
            assetSelect.appendChild(emptyOption);
        }
        assetSelect.value = element.assetId || "";
    }

    function renderMediaPreview(element, targetNode = mediaPreviewNode) {
        targetNode.replaceChildren();
        const asset = mediaAssetsById.get(element.assetId);
        if (!asset) {
            const unavailable = document.createElement("span");
            unavailable.className = "editor-media-current-unavailable";
            unavailable.textContent = element.type === "icon"
                ? "Se folosește iconul inclus"
                : "Fișier media indisponibil";
            targetNode.appendChild(unavailable);
            return;
        }
        const image = document.createElement("img");
        image.src = asset.url;
        image.alt = element.alt || asset.name;
        const details = document.createElement("span");
        const name = document.createElement("strong");
        const metadata = document.createElement("small");
        name.textContent = asset.name;
        metadata.textContent = assetDetails(asset);
        details.append(name, metadata);
        targetNode.append(image, details);
    }

    function setPickerFeedback(message = "", mode = "status") {
        mediaPickerFeedback.hidden = !message;
        mediaPickerFeedback.textContent = message;
        mediaPickerFeedback.classList.toggle("is-error", mode === "error");
    }

    function renderMediaPicker() {
        mediaPickerGrid.replaceChildren();
        mediaPickerEmpty.hidden = mediaAssets.length > 0;
        mediaAssets.forEach((asset) => {
            const button = document.createElement("button");
            button.type = "button";
            button.className = "editor-media-card";
            button.dataset.assetId = asset.id;
            button.setAttribute("role", "option");
            const selected = pickerState.selectedAssetId === asset.id;
            button.classList.toggle("is-selected", selected);
            button.setAttribute("aria-selected", String(selected));

            const preview = document.createElement("span");
            preview.className = "editor-media-card-preview";
            const image = document.createElement("img");
            image.src = asset.url;
            image.alt = "";
            image.loading = "lazy";
            preview.appendChild(image);

            const copy = document.createElement("span");
            copy.className = "editor-media-card-copy";
            const name = document.createElement("strong");
            const metadata = document.createElement("small");
            name.textContent = asset.name;
            metadata.textContent = assetDetails(asset);
            copy.append(name, metadata);
            button.append(preview, copy);
            button.addEventListener("click", () => {
                pickerState.selectedAssetId = asset.id;
                renderMediaPicker();
                mediaPickerGrid.querySelector(`[data-asset-id="${asset.id}"]`)?.focus();
            });
            mediaPickerGrid.appendChild(button);
        });

        const selectedAsset = mediaAssetsById.get(pickerState.selectedAssetId);
        mediaPickerSelection.textContent = selectedAsset
            ? `Selectat: ${selectedAsset.name}`
            : "Niciun fișier selectat";
        root.querySelector('[data-action="apply-media-asset"]').disabled = !selectedAsset;
    }

    function openMediaPicker(mode, trigger = document.activeElement) {
        const element = selectedElement();
        pickerState.mode = mode;
        pickerState.returnFocus = trigger;
        pickerState.selectedAssetId = ["replace", "replace-background", "replace-icon"].includes(mode) && mediaAssetsById.has(element?.assetId)
            ? element.assetId
            : null;
        const descriptions = {
            "create-image": "Alege fișierul pentru imaginea nouă.",
            "create-background": "Alege fișierul care va acoperi fundalul paginii.",
            replace: "Alege fișierul care va înlocui selecția curentă.",
            "replace-background": "Alege fișierul care va înlocui fundalul curent.",
            "replace-icon": "Alege sau încarcă grafica folosită de icon.",
        };
        document.getElementById("editor-media-picker-description").textContent = descriptions[mode];
        setPickerFeedback();
        mediaUploadError.hidden = true;
        mediaUploadError.textContent = "";
        renderMediaPicker();
        mediaPicker.hidden = false;
        window.requestAnimationFrame(() => {
            const selectedCard = mediaPickerGrid.querySelector(".is-selected");
            (selectedCard || mediaPickerGrid.querySelector("button") || mediaUploadForm.elements.file).focus();
        });
    }

    function closeMediaPicker() {
        if (mediaPicker.hidden) return;
        mediaPicker.hidden = true;
        const returnFocus = pickerState.returnFocus;
        pickerState.mode = null;
        pickerState.selectedAssetId = null;
        if (returnFocus instanceof HTMLElement) returnFocus.focus();
    }

    async function fetchMediaAssets() {
        const response = await fetch(root.dataset.mediaAssetsApiUrl, {
            headers: { "Accept": "application/json" },
        });
        const payload = await response.json().catch(() => ({}));
        if (!response.ok || !Array.isArray(payload.assets)) {
            throw new Error("Biblioteca media nu a putut fi reîmprospătată.");
        }
        replaceMediaAssets(payload.assets);
    }

    async function refreshMediaAssets() {
        const refreshButton = root.querySelector('[data-action="refresh-media-assets"]');
        refreshButton.disabled = true;
        setPickerFeedback("Se reîmprospătează biblioteca…");
        try {
            await fetchMediaAssets();
            if (!mediaAssetsById.has(pickerState.selectedAssetId)) {
                pickerState.selectedAssetId = null;
            }
            setPickerFeedback("Biblioteca media a fost actualizată.");
            renderMediaPicker();
            renderProperties();
            renderCanvas();
        } catch (error) {
            setPickerFeedback(error.message, "error");
        } finally {
            refreshButton.disabled = false;
        }
    }

    function applyMediaAsset() {
        const asset = mediaAssetsById.get(pickerState.selectedAssetId);
        if (!asset) return;
        if (pickerState.mode === "create-image") {
            addElement({
                ...baseElement("image", "Imagine", 58, 37),
                style: { fit: "contain", opacity: 1 },
                assetId: asset.id,
                alt: asset.name,
            }, { fitContent: true });
        } else if (pickerState.mode === "create-background") {
            if (state.layout.elements.some((element) => element.type === "background")) {
                setPickerFeedback("Template-ul poate avea un singur fundal.", "error");
                return;
            }
            const element = baseElement(
                "background",
                "Fundal",
                state.layout.page.width_mm,
                state.layout.page.height_mm,
            );
            Object.assign(element, {
                x_mm: 0,
                y_mm: 0,
                zIndex: 0,
                locked: true,
                style: { fit: "cover", opacity: 1 },
                assetId: asset.id,
                alt: "",
            });
            addElement(element);
        } else if (["replace", "replace-background", "replace-icon"].includes(pickerState.mode)) {
            const element = selectedElement();
            const backgroundWorkflow = pickerState.mode === "replace-background" && element?.type === "background";
            const iconWorkflow = pickerState.mode === "replace-icon" && element?.type === "icon";
            if (!element || !["image", "background", "icon"].includes(element.type)
                || (element.locked && !backgroundWorkflow)
                || (pickerState.mode === "replace-icon" && !iconWorkflow)) return;
            if (element.assetId !== asset.id) {
                element.assetId = asset.id;
                if (!element.alt) element.alt = asset.name;
                markDirty();
                renderAll();
            }
        }
        closeMediaPicker();
    }

    async function removeIconAsset() {
        const element = selectedElement();
        if (!element || element.type !== "icon" || element.locked || !element.assetId) return;
        const confirmed = await requestConfirmation({
            title: "Revii la iconul inclus?",
            message: "Grafica personalizată va fi scoasă din element. Fișierul rămâne în biblioteca media.",
            acceptLabel: "Revino",
        });
        if (!confirmed) return;
        delete element.assetId;
        delete element.alt;
        markDirty();
        renderAll();
    }

    let confirmationResolver = null;

    function closeConfirmation(result) {
        if (!confirmationResolver) return;
        const resolve = confirmationResolver;
        confirmationResolver = null;
        if (confirmDialog.open) confirmDialog.close();
        resolve(result);
    }

    function requestConfirmation({
        title,
        message,
        acceptLabel = "Șterge",
        cancelLabel = "Renunță",
    }) {
        if (confirmationResolver) closeConfirmation(false);
        confirmTitle.textContent = title;
        confirmMessage.textContent = message;
        confirmAccept.textContent = acceptLabel;
        confirmCancel.textContent = cancelLabel;
        confirmDialog.showModal();
        return new Promise((resolve) => {
            confirmationResolver = resolve;
            window.requestAnimationFrame(() => confirmAccept.focus());
        });
    }

    async function removeSelectedMediaElement() {
        const element = selectedElement();
        if (!element || !["image", "background"].includes(element.type)) return;
        await deleteElements([element.id], {
            allowLockedBackground: element.type === "background",
            confirmDelete: true,
        });
    }

    async function deleteElements(
        ids = state.selectedIds,
        { allowLockedBackground = false, confirmDelete = false } = {},
    ) {
        const idSet = new Set(ids);
        const targets = state.layout.elements.filter((element) => idSet.has(element.id));
        const deletable = targets.filter(
            (element) => !element.locked || (allowLockedBackground && element.type === "background"),
        );
        if (!deletable.length) return;
        if (confirmDelete || deletable.some((element) => element.type === "background")) {
            const hasBackground = deletable.some((element) => element.type === "background");
            const confirmed = await requestConfirmation({
                title: hasBackground ? "Elimini fundalul?" : "Elimini elementul media?",
                message: "Elementul va fi eliminat din template. Fișierul original rămâne în biblioteca media.",
            });
            if (!confirmed) return;
        }
        const firstIndex = Math.min(...deletable.map((element) => state.layout.elements.indexOf(element)));
        const deletedIds = new Set(deletable.map((element) => element.id));
        state.layout.elements = state.layout.elements.filter((element) => !deletedIds.has(element.id));
        const next = state.layout.elements[Math.min(firstIndex, state.layout.elements.length - 1)];
        setSelection(next ? [next.id] : []);
        markDirty();
        renderAll();
    }

    function duplicateElements(ids = state.selectedIds) {
        const idSet = new Set(ids);
        const originals = state.layout.elements.filter(
            (element) => idSet.has(element.id) && !element.locked && element.type !== "background",
        );
        if (!originals.length) return;
        let nextZ = Math.max(0, ...state.layout.elements.map((element) => element.zIndex));
        const copies = originals.map((element) => {
            const copy = JSON.parse(JSON.stringify(element));
            copy.id = uniqueId(element.type);
            copy.label = `${element.label} copie`.slice(0, 120);
            copy.x_mm = clamp(element.x_mm + 5, 0, state.layout.page.width_mm - element.width_mm);
            copy.y_mm = clamp(element.y_mm + 5, 0, state.layout.page.height_mm - element.height_mm);
            nextZ = Math.min(1000, nextZ + 1);
            copy.zIndex = nextZ;
            return copy;
        });
        state.layout.elements.push(...copies);
        setSelection(copies.map((element) => element.id));
        markDirty();
        renderAll();
    }

    function renderLayers() {
        layersNode.replaceChildren();
        [...state.layout.elements]
            .sort((left, right) => right.zIndex - left.zIndex)
            .forEach((element) => {
                const row = document.createElement("div");
                row.className = "editor-layer";
                row.dataset.elementId = element.id;
                row.classList.toggle("is-selected", state.selectedIds.includes(element.id));
                row.tabIndex = 0;

                const drag = document.createElement("span");
                drag.className = "editor-layer-drag";
                drag.textContent = "⠿";
                const name = document.createElement("span");
                name.className = "editor-layer-name";
                name.textContent = element.label;
                name.title = element.label;
                row.append(drag, name);
                row.appendChild(iconButton(
                    element.visible ? "Ascunde stratul" : "Afișează stratul",
                    element.visible ? "◉" : "○",
                    () => {
                        element.visible = !element.visible;
                        markDirty();
                        renderAll();
                    },
                ));
                row.appendChild(iconButton(
                    element.locked ? "Deblochează stratul" : "Blochează stratul",
                    element.locked ? "▣" : "□",
                    () => {
                        element.locked = !element.locked;
                        markDirty();
                        renderAll();
                    },
                ));
                row.appendChild(iconButton("Duplică stratul", "⧉", () => duplicateElements([element.id])));
                row.appendChild(iconButton(
                    "Șterge stratul",
                    "×",
                    () => deleteElements(
                        [element.id],
                        { allowLockedBackground: element.type === "background" },
                    ),
                ));
                row.addEventListener("click", (event) => selectElement(element.id, event));
                row.addEventListener("keydown", (event) => {
                    if (event.key === "Enter" || event.key === " ") selectElement(element.id, event);
                });
                layersNode.appendChild(row);
            });
    }

    function setFieldValue(selector, value) {
        const node = propertiesNode.querySelector(selector);
        if (!node) return;
        if (node.type === "checkbox") node.checked = Boolean(value);
        else node.value = value ?? "";
    }

    function renderProperties() {
        const element = selectedElement();
        propertiesNode.hidden = !element;
        const multiple = state.selectedIds.length > 1;
        emptyPropertiesNode.hidden = Boolean(element) || multiple;
        multiPropertiesNode.hidden = !multiple;
        multiPropertiesNode.querySelector("[data-multi-count]").textContent = `${state.selectedIds.length} elemente selectate`;
        document.getElementById("property-lock-indicator").textContent = element?.locked ? "▣" : "○";
        if (!element) return;

        ["x_mm", "y_mm", "width_mm", "height_mm", "rotation", "zIndex", "label", "text", "placeholder", "variable", "alt", "iconName"]
            .forEach((key) => setFieldValue(`[data-prop="${key}"]`, element[key]));

        const hasTypography = ["text", "variable", "list"].includes(element.type);
        propertiesNode.querySelector('[data-section="typography"]').hidden = !hasTypography;
        if (hasTypography) {
            ["fontFamily", "fontSize", "color", "align", "lineHeight", "letterSpacing", "textTransform"].forEach((key) => {
                setFieldValue(`[data-style="${key}"]`, element.style[key]);
            });
            propertiesNode.querySelectorAll("[data-style-toggle]").forEach((button) => {
                button.setAttribute("aria-pressed", String(Boolean(element.style[button.dataset.styleToggle])));
            });
        }
        const hasList = element.type === "list";
        propertiesNode.querySelector('[data-section="list"]').hidden = !hasList;
        if (hasList) {
            ["listType", "indent_mm"].forEach((key) => {
                setFieldValue(`[data-style="${key}"]`, element.style[key]);
            });
            propertiesNode.querySelector("[data-list-items]").value = element.items.join("\n");
        }
        const hasMedia = element.type === "image" || element.type === "background";
        propertiesNode.querySelector('[data-section="media"]').hidden = !hasMedia;
        if (hasMedia) {
            renderAssetSelect(element);
            renderMediaPreview(element);
            ["fit", "opacity"].forEach((key) => {
                setFieldValue(`[data-style="${key}"]`, element.style[key]);
            });
        }
        const hasIcon = element.type === "icon";
        propertiesNode.querySelector('[data-section="icon"]').hidden = !hasIcon;
        if (hasIcon) {
            renderMediaPreview(element, iconPreviewNode);
            ["color", "opacity"].forEach((key) => {
                setFieldValue(`[data-icon-style="${key}"]`, element.style[key]);
            });
            propertiesNode.querySelector('[data-action="remove-icon-asset"]').disabled = !element.assetId;
        }
        const hasTable = element.type === "table";
        propertiesNode.querySelector('[data-section="table"]').hidden = !hasTable;
        if (hasTable) {
            propertiesNode.querySelector("[data-table-columns]").value = element.columns.join("\n");
            propertiesNode.querySelector("[data-table-rows]").value = element.rows
                .map((row) => row.join(" | "))
                .join("\n");
            ["fontFamily", "fontSize", "bold", "color", "align", "borderColor", "headerBackground"]
                .forEach((key) => setFieldValue(`[data-table-style="${key}"]`, element.style[key]));
        }
        propertiesNode.querySelector('[data-content-field="text"]').hidden = element.type !== "text";
        propertiesNode.querySelector('[data-content-field="placeholder"]').hidden = element.type !== "variable";
        propertiesNode.querySelector('[data-content-field="variable"]').hidden = element.type !== "variable";
        propertiesNode.querySelectorAll("input, select, textarea, button").forEach((control) => {
            control.disabled = element.locked;
        });
        if (element.type === "icon") {
            propertiesNode.querySelector('[data-action="remove-icon-asset"]').disabled = element.locked || !element.assetId;
        }
        if (element.type === "background") {
            ["x_mm", "y_mm", "width_mm", "height_mm", "rotation", "zIndex"].forEach((key) => {
                propertiesNode.querySelector(`[data-prop="${key}"]`).disabled = true;
            });
            [
                '[data-prop="assetId"]', '[data-prop="alt"]', '[data-style="fit"]',
                '[data-style="opacity"]', '[data-action="open-media-picker"]',
                '[data-action="remove-media-element"]',
            ].forEach((selector) => {
                propertiesNode.querySelector(selector).disabled = false;
            });
        }
    }

    function renderAlignmentState() {
        const unlockedCount = selectedElements().filter(
            (element) => !element.locked && element.type !== "background"
        ).length;
        root.querySelectorAll("[data-align]").forEach((button) => {
            button.disabled = unlockedCount < 1;
        });
        root.querySelectorAll("[data-distribute]").forEach((button) => {
            button.disabled = unlockedCount < 3;
        });
        const element = selectedElement();
        root.querySelector('[data-action="fit-content"]').disabled = !(
            element && !element.locked && FITTABLE_TYPES.has(element.type)
        );
    }

    function renderStatus() {
        root.querySelector('[data-status="grid"]').textContent = `${state.layout.page.grid_mm} mm / ${state.layout.page.major_grid_mm} mm`;
        root.querySelector('[data-status="zoom"]').textContent = `${Math.round(state.zoom * 100)}%`;
        root.querySelector('[data-status="page"]').textContent = `${state.layout.page.size} ${state.layout.page.orientation}`;
        syncZoomControl();
    }

    function renderAll() {
        renderCanvas();
        renderLayers();
        renderProperties();
        renderAlignmentState();
        renderStatus();
        renderHistoryControls();
        renderGuideControls();
    }

    function selectElement(elementId, event = {}) {
        if (event.shiftKey || event.ctrlKey || event.metaKey) {
            const ids = new Set(state.selectedIds);
            if (ids.has(elementId)) ids.delete(elementId);
            else ids.add(elementId);
            setSelection([...ids]);
        } else {
            setSelection([elementId]);
        }
        renderAll();
    }

    function addElement(element, { fitContent = false } = {}) {
        state.layout.elements.push(element);
        setSelection([element.id]);
        renderCanvas();
        if (fitContent && fitElementToContent(element)) {
            element.x_mm = snap(Math.max(0, (state.layout.page.width_mm - element.width_mm) / 2));
            element.y_mm = snap(Math.max(0, (state.layout.page.height_mm - element.height_mm) / 2));
        }
        markDirty();
        renderAll();
    }

    function addText() {
        addElement({
            ...baseElement("text", "Text nou", 85, 13),
            style: typography(24),
            text: "Text nou",
        }, { fitContent: true });
    }

    function addList() {
        addElement({
            ...baseElement("list", "Listă", 120, 40),
            style: {
                ...typography(14),
                fontFamily: "Inter",
                color: "#111827",
                align: "left",
                lineHeight: 1.2,
                listType: "bullet",
                indent_mm: 5,
            },
            items: ["Primul punct", "Al doilea punct"],
        }, { fitContent: true });
    }

    function addVariable(variable) {
        const label = VARIABLE_LABELS[variable];
        addElement({
            ...baseElement("variable", label, 90, 15),
            style: typography(variable === "full_name" ? 32 : 20, variable === "full_name"),
            variable,
            placeholder: label,
        }, { fitContent: true });
    }

    function addImage(trigger) {
        openMediaPicker("create-image", trigger);
    }

    function addBackground(trigger) {
        const background = state.layout.elements.find((element) => element.type === "background");
        if (background) {
            setSelection([background.id]);
            renderAll();
            openMediaPicker("replace-background", trigger);
            return;
        }
        openMediaPicker("create-background", trigger);
    }

    function addIcon() {
        addElement({
            ...baseElement("icon", "Icon", 13, 13),
            style: { color: "#164194", opacity: 1 },
            iconName: "award",
        }, { fitContent: true });
    }

    function addTable() {
        addElement({
            ...baseElement("table", "Tabel", 143, 29),
            style: {
                fontFamily: "Inter",
                fontSize: 14,
                bold: false,
                color: "#304253",
                align: "center",
                borderColor: "#164194",
                headerBackground: "#edf3f9",
            },
            columns: ["Coloana 1", "Coloana 2", "Coloana 3"],
            rows: [["Valoare", "Valoare", "Valoare"]],
        });
    }

    function moveLayer(direction) {
        const element = selectedElement();
        if (!element || element.type === "background") return;
        const sorted = state.layout.elements
            .filter((item) => item.type !== "background")
            .sort((left, right) => left.zIndex - right.zIndex);
        const index = sorted.findIndex((item) => item.id === element.id);
        const targetIndex = index + direction;
        if (targetIndex < 0 || targetIndex >= sorted.length) return;
        const target = sorted[targetIndex];
        [element.zIndex, target.zIndex] = [target.zIndex, element.zIndex];
        markDirty();
        renderAll();
    }

    function alignSelected(kind) {
        const elements = selectedElements().filter(
            (element) => !element.locked && element.type !== "background"
        );
        if (!elements.length) return;
        const alignToPage = elements.length === 1;
        const left = alignToPage
            ? 0
            : Math.min(...elements.map((element) => element.x_mm));
        const right = alignToPage
            ? state.layout.page.width_mm
            : Math.max(...elements.map((element) => element.x_mm + element.width_mm));
        const top = alignToPage
            ? 0
            : Math.min(...elements.map((element) => element.y_mm));
        const bottom = alignToPage
            ? state.layout.page.height_mm
            : Math.max(...elements.map((element) => element.y_mm + element.height_mm));
        elements.forEach((element) => {
            if (kind === "left") element.x_mm = left;
            if (kind === "center") element.x_mm = snap((left + right - element.width_mm) / 2);
            if (kind === "right") element.x_mm = right - element.width_mm;
            if (kind === "top") element.y_mm = top;
            if (kind === "middle") element.y_mm = snap((top + bottom - element.height_mm) / 2);
            if (kind === "bottom") element.y_mm = bottom - element.height_mm;
            element.x_mm = clamp(element.x_mm, 0, state.layout.page.width_mm - element.width_mm);
            element.y_mm = clamp(element.y_mm, 0, state.layout.page.height_mm - element.height_mm);
        });
        markDirty();
        renderAll();
    }

    function distributeSelected(axis) {
        const elements = selectedElements().filter(
            (element) => !element.locked && element.type !== "background"
        );
        if (elements.length < 3) return;
        const horizontal = axis === "horizontal";
        elements.sort((left, right) => horizontal ? left.x_mm - right.x_mm : left.y_mm - right.y_mm);
        const positionKey = horizontal ? "x_mm" : "y_mm";
        const sizeKey = horizontal ? "width_mm" : "height_mm";
        const first = elements[0][positionKey];
        const end = elements.at(-1)[positionKey] + elements.at(-1)[sizeKey];
        const occupied = elements.reduce((sum, element) => sum + element[sizeKey], 0);
        const gap = (end - first - occupied) / (elements.length - 1);
        let cursor = first;
        elements.forEach((element) => {
            if (element.type !== "background") element[positionKey] = snap(cursor);
            cursor += element[sizeKey] + gap;
        });
        markDirty();
        renderAll();
    }

    function hideGuides() {
        guideX.hidden = true;
        guideY.hidden = true;
    }

    function snapBoundsToPage(bounds) {
        if (!state.guidesVisible) {
            hideGuides();
            return { dx: 0, dy: 0 };
        }
        const tolerance = 1;
        const page = state.layout.page;
        const findSnap = (values, targets) => {
            let best = null;
            values.forEach((value) => targets.forEach((target) => {
                const distance = Math.abs(target - value);
                if (distance <= tolerance && (!best || distance < best.distance)) {
                    best = { adjustment: target - value, target, distance };
                }
            }));
            return best;
        };
        const xSnap = findSnap(
            [bounds.left, (bounds.left + bounds.right) / 2, bounds.right],
            [0, page.width_mm / 2, page.width_mm, ...state.layout.guides.vertical],
        );
        const ySnap = findSnap(
            [bounds.top, (bounds.top + bounds.bottom) / 2, bounds.bottom],
            [0, page.height_mm / 2, page.height_mm, ...state.layout.guides.horizontal],
        );
        guideX.hidden = !xSnap;
        guideY.hidden = !ySnap;
        if (xSnap) guideX.style.left = `${mmToPx(xSnap.target)}px`;
        if (ySnap) guideY.style.top = `${mmToPx(ySnap.target)}px`;
        return { dx: xSnap?.adjustment || 0, dy: ySnap?.adjustment || 0 };
    }

    function beginPointerInteraction(event) {
        const node = event.target.closest(".diploma-element");
        if (!node) {
            setSelection([]);
            renderAll();
            return;
        }
        const element = state.layout.elements.find((item) => item.id === node.dataset.elementId);
        if (!element) return;
        if (event.shiftKey || event.ctrlKey || event.metaKey) {
            selectElement(element.id, event);
            return;
        }
        if (!state.selectedIds.includes(element.id)) setSelection([element.id]);
        renderAll();
        if (element.locked || element.type === "background" || event.button !== 0) return;
        event.preventDefault();

        const resizing = state.selectedIds.length === 1 && Boolean(event.target.closest("[data-resize-handle]"));
        const moving = selectedElements().filter((item) => !item.locked);
        if (!moving.length) return;
        const startElements = moving.map((item) => ({
            element: item,
            x_mm: item.x_mm,
            y_mm: item.y_mm,
            width_mm: item.width_mm,
            height_mm: item.height_mm,
        }));
        const start = {
            clientX: event.clientX,
            clientY: event.clientY,
            x_mm: element.x_mm,
            y_mm: element.y_mm,
            width_mm: element.width_mm,
            height_mm: element.height_mm,
        };

        function onMove(moveEvent) {
            const dx_mm = pxToMm((moveEvent.clientX - start.clientX) / state.zoom);
            const dy_mm = pxToMm((moveEvent.clientY - start.clientY) / state.zoom);
            if (resizing) {
                element.width_mm = clamp(snap(start.width_mm + dx_mm), 1, state.layout.page.width_mm - element.x_mm);
                element.height_mm = clamp(snap(start.height_mm + dy_mm), 1, state.layout.page.height_mm - element.y_mm);
                const adjustment = snapBoundsToPage({
                    left: element.x_mm,
                    right: element.x_mm + element.width_mm,
                    top: element.y_mm,
                    bottom: element.y_mm + element.height_mm,
                });
                element.width_mm = clamp(snap(element.width_mm + adjustment.dx), 1, state.layout.page.width_mm - element.x_mm);
                element.height_mm = clamp(snap(element.height_mm + adjustment.dy), 1, state.layout.page.height_mm - element.y_mm);
            } else {
                const left = Math.min(...startElements.map((item) => item.x_mm));
                const right = Math.max(...startElements.map((item) => item.x_mm + item.width_mm));
                const top = Math.min(...startElements.map((item) => item.y_mm));
                const bottom = Math.max(...startElements.map((item) => item.y_mm + item.height_mm));
                let moveX = clamp(snap(dx_mm), -left, state.layout.page.width_mm - right);
                let moveY = clamp(snap(dy_mm), -top, state.layout.page.height_mm - bottom);
                const adjustment = snapBoundsToPage({
                    left: left + moveX,
                    right: right + moveX,
                    top: top + moveY,
                    bottom: bottom + moveY,
                });
                moveX = clamp(snap(moveX + adjustment.dx), -left, state.layout.page.width_mm - right);
                moveY = clamp(snap(moveY + adjustment.dy), -top, state.layout.page.height_mm - bottom);
                startElements.forEach((item) => {
                    item.element.x_mm = item.x_mm + moveX;
                    item.element.y_mm = item.y_mm + moveY;
                });
            }
            renderCanvas();
            renderProperties();
        }

        function onUp() {
            document.removeEventListener("pointermove", onMove);
            document.removeEventListener("pointerup", onUp);
            hideGuides();
            markDirty();
            renderAll();
        }

        document.addEventListener("pointermove", onMove);
        document.addEventListener("pointerup", onUp, { once: true });
    }

    function updateProperty(control) {
        const element = selectedElement();
        const key = control.dataset.prop;
        const backgroundMediaChange = element?.type === "background" && ["assetId", "alt"].includes(key);
        if (!element || (element.locked && !backgroundMediaChange)) return;
        let value = control.value;
        if (key === "assetId" && !mediaAssetsById.has(value)) return;
        if (["x_mm", "y_mm", "width_mm", "height_mm", "rotation", "zIndex"].includes(key)) {
            value = Number.parseInt(value, 10);
            if (!Number.isFinite(value)) return;
            if (["x_mm", "y_mm", "width_mm", "height_mm"].includes(key)) value = snap(value);
        }
        if (key === "width_mm") value = clamp(value, 1, state.layout.page.width_mm - element.x_mm);
        if (key === "height_mm") value = clamp(value, 1, state.layout.page.height_mm - element.y_mm);
        if (key === "x_mm") value = clamp(value, 0, state.layout.page.width_mm - element.width_mm);
        if (key === "y_mm") value = clamp(value, 0, state.layout.page.height_mm - element.height_mm);
        if (key === "rotation") value = clamp(value, -180, 180);
        if (key === "zIndex") value = clamp(value, element.type === "background" ? 0 : 1, 1000);
        element[key] = value;
        if (key === "assetId" && !element.alt) {
            element.alt = mediaAssetsById.get(value)?.name || "";
        }
        markDirty();
        renderCanvas();
        renderLayers();
    }

    function updateStyle(control) {
        const element = selectedElement();
        const key = control.dataset.style;
        const backgroundStyleChange = element?.type === "background" && ["fit", "opacity"].includes(key);
        if (!element || (element.locked && !backgroundStyleChange)) return;
        let value = control.value;
        if (key === "fontSize") value = clamp(Number.parseInt(value, 10) || 8, 8, 200);
        if (key === "opacity") value = clamp(Number.parseFloat(value) || 0, 0, 1);
        if (key === "lineHeight") value = clamp(Number.parseFloat(value) || 0.8, 0.8, 3);
        if (key === "letterSpacing") value = clamp(Number.parseFloat(value) || 0, -5, 20);
        if (key === "indent_mm") value = clamp(Number.parseFloat(value) || 0, 0, 50);
        element.style[key] = value;
        markDirty();
        renderCanvas();
    }

    function updateIconStyle(control) {
        const element = selectedElement();
        if (!element || element.type !== "icon" || element.locked) return;
        const key = control.dataset.iconStyle;
        let value = control.value;
        if (key === "opacity") value = clamp(Number.parseFloat(value) || 0, 0, 1);
        element.style[key] = value;
        markDirty();
        renderCanvas();
    }

    function updateTableStyle(control) {
        const element = selectedElement();
        if (!element || element.type !== "table" || element.locked) return;
        const key = control.dataset.tableStyle;
        let value = control.type === "checkbox" ? control.checked : control.value;
        if (key === "fontSize") value = clamp(Number.parseInt(value, 10) || 8, 8, 72);
        element.style[key] = value;
        markDirty();
        renderCanvas();
    }

    function updateTableColumns(control) {
        const element = selectedElement();
        if (!element || element.type !== "table" || element.locked) return;
        const columns = control.value.split(/\r?\n/)
            .map((value) => value.trim())
            .filter(Boolean)
            .slice(0, 8);
        if (!columns.length) return;
        element.columns = columns;
        element.rows = element.rows.map((row) => [
            ...row.slice(0, columns.length),
            ...Array(Math.max(0, columns.length - row.length)).fill(""),
        ]);
        markDirty();
        renderCanvas();
    }

    function updateTableRows(control) {
        const element = selectedElement();
        if (!element || element.type !== "table" || element.locked) return;
        element.rows = control.value.split(/\r?\n/)
            .filter((line) => line.trim())
            .slice(0, 20)
            .map((line) => {
                const cells = line.split("|").map((value) => value.trim());
                return [
                    ...cells.slice(0, element.columns.length),
                    ...Array(Math.max(0, element.columns.length - cells.length)).fill(""),
                ];
            });
        markDirty();
        renderCanvas();
    }

    async function saveLayout() {
        if (state.saving) return false;
        state.saving = true;
        setSaveStatus("saving", "Se salvează…");
        const savedRevision = state.revision;
        const submittedSnapshot = layoutSnapshot();
        const formData = new FormData(saveForm);
        formData.append("layout_json", JSON.stringify(state.layout));
        try {
            const response = await fetch(root.dataset.saveUrl, {
                method: "POST",
                body: formData,
                headers: { "X-Requested-With": "XMLHttpRequest" },
            });
            const payload = await response.json();
            if (!response.ok || !payload.success) {
                const message = payload.errors?.layout_json?.[0]?.message || "Template-ul nu a putut fi salvat.";
                throw new Error(message);
            }
            isDraftTemplate = Boolean(payload.isDraft);
            state.savedSnapshot = submittedSnapshot;
            if (state.revision !== savedRevision) {
                updateDirtyStatus();
                setSaveStatus("dirty", "Există modificări noi nesalvate");
                return false;
            }
            updateDirtyStatus();
            return true;
        } catch (error) {
            setSaveStatus("error", error.message || "Eroare la salvare");
            return false;
        } finally {
            state.saving = false;
        }
    }

    async function openPreview(event) {
        event.preventDefault();
        const previewLink = event.currentTarget;
        if (state.dirty && !(await saveLayout())) return;
        window.location.href = previewLink.href;
    }

    async function confirmDiscardChanges() {
        if (!state.dirty) return true;
        return requestConfirmation({
            title: "Modificări nesalvate",
            message: "Ai modificări nesalvate. Dacă ieși acum, acestea vor fi pierdute.",
            acceptLabel: "Ieși fără salvare",
            cancelLabel: "Rămâi în editor",
        });
    }

    async function discardDraftTemplate() {
        if (!isDraftTemplate) return true;
        try {
            const response = await fetch(discardForm.action, {
                method: "POST",
                body: new FormData(discardForm),
                headers: {
                    "Accept": "application/json",
                    "X-Requested-With": "XMLHttpRequest",
                },
            });
            const payload = await response.json().catch(() => ({}));
            if (!response.ok || !payload.success) {
                throw new Error("Template-ul provizoriu nu a putut fi eliminat.");
            }
            isDraftTemplate = false;
            return true;
        } catch (error) {
            setSaveStatus("error", error.message || "Template-ul provizoriu nu a putut fi eliminat.");
            return false;
        }
    }

    async function prepareToLeaveEditor() {
        if (state.leaving) return false;
        state.leaving = true;
        if (!(await confirmDiscardChanges())) {
            state.leaving = false;
            return false;
        }
        if (!(await discardDraftTemplate())) {
            state.leaving = false;
            return false;
        }
        state.dirty = false;
        return true;
    }

    async function closeEditor() {
        if (!(await prepareToLeaveEditor())) return;
        window.location.assign(root.dataset.templateListUrl);
    }

    function shouldInterceptNavigation(event, link) {
        if ((!state.dirty && !isDraftTemplate) || !link || event.defaultPrevented || event.button !== 0) return false;
        if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return false;
        if (link.hasAttribute("download") || (link.target && link.target !== "_self")) return false;
        if (link.dataset.action === "preview") return false;

        const destination = new URL(link.href, window.location.href);
        if (!["http:", "https:"].includes(destination.protocol)) return false;
        const current = new URL(window.location.href);
        if (
            destination.origin === current.origin
            && destination.pathname === current.pathname
            && destination.search === current.search
        ) return false;
        return true;
    }

    async function handleDocumentNavigation(event) {
        const link = event.target.closest?.("a[href]");
        if (!shouldInterceptNavigation(event, link)) return;
        event.preventDefault();
        event.stopPropagation();
        if (!(await prepareToLeaveEditor())) return;
        window.location.assign(link.href);
    }

    root.addEventListener("click", (event) => {
        const alignNode = event.target.closest("[data-align]");
        if (alignNode) {
            alignSelected(alignNode.dataset.align);
            return;
        }
        const distributeNode = event.target.closest("[data-distribute]");
        if (distributeNode) {
            distributeSelected(distributeNode.dataset.distribute);
            return;
        }
        const actionNode = event.target.closest("[data-action]");
        if (!actionNode) return;
        const action = actionNode.dataset.action;
        if (action === "save") saveLayout();
        if (action === "close-editor") closeEditor();
        if (action === "undo") restoreHistory(-1);
        if (action === "redo") restoreHistory(1);
        if (action === "zoom-out") changeZoom(-1);
        if (action === "zoom-in") changeZoom(1);
        if (action === "fit-page") fitPage();
        if (action === "toggle-grid") {
            state.gridVisible = !state.gridVisible;
            actionNode.classList.toggle("is-active", state.gridVisible);
            actionNode.setAttribute("aria-pressed", String(state.gridVisible));
            renderCanvas();
        }
        if (action === "toggle-guides") {
            state.guidesVisible = !state.guidesVisible;
            actionNode.classList.toggle("is-active", state.guidesVisible);
            actionNode.setAttribute("aria-pressed", String(state.guidesVisible));
            if (!state.guidesVisible) hideGuides();
            renderCanvas();
        }
        if (action === "fit-content") fitSelectedToContent();
        if (action === "add-guide-x") addCustomGuide("vertical");
        if (action === "add-guide-y") addCustomGuide("horizontal");
        if (action === "add-text") addText();
        if (action === "add-list") addList();
        if (action === "add-image") addImage(actionNode);
        if (action === "add-background") addBackground(actionNode);
        if (action === "add-icon") addIcon();
        if (action === "add-table") addTable();
        if (action === "layer-up") moveLayer(1);
        if (action === "layer-down") moveLayer(-1);
        if (action === "open-media-picker") {
            openMediaPicker(selectedElement()?.type === "background" ? "replace-background" : "replace", actionNode);
        }
        if (action === "open-icon-media-picker") openMediaPicker("replace-icon", actionNode);
        if (action === "close-media-picker") closeMediaPicker();
        if (action === "apply-media-asset") applyMediaAsset();
        if (action === "refresh-media-assets") refreshMediaAssets();
        if (action === "remove-media-element") removeSelectedMediaElement();
        if (action === "remove-icon-asset") removeIconAsset();
    });

    root.querySelector('[data-action="zoom"]').addEventListener("change", (event) => {
        if (event.target.value === "fit") {
            fitPage();
            return;
        }
        setZoom(Number.parseFloat(event.target.value));
    });

    viewport.addEventListener("wheel", (event) => {
        if (!event.ctrlKey && !event.metaKey) return;
        event.preventDefault();
        changeZoom(event.deltaY < 0 ? 1 : -1, {
            clientX: event.clientX,
            clientY: event.clientY,
        });
    }, { passive: false });

    inspectorTabs.forEach((tab, index) => {
        tab.addEventListener("click", () => setInspectorTab(tab.dataset.inspectorTab));
        tab.addEventListener("keydown", (event) => {
            let nextIndex = null;
            if (event.key === "ArrowLeft") nextIndex = (index - 1 + inspectorTabs.length) % inspectorTabs.length;
            if (event.key === "ArrowRight") nextIndex = (index + 1) % inspectorTabs.length;
            if (event.key === "Home") nextIndex = 0;
            if (event.key === "End") nextIndex = inspectorTabs.length - 1;
            if (nextIndex === null) return;
            event.preventDefault();
            setInspectorTab(inspectorTabs[nextIndex].dataset.inspectorTab, { focus: true });
        });
    });

    root.querySelector('[data-action="preview"]').addEventListener("click", openPreview);

    root.querySelectorAll("[data-add-variable]").forEach((button) => {
        button.addEventListener("click", () => {
            addVariable(button.dataset.addVariable);
            button.closest("details")?.removeAttribute("open");
        });
    });

    propertiesNode.addEventListener("input", (event) => {
        if (event.target.tagName === "SELECT") return;
        if (event.target.matches("[data-prop]")) updateProperty(event.target);
        if (event.target.matches("[data-style]")) updateStyle(event.target);
        if (event.target.matches("[data-icon-style]")) updateIconStyle(event.target);
        if (event.target.matches("[data-table-style]")) updateTableStyle(event.target);
        if (event.target.matches("[data-table-columns]")) updateTableColumns(event.target);
        if (event.target.matches("[data-table-rows]")) updateTableRows(event.target);
        if (event.target.matches("[data-list-items]")) {
            const element = selectedElement();
            if (!element || element.type !== "list" || element.locked) return;
            element.items = event.target.value.split(/\r?\n/).slice(0, 20);
            markDirty();
            renderCanvas();
        }
    });
    propertiesNode.addEventListener("change", (event) => {
        if (event.target.matches("[data-prop]")) {
            updateProperty(event.target);
            renderProperties();
        }
        if (event.target.matches("[data-style]")) {
            updateStyle(event.target);
            renderProperties();
        }
        if (event.target.matches("[data-icon-style]")) {
            updateIconStyle(event.target);
            renderProperties();
        }
        if (event.target.matches("[data-table-style]")) {
            updateTableStyle(event.target);
            renderProperties();
        }
    });
    propertiesNode.querySelectorAll("[data-style-toggle]").forEach((button) => {
        button.addEventListener("click", () => {
            const element = selectedElement();
            if (!element || element.locked) return;
            const key = button.dataset.styleToggle;
            element.style[key] = !element.style[key];
            markDirty();
            renderAll();
        });
    });

    mediaUploadForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const submitButton = mediaUploadForm.querySelector('[type="submit"]');
        submitButton.disabled = true;
        mediaUploadError.hidden = true;
        mediaUploadError.textContent = "";
        try {
            const response = await fetch(root.dataset.mediaAssetsUploadUrl, {
                method: "POST",
                body: new FormData(mediaUploadForm),
                headers: { "Accept": "application/json" },
            });
            const payload = await response.json().catch(() => ({}));
            if (!response.ok || !payload.success || !payload.asset) {
                const messages = Object.values(payload.errors || {})
                    .flat()
                    .map((error) => typeof error === "string" ? error : error.message)
                    .filter(Boolean);
                throw new Error(messages.join(" ") || "Fișierul nu a putut fi încărcat.");
            }

            const uploadedAsset = payload.asset;
            const existingIndex = mediaAssets.findIndex((asset) => asset.id === uploadedAsset.id);
            if (existingIndex >= 0) mediaAssets.splice(existingIndex, 1, uploadedAsset);
            else mediaAssets.unshift(uploadedAsset);
            mediaAssetsById.set(uploadedAsset.id, uploadedAsset);
            try {
                await fetchMediaAssets();
            } catch (_error) {
                // The upload response is sufficient to keep the new asset usable.
            }
            pickerState.selectedAssetId = uploadedAsset.id;
            mediaUploadForm.reset();
            setPickerFeedback(`„${uploadedAsset.name}” a fost încărcat și selectat.`);
            renderMediaPicker();
            renderProperties();
            renderCanvas();
        } catch (error) {
            mediaUploadError.textContent = error.message || "Fișierul nu a putut fi încărcat.";
            mediaUploadError.hidden = false;
        } finally {
            submitButton.disabled = false;
        }
    });

    confirmAccept.addEventListener("click", () => closeConfirmation(true));
    confirmDialog.querySelectorAll("[data-confirm-cancel]").forEach((button) => {
        button.addEventListener("click", (event) => {
            event.preventDefault();
            closeConfirmation(false);
        });
    });
    confirmDialog.addEventListener("cancel", (event) => {
        event.preventDefault();
        closeConfirmation(false);
    });

    document.addEventListener("click", handleDocumentNavigation, true);
    canvas.addEventListener("pointerdown", beginPointerInteraction);
    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && !mediaPicker.hidden) closeMediaPicker();
        const typing = event.target.closest("input, textarea, select, [contenteditable='true']");
        if (!typing && (event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "z") {
            event.preventDefault();
            restoreHistory(event.shiftKey ? 1 : -1);
            return;
        }
        if (!typing && (event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "y") {
            event.preventDefault();
            restoreHistory(1);
            return;
        }
        if (!["Delete", "Backspace"].includes(event.key)) return;
        if (typing) return;
        if (!state.selectedIds.length) return;
        event.preventDefault();
        deleteElements();
    });
    let bypassHistoryGuard = false;
    window.history.pushState({ diplomaEditorGuard: true }, "", window.location.href);
    window.addEventListener("popstate", async () => {
        if (bypassHistoryGuard) return;
        if (await prepareToLeaveEditor()) {
            bypassHistoryGuard = true;
            window.history.back();
            return;
        }
        window.history.pushState({ diplomaEditorGuard: true }, "", window.location.href);
    });

    if ("ResizeObserver" in window) {
        const viewportObserver = new ResizeObserver(refreshFittedZoom);
        viewportObserver.observe(viewport);
    } else {
        window.addEventListener("resize", refreshFittedZoom);
    }

    renderAll();
})();
```

## `apps/diplome/static/diplome/template_preview.js`

Size: 1.4 KB

```javascript
(function () {
    "use strict";

    const root = document.getElementById("diploma-preview")
        || document.getElementById("generation-diploma-preview");
    if (!root || !window.DiplomaRenderer) return;

    const layout = JSON.parse(document.getElementById("diploma-layout-data").textContent);
    const sampleData = JSON.parse(document.getElementById("diploma-sample-data").textContent);
    const assetsNode = document.getElementById("diploma-media-assets-data");
    const assets = new Map(
        (assetsNode ? JSON.parse(assetsNode.textContent) : []).map((asset) => [asset.id, asset]),
    );
    const canvas = document.getElementById("preview-canvas");
    const frame = document.getElementById("preview-canvas-frame");
    const workspace = root.querySelector(".preview-workspace");

    window.DiplomaRenderer.render(canvas, layout, { editable: false, sampleData, assets });

    function fitPreview() {
        const pageSize = window.DiplomaRenderer.pagePixelSize(layout);
        const available = Math.max(320, workspace.clientWidth - 64);
        const scale = Math.min(1, available / pageSize.width);
        canvas.style.transform = `scale(${scale})`;
        canvas.style.transformOrigin = "top left";
        frame.style.width = `${pageSize.width * scale}px`;
        frame.style.height = `${pageSize.height * scale}px`;
    }

    fitPreview();
    window.addEventListener("resize", fitPreview);
})();
```

## `apps/diplome/static/diplome/template_renderer.js`

Size: 9.3 KB

```javascript
(function () {
    "use strict";

    const PX_PER_MM = 96 / 25.4;

    const FONT_STACKS = {
        Inter: 'InterVariable, Inter, "Segoe UI", sans-serif',
        Lora: 'Lora, Georgia, "Times New Roman", serif',
        Georgia: 'Georgia, "Times New Roman", serif',
        Arial: 'Arial, sans-serif',
        "Times New Roman": '"Times New Roman", serif',
    };
    const SVG_NS = "http://www.w3.org/2000/svg";

    function mmToPx(value) {
        return value * PX_PER_MM;
    }

    function pxToMm(value) {
        return value / PX_PER_MM;
    }

    function pagePixelSize(layout) {
        return {
            width: mmToPx(layout.page.width_mm),
            height: mmToPx(layout.page.height_mm),
        };
    }

    function textNode(className, value) {
        const node = document.createElement("div");
        node.className = className;
        node.textContent = value;
        return node;
    }

    function svgIcon(iconName) {
        const svg = document.createElementNS(SVG_NS, "svg");
        svg.classList.add("diploma-icon-svg");
        svg.setAttribute("viewBox", "0 0 24 24");
        svg.setAttribute("aria-hidden", "true");
        svg.setAttribute("fill", "none");
        svg.setAttribute("stroke", "currentColor");
        svg.setAttribute("stroke-width", "1.8");
        svg.setAttribute("stroke-linecap", "round");
        svg.setAttribute("stroke-linejoin", "round");
        const paths = {
            award: [
                ["circle", { cx: "12", cy: "8", r: "5" }],
                ["path", { d: "M8.7 12.7 7.5 22l4.5-2.7 4.5 2.7-1.2-9.3" }],
            ],
            "patch-check": [
                ["rect", { x: "3.5", y: "3.5", width: "17", height: "17", rx: "2" }],
                ["path", { d: "m7.5 12 3 3 6-6" }],
            ],
            star: [["path", { d: "m12 2.8 2.8 5.7 6.3.9-4.6 4.5 1.1 6.3-5.6-3-5.6 3 1.1-6.3-4.6-4.5 6.3-.9Z" }]],
        };
        (paths[iconName] || paths.star).forEach(([tag, attributes]) => {
            const node = document.createElementNS(SVG_NS, tag);
            Object.entries(attributes).forEach(([key, value]) => node.setAttribute(key, value));
            svg.appendChild(node);
        });
        return svg;
    }

    function applyTypography(node, style) {
        node.style.fontFamily = FONT_STACKS[style.fontFamily] || FONT_STACKS.Inter;
        node.style.fontSize = `${style.fontSize}px`;
        node.style.fontWeight = style.bold ? "700" : "400";
        node.style.fontStyle = style.italic ? "italic" : "normal";
        node.style.textDecoration = style.underline ? "underline" : "none";
        node.style.color = style.color;
        node.style.textAlign = style.align;
        node.style.lineHeight = String(style.lineHeight ?? 1.18);
        node.style.letterSpacing = `${style.letterSpacing ?? 0}px`;
        node.style.textTransform = style.textTransform || "none";
    }

    function renderList(element) {
        const list = document.createElement(element.style.listType === "number" ? "ol" : "ul");
        list.className = "diploma-list";
        element.items.forEach((item) => {
            const row = document.createElement("li");
            row.textContent = item;
            list.appendChild(row);
        });
        applyTypography(list, element.style);
        list.style.paddingInlineStart = `${mmToPx(element.style.indent_mm)}px`;
        return list;
    }

    function renderTable(element) {
        const table = document.createElement("table");
        table.setAttribute("aria-label", element.label);
        const thead = document.createElement("thead");
        const headerRow = document.createElement("tr");
        element.columns.forEach((column) => {
            const cell = document.createElement("th");
            cell.textContent = column;
            headerRow.appendChild(cell);
        });
        thead.appendChild(headerRow);
        table.appendChild(thead);
        const tbody = document.createElement("tbody");
        element.rows.forEach((row) => {
            const tableRow = document.createElement("tr");
            row.forEach((value) => {
                const cell = document.createElement("td");
                cell.textContent = value;
                tableRow.appendChild(cell);
            });
            tbody.appendChild(tableRow);
        });
        table.appendChild(tbody);
        table.style.fontFamily = FONT_STACKS[element.style.fontFamily] || FONT_STACKS.Inter;
        table.style.fontSize = `${element.style.fontSize}px`;
        table.style.fontWeight = element.style.bold ? "700" : "400";
        table.style.color = element.style.color;
        table.style.textAlign = element.style.align;
        return table;
    }

    function renderContent(element, sampleData, assets) {
        if (element.type === "text") {
            const node = textNode("diploma-element-content", element.text);
            applyTypography(node, element.style);
            return node;
        }
        if (element.type === "variable") {
            const value = sampleData?.[element.variable] || `{{ ${element.variable} }}`;
            const node = textNode("diploma-element-content", value);
            applyTypography(node, element.style);
            return node;
        }
        if (element.type === "list") return renderList(element);
        if (element.type === "table") {
            return renderTable(element);
        }
        if (element.type === "icon") {
            const asset = element.assetId ? assets?.get(element.assetId) : null;
            if (asset) {
                const image = document.createElement("img");
                image.className = "diploma-media";
                image.src = asset.url;
                image.alt = element.alt || "";
                image.draggable = false;
                image.style.objectFit = "contain";
                image.style.opacity = String(element.style.opacity);
                return image;
            }
            const node = document.createElement("div");
            node.className = "diploma-icon";
            node.style.color = element.style.color;
            node.style.opacity = String(element.style.opacity);
            node.appendChild(svgIcon(element.iconName));
            return node;
        }
        const asset = assets?.get(element.assetId);
        if (asset) {
            const image = document.createElement("img");
            image.className = "diploma-media";
            image.src = asset.url;
            image.alt = element.alt || "";
            image.draggable = false;
            image.style.objectFit = element.style.fit === "stretch" ? "fill" : element.style.fit;
            image.style.opacity = String(element.style.opacity);
            return image;
        }
        const node = textNode("diploma-placeholder", "Fișier media indisponibil");
        node.style.opacity = String(element.style.opacity);
        return node;
    }

    function renderElement(element, options) {
        const node = document.createElement("div");
        node.className = `diploma-element diploma-element-${element.type}`;
        node.dataset.elementId = element.id;
        node.style.left = `${mmToPx(element.x_mm)}px`;
        node.style.top = `${mmToPx(element.y_mm)}px`;
        node.style.width = `${mmToPx(element.width_mm)}px`;
        node.style.height = `${mmToPx(element.height_mm)}px`;
        node.style.zIndex = String(element.zIndex);
        node.style.transform = `rotate(${element.rotation}deg)`;
        node.setAttribute("role", options.editable ? "button" : "group");
        node.setAttribute("aria-label", element.label);
        if (!element.visible) node.classList.add("is-hidden");
        if (element.locked) node.classList.add("is-locked");
        const selectedIds = options.selectedIds || (options.selectedId ? [options.selectedId] : []);
        const selected = selectedIds.includes(element.id);
        if (options.editable && selected) {
            node.classList.add("is-selected");
            node.setAttribute("aria-pressed", "true");
        }
        if (element.type === "table") {
            node.style.setProperty("--element-border", element.style.borderColor);
            node.style.setProperty("--element-header", element.style.headerBackground);
        }
        node.appendChild(renderContent(element, options.sampleData, options.assets));
        if (options.editable && selected && selectedIds.length === 1 && !element.locked) {
            const handle = document.createElement("span");
            handle.className = "editor-resize-handle";
            handle.dataset.resizeHandle = "true";
            handle.setAttribute("aria-label", "Redimensionează elementul");
            node.appendChild(handle);
        }
        return node;
    }

    function render(canvas, layout, options = {}) {
        const guides = Array.from(canvas.querySelectorAll(".editor-guide"));
        canvas.replaceChildren(...guides);
        const pageSize = pagePixelSize(layout);
        canvas.style.width = `${pageSize.width}px`;
        canvas.style.height = `${pageSize.height}px`;
        canvas.style.setProperty("--minor-grid-size", `${mmToPx(layout.page.grid_mm)}px`);
        canvas.style.setProperty("--major-grid-size", `${mmToPx(layout.page.major_grid_mm)}px`);
        [...layout.elements]
            .sort((left, right) => left.zIndex - right.zIndex)
            .forEach((element) => canvas.appendChild(renderElement(element, options)));
    }

    window.DiplomaRenderer = { render, mmToPx, pxToMm, pagePixelSize };
})();
```

## `apps/diplome/templates/diplome/batch_detail.html`

Size: 247 B

```html
{% extends "layouts/base.html" %}

{% block title %}Lot diplome | Platforma TUVTK{% endblock %}

{% block content %}
<section class="mx-auto w-full max-w-7xl">
    {% include "diplome/includes/batch_detail_panel.html" %}
</section>
{% endblock %}
```

## `apps/diplome/templates/diplome/generation_index.html`

Size: 11.0 KB

```html
{% extends "layouts/base.html" %}
{% load static %}

{% block title %}Generator diplome | Platforma TUVTK{% endblock %}

{% block content %}
<section class="mx-auto w-full max-w-6xl space-y-6">
    <header class="space-y-2">
        <div class="breadcrumbs p-0 text-sm text-muted">
            <ul><li>Diplome</li><li>Generare</li></ul>
        </div>
        <div>
            <h1 class="text-2xl font-bold text-primary">Generator diplome</h1>
            <p class="mt-1 text-sm text-muted">Generează o diplomă individuală sau toate diplomele unei liste.</p>
        </div>
    </header>

    <div class="grid gap-6 lg:grid-cols-[minmax(0,1.35fr)_minmax(18rem,0.65fr)]">
        <div class="border border-base-300 bg-base-100 p-5 sm:p-6">
            {% if form.non_field_errors %}
                <div class="alert alert-error mb-5 py-2 text-sm" role="alert">
                    {% for error in form.non_field_errors %}<span>{{ error }}</span>{% endfor %}
                </div>
            {% endif %}

            {% if not has_participant_lists or not has_templates %}
                <div class="mb-6 border border-warning/40 bg-warning/10 p-4 text-sm text-base-content" role="status">
                    <p class="font-semibold">Completează datele necesare înainte de generare.</p>
                    <ul class="mt-2 list-inside list-disc space-y-1 text-muted">
                        {% if not has_participant_lists %}<li>Importă cel puțin o listă de participanți.</li>{% endif %}
                        {% if not has_templates %}<li>Creează cel puțin un template de diplomă.</li>{% endif %}
                    </ul>
                </div>
            {% endif %}

            <form method="post" class="space-y-5" data-generation-form>
                {% csrf_token %}
                <div class="form-control">
                    <label for="{{ form.participant_list.id_for_label }}" class="mb-1.5 text-sm font-semibold text-base-content">{{ form.participant_list.label }}</label>
                    {{ form.participant_list }}
                    {% for error in form.participant_list.errors %}<p class="mt-1 text-xs text-error">{{ error }}</p>{% endfor %}
                    <p class="mt-1.5 text-xs text-muted">Lista determină participanții disponibili în pasul următor.</p>
                </div>

                <div class="form-control">
                    <span id="generation-participant-label" class="mb-1.5 text-sm font-semibold text-base-content">{{ form.participant.label }}</span>
                    <div class="overflow-hidden border border-base-300 bg-base-100" role="group" aria-labelledby="generation-participant-label" data-participant-table>
                        <div class="flex items-center justify-between gap-3 border-b border-base-300 bg-base-200 px-3 py-2 text-xs text-muted">
                            <span>Selectează un singur participant</span>
                            <span>Selectați: <strong class="font-semibold text-base-content" data-participant-count>0</strong></span>
                        </div>
                        <div class="max-h-64 overflow-auto" data-participant-scroll>
                            <table class="table table-xs min-w-[46rem]">
                                <thead class="sticky top-0 z-10 bg-base-200 text-[0.68rem] uppercase tracking-wide text-muted">
                                    <tr>
                                        <th class="w-10 text-center">Alege</th>
                                        <th class="w-16">Nr.</th>
                                        <th>Nume complet</th>
                                        <th class="w-28">Data nașterii</th>
                                        <th>Locul nașterii</th>
                                        <th class="w-32">Nr. certificat</th>
                                    </tr>
                                </thead>
                                <tbody data-participant-rows>
                                    {% for participant in form.fields.participant.queryset %}
                                        <tr class="cursor-pointer border-base-300 hover:bg-base-200/70" data-participant-row data-participant-id="{{ participant.pk }}" data-participant-list-id="{{ participant.participant_list_id }}">
                                            <td class="text-center">
                                                <input type="radio" name="{{ form.participant.html_name }}" class="radio radio-primary radio-sm h-4 w-4" value="{{ participant.pk }}" aria-label="Selectează {{ participant.full_name }}" data-participant-checkbox {% if selected_participant_id == participant.pk|stringformat:"s" %}checked{% endif %}>
                                            </td>
                                            <td class="font-mono text-xs text-muted">{{ participant.source_row }}</td>
                                            <td class="max-w-56 truncate font-medium text-base-content" title="{{ participant.full_name }}">{{ participant.full_name }}</td>
                                            <td class="whitespace-nowrap">{{ participant.date_of_birth|date:"d.m.Y" }}</td>
                                            <td class="max-w-56 truncate" title="{{ participant.place_of_birth }}">{{ participant.place_of_birth }}</td>
                                            <td class="whitespace-nowrap font-mono text-xs">{{ participant.certificate_number }}</td>
                                        </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                        <p class="px-3 py-5 text-center text-sm text-muted" data-participant-empty hidden>Selectează mai întâi o listă cu participanți.</p>
                    </div>
                    {% for error in form.participant.errors %}<p class="mt-1 text-xs text-error">{{ error }}</p>{% endfor %}
                    <p class="mt-1.5 text-xs text-muted">PDF-ul va fi generat doar pentru participantul selectat.</p>
                </div>

                <div class="form-control">
                    <label for="{{ form.template.id_for_label }}" class="mb-1.5 text-sm font-semibold text-base-content">{{ form.template.label }}</label>
                    {{ form.template }}
                    {% for error in form.template.errors %}<p class="mt-1 text-xs text-error">{{ error }}</p>{% endfor %}
                    <p class="mt-1.5 text-xs text-muted">Previzualizarea folosește pozițiile și stilurile salvate în template.</p>
                </div>

                <div class="flex flex-col gap-3 border-t border-base-300 pt-5 sm:flex-row sm:items-center sm:justify-between">
                    <button type="submit" class="btn btn-primary btn-sm" {% if not has_participant_lists or not has_templates %}disabled{% endif %}>Previzualizează diploma</button>
                    <div class="flex flex-wrap gap-x-4 gap-y-2 text-sm">
                        <a href="{% url 'diplome:list_index' %}" class="link link-primary link-hover">Administrează liste</a>
                        <a href="{% url 'diplome:template_list' %}" class="link link-primary link-hover">Administrează template-uri</a>
                    </div>
                </div>
            </form>
        </div>

        <aside class="border border-base-300 bg-base-200 p-5 sm:p-6" aria-labelledby="generation-next-step">
            <div class="mx-auto flex aspect-210/297 w-full max-w-52 items-center justify-center border border-base-300 bg-base-100 shadow-sm" aria-hidden="true">
                <div class="w-3/4 space-y-4 text-center">
                    <div class="mx-auto h-1 w-1/3 bg-primary/30"></div>
                    <div class="mx-auto h-2 w-2/3 bg-primary/20"></div>
                    <div class="mx-auto h-px w-full bg-base-300"></div>
                    <div class="mx-auto h-1 w-1/2 bg-base-300"></div>
                    <div class="mx-auto h-1 w-2/3 bg-base-300"></div>
                </div>
            </div>
            <h2 id="generation-next-step" class="mt-6 text-lg font-semibold text-base-content">Pasul următor</h2>
            <p class="mt-2 text-sm leading-6 text-muted">Verifici diploma cu datele reale ale participantului, apoi generezi și descarci fișierul PDF.</p>
            <p class="mt-4 border-l-2 border-primary pl-3 text-xs leading-5 text-muted">O selecție generează o singură diplomă.</p>
        </aside>
    </div>

    <section class="border border-base-300 bg-base-100 p-5 sm:p-6" aria-labelledby="bulk-generation-title">
        <div class="grid gap-6 lg:grid-cols-[minmax(0,1fr)_18rem]">
            <div>
                <h2 id="bulk-generation-title" class="text-lg font-semibold text-primary">Generare pentru întreaga listă</h2>
                <p class="mt-1 text-sm text-muted">Se creează câte un PDF pentru fiecare participant și un lot disponibil ulterior în istoric.</p>

                {% if bulk_form.non_field_errors %}
                    <div class="alert alert-error mt-4 py-2 text-sm" role="alert">
                        {% for error in bulk_form.non_field_errors %}<span>{{ error }}</span>{% endfor %}
                    </div>
                {% endif %}

                <form method="post" action="{% url 'diplome:generation_bulk_create' %}" class="mt-5 grid gap-5 md:grid-cols-2">
                    {% csrf_token %}
                    <div class="form-control">
                        <label for="{{ bulk_form.participant_list.id_for_label }}" class="mb-1.5 text-sm font-semibold text-base-content">{{ bulk_form.participant_list.label }}</label>
                        {{ bulk_form.participant_list }}
                        {% for error in bulk_form.participant_list.errors %}<p class="mt-1 text-xs text-error">{{ error }}</p>{% endfor %}
                    </div>
                    <div class="form-control">
                        <label for="{{ bulk_form.template.id_for_label }}" class="mb-1.5 text-sm font-semibold text-base-content">{{ bulk_form.template.label }}</label>
                        {{ bulk_form.template }}
                        {% for error in bulk_form.template.errors %}<p class="mt-1 text-xs text-error">{{ error }}</p>{% endfor %}
                    </div>
                    <div class="md:col-span-2">
                        <button type="submit" class="btn btn-primary btn-sm" {% if not has_participant_lists or not has_templates %}disabled{% endif %}>Generează diplome pentru toată lista</button>
                    </div>
                </form>
            </div>
            <aside class="border-l-2 border-primary pl-4 text-sm text-muted">
                <p class="font-semibold text-base-content">Rezultatul lotului</p>
                <p class="mt-2 leading-6">După generare vei vedea numărul de fișiere reușite, eventualele erori și descărcarea ZIP.</p>
                <a href="{% url 'diplome:history_index' %}" class="link link-primary link-hover mt-3 inline-block">Deschide istoricul</a>
            </aside>
        </div>
    </section>
</section>
{% endblock %}

{% block page_scripts %}
<script src="{% static 'diplome/generation.js' %}" defer></script>
{% endblock %}
```

## `apps/diplome/templates/diplome/generation_preview.html`

Size: 5.0 KB

```html
{% extends "layouts/base.html" %}
{% load static %}

{% block title %}Previzualizare diplomă | Platforma TUVTK{% endblock %}

{% block page_styles %}
<link rel="stylesheet" href="{% static 'diplome/template_editor.css' %}">
{% endblock %}

{% block content %}
<section class="mx-auto w-full max-w-7xl space-y-6">
    <header class="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div class="space-y-2">
            <div class="breadcrumbs p-0 text-sm text-muted">
                <ul><li>Diplome</li><li><a href="{% url 'diplome:generation_index' %}?{{ selection_query }}">Generare</a></li><li>Previzualizare</li></ul>
            </div>
            <div>
                <h1 class="text-2xl font-bold text-primary">Previzualizare diplomă</h1>
                <p class="mt-1 text-sm text-muted">Verifică datele și aspectul înainte de generarea fișierului PDF.</p>
            </div>
        </div>
        <a href="{% url 'diplome:generation_index' %}?{{ selection_query }}" class="btn btn-outline btn-primary btn-sm">Înapoi la selecție</a>
    </header>

    {% if messages %}
        {% for message in messages %}<div class="alert alert-success py-2 text-sm" role="status"><span>{{ message }}</span></div>{% endfor %}
    {% endif %}

    {% if generated_diploma %}
        <div class="flex flex-col gap-3 border border-success/40 bg-success/10 p-4 sm:flex-row sm:items-center sm:justify-between" role="status">
            <div>
                <p class="font-semibold text-base-content">Diploma PDF a fost generată.</p>
                <p class="mt-1 text-xs text-muted">{{ generated_diploma.created_at|date:"d.m.Y H:i" }} · {{ generated_diploma.participant_name }} · {{ generated_diploma.certificate_number }}</p>
            </div>
            <a href="{% url 'diplome:generation_download' generated_diploma.pk %}" class="btn btn-success btn-sm">Descarcă PDF</a>
        </div>
    {% endif %}

    <div class="grid gap-6 xl:grid-cols-[minmax(0,1fr)_20rem]">
        <div id="generation-diploma-preview" class="overflow-hidden border border-base-300 bg-base-100">
            <div class="preview-workspace !min-h-0 p-4 sm:p-6">
                <div class="preview-canvas-frame" id="preview-canvas-frame">
                    <div class="diploma-canvas preview-canvas" id="preview-canvas" aria-label="Previzualizare diplomă cu datele participantului"></div>
                </div>
            </div>
            {{ layout|json_script:"diploma-layout-data" }}
            {{ participant_data|json_script:"diploma-sample-data" }}
            {{ media_assets|json_script:"diploma-media-assets-data" }}
        </div>

        <aside class="space-y-5 border border-base-300 bg-base-100 p-5">
            <div>
                <h2 class="text-sm font-semibold uppercase tracking-wide text-muted">Participant</h2>
                <p class="mt-2 font-semibold text-base-content">{{ participant.full_name }}</p>
                <dl class="mt-3 space-y-2 text-sm">
                    <div><dt class="text-xs text-muted">Număr certificat</dt><dd class="font-medium text-base-content">{{ participant.certificate_number }}</dd></div>
                    <div><dt class="text-xs text-muted">Data nașterii</dt><dd class="text-base-content">{{ participant.date_of_birth|date:"d.m.Y" }}</dd></div>
                    <div><dt class="text-xs text-muted">Locul nașterii</dt><dd class="text-base-content">{{ participant.place_of_birth }}</dd></div>
                </dl>
            </div>
            <div class="border-t border-base-300 pt-4">
                <h2 class="text-sm font-semibold uppercase tracking-wide text-muted">Sursă și template</h2>
                <dl class="mt-3 space-y-2 text-sm">
                    <div><dt class="text-xs text-muted">Listă</dt><dd class="text-base-content">{{ participant_list.name }}</dd></div>
                    <div><dt class="text-xs text-muted">Template</dt><dd class="text-base-content">{{ diploma_template.name }}</dd></div>
                    <div><dt class="text-xs text-muted">Format</dt><dd class="text-base-content">{{ diploma_template.page_size }} · {{ diploma_template.get_orientation_display }}</dd></div>
                </dl>
            </div>
            <form method="post" action="{% url 'diplome:generation_create' %}" class="border-t border-base-300 pt-5">
                {% csrf_token %}
                <input type="hidden" name="participant_list" value="{{ participant_list.pk }}">
                <input type="hidden" name="participant" value="{{ participant.pk }}">
                <input type="hidden" name="template" value="{{ diploma_template.pk }}">
                <button type="submit" class="btn btn-primary btn-sm w-full">Generează PDF</button>
                <p class="mt-2 text-center text-xs text-muted">Se creează un singur fișier pentru participantul selectat.</p>
            </form>
        </aside>
    </div>
</section>
{% endblock %}

{% block page_scripts %}
<script src="{% static 'diplome/template_renderer.js' %}" defer></script>
<script src="{% static 'diplome/template_preview.js' %}" defer></script>
{% endblock %}
```

## `apps/diplome/templates/diplome/history_index.html`

Size: 884 B

```html
{% extends "layouts/base.html" %}

{% block title %}Istoric generări | Platforma TUVTK{% endblock %}

{% block content %}
<section class="mx-auto w-full max-w-7xl space-y-6">
    <header class="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div class="space-y-2">
            <div class="breadcrumbs p-0 text-sm text-muted">
                <ul><li>Diplome</li><li>Istoric</li></ul>
            </div>
            <div>
                <h1 class="text-2xl font-bold text-primary">Istoric generări</h1>
                <p class="mt-1 text-sm text-muted">Loturile de diplome generate, ordonate de la cel mai recent.</p>
            </div>
        </div>
        <a href="{% url 'diplome:generation_index' %}" class="btn btn-primary btn-sm">Generare nouă</a>
    </header>

    {% include "diplome/includes/history_panel.html" %}
</section>
{% endblock %}
```

## `apps/diplome/templates/diplome/includes/batch_detail_panel.html`

Size: 6.2 KB

```html
<div id="batch-detail-panel" class="space-y-6">
    <header class="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div class="space-y-2">
            <div class="breadcrumbs p-0 text-sm text-muted">
                <ul><li>Diplome</li><li><a href="{% url 'diplome:history_index' %}">Istoric</a></li><li>Detalii lot</li></ul>
            </div>
            <div>
                <h1 class="text-2xl font-bold text-primary">{{ batch.participant_list_display_name }}</h1>
                <p class="mt-1 text-sm text-muted">Template: {{ batch.template_display_name }}</p>
            </div>
        </div>
        <div class="flex flex-wrap gap-2">
            {% if batch.status == 'pending' %}
                <form
                    method="post"
                    action="{% url 'diplome:batch_resume' batch.pk %}"
                    hx-post="{% url 'diplome:batch_resume' batch.pk %}"
                    hx-target="#batch-detail-panel"
                    hx-swap="outerHTML show:top"
                    hx-confirm="Reiei generarea acestui lot?"
                >
                    {% csrf_token %}
                    <button type="submit" class="btn btn-primary btn-sm">Reia generarea</button>
                </form>
            {% endif %}
            <a href="{% url 'diplome:history_index' %}" class="btn btn-outline btn-primary btn-sm">Înapoi la istoric</a>
            {% if batch.success_count %}<a href="{% url 'diplome:batch_zip_download' batch.pk %}" class="btn btn-primary btn-sm">Descarcă ZIP</a>{% endif %}
        </div>
    </header>

    {% include "diplome/includes/messages.html" %}

    <div class="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        <div class="border border-base-300 bg-base-100 p-4">
            <p class="text-xs font-semibold uppercase tracking-wide text-muted">Status</p>
            <p class="mt-2 font-semibold text-base-content">{{ batch.get_status_display }}</p>
        </div>
        <div class="border border-base-300 bg-base-100 p-4">
            <p class="text-xs font-semibold uppercase tracking-wide text-muted">Total</p>
            <p class="mt-2 text-xl font-bold text-base-content">{{ batch.total_count }}</p>
        </div>
        <div class="border border-success/40 bg-success/10 p-4">
            <p class="text-xs font-semibold uppercase tracking-wide text-muted">Generate</p>
            <p class="mt-2 text-xl font-bold text-success">{{ batch.success_count }}</p>
        </div>
        <div class="border border-error/40 bg-error/10 p-4">
            <p class="text-xs font-semibold uppercase tracking-wide text-muted">Eșuate</p>
            <p class="mt-2 text-xl font-bold text-error">{{ batch.failed_count }}</p>
        </div>
    </div>

    <dl class="grid gap-3 border border-base-300 bg-base-100 p-4 text-sm sm:grid-cols-3">
        <div><dt class="text-xs text-muted">Creat</dt><dd class="mt-1 text-base-content">{{ batch.created_at|date:"d.m.Y H:i" }}</dd></div>
        <div><dt class="text-xs text-muted">Început</dt><dd class="mt-1 text-base-content">{% if batch.started_at %}{{ batch.started_at|date:"d.m.Y H:i" }}{% else %}—{% endif %}</dd></div>
        <div><dt class="text-xs text-muted">Finalizat</dt><dd class="mt-1 text-base-content">{% if batch.completed_at %}{{ batch.completed_at|date:"d.m.Y H:i" }}{% else %}—{% endif %}</dd></div>
    </dl>

    {% if batch.error_summary %}
        <section class="border border-warning/40 bg-warning/10 p-4" aria-labelledby="batch-errors-title">
            <h2 id="batch-errors-title" class="font-semibold text-base-content">Erori de generare</h2>
            <ul class="mt-2 space-y-1 text-sm text-muted">
                {% for error in batch.error_summary %}
                    <li>{% if error.participant_name %}<span class="font-medium text-base-content">{{ error.participant_name }}</span>{% if error.certificate_number %} ({{ error.certificate_number }}){% endif %}: {% endif %}{{ error.message }}</li>
                {% endfor %}
            </ul>
        </section>
    {% endif %}

    <section class="space-y-3" aria-labelledby="generated-pdfs-title">
        <h2 id="generated-pdfs-title" class="text-lg font-semibold text-primary">Fișiere PDF generate</h2>
        <div class="overflow-x-auto border border-base-300 bg-base-100">
            <table class="table table-xs">
                <thead><tr><th>Participant</th><th>Număr certificat</th><th>Status</th><th>Creat</th><th class="text-right">Acțiuni</th></tr></thead>
                <tbody>
                    {% for diploma in generated_diplomas %}
                        <tr>
                            <td class="font-medium text-base-content">{{ diploma.participant_name }}</td>
                            <td>{{ diploma.certificate_number }}</td>
                            <td><span class="badge badge-success badge-sm">Disponibil</span></td>
                            <td class="whitespace-nowrap">{{ diploma.created_at|date:"d.m.Y H:i" }}</td>
                            <td>
                                <div class="flex justify-end">
                                    <a
                                        href="{% url 'diplome:generation_download' diploma.pk %}"
                                        class="btn btn-square btn-ghost btn-xs text-success hover:bg-success/10"
                                        aria-label="Descarcă diploma PDF"
                                        title="Descarcă diploma PDF"
                                    >
                                        <svg xmlns="http://www.w3.org/2000/svg" class="size-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M12 3.75v11.5m0 0 4-4m-4 4-4-4M5 19.25h14" />
                                        </svg>
                                    </a>
                                </div>
                            </td>
                        </tr>
                    {% empty %}
                        <tr><td colspan="5" class="py-10 text-center text-muted">Nu a fost generat niciun fișier PDF.</td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </section>
</div>
```

## `apps/diplome/templates/diplome/includes/history_panel.html`

Size: 8.0 KB

```html
<div id="history-panel" class="space-y-4">
    {% include "diplome/includes/messages.html" %}

    <form
        method="get"
        action="{% url 'diplome:history_index' %}"
        class="grid gap-3 border border-base-300 bg-base-100 p-4 sm:grid-cols-2 lg:grid-cols-5"
        hx-get="{% url 'diplome:history_index' %}"
        hx-target="#history-panel"
        hx-swap="outerHTML show:top"
        hx-push-url="true"
        hx-indicator="#history-loading"
        hx-trigger="submit, change delay:250ms"
        hx-sync="this:replace"
        hx-disabled-elt="find input, find select, find button"
    >
        <div>
            <label for="{{ filter_form.participant_list.id_for_label }}" class="mb-1 block text-xs font-semibold text-muted">{{ filter_form.participant_list.label }}</label>
            {{ filter_form.participant_list }}
        </div>
        <div>
            <label for="{{ filter_form.template.id_for_label }}" class="mb-1 block text-xs font-semibold text-muted">{{ filter_form.template.label }}</label>
            {{ filter_form.template }}
        </div>
        <div>
            <label for="{{ filter_form.status.id_for_label }}" class="mb-1 block text-xs font-semibold text-muted">{{ filter_form.status.label }}</label>
            {{ filter_form.status }}
        </div>
        <div>
            <label for="{{ filter_form.date.id_for_label }}" class="mb-1 block text-xs font-semibold text-muted">{{ filter_form.date.label }}</label>
            {{ filter_form.date }}
        </div>
        <div class="flex items-end gap-2">
            <button type="submit" class="btn btn-primary btn-sm">Filtrează</button>
            <a
                href="{% url 'diplome:history_index' %}"
                class="btn btn-ghost btn-sm"
                hx-get="{% url 'diplome:history_index' %}"
                hx-target="#history-panel"
                hx-swap="outerHTML show:top"
                hx-push-url="true"
                hx-indicator="#history-loading"
            >Resetează</a>
        </div>
    </form>

    <div class="relative overflow-x-auto border border-base-300 bg-base-100" aria-live="polite">
        <div
            id="history-loading"
            class="htmx-indicator absolute inset-0 z-10 flex items-center justify-center bg-base-100/80"
            role="status"
        >
            <span class="inline-flex items-center gap-3 border border-base-300 bg-base-100 px-4 py-3 text-sm font-medium text-base-content shadow-sm">
                <span class="loading loading-spinner loading-md text-primary" aria-hidden="true"></span>
                Se actualizează istoricul
            </span>
        </div>
        <table class="table table-xs">
            <thead>
                <tr>
                    <th>Listă</th>
                    <th>Template</th>
                    <th>Status</th>
                    <th class="text-right">Reușite</th>
                    <th class="text-right">Erori</th>
                    <th>Creat</th>
                    <th class="text-right">Acțiuni</th>
                </tr>
            </thead>
            <tbody>
                {% for batch in batches %}
                    <tr>
                        <td class="font-medium text-base-content">{{ batch.participant_list_display_name }}</td>
                        <td>{{ batch.template_display_name }}</td>
                        <td>
                            <span class="badge badge-sm {% if batch.status == 'completed' %}badge-success{% elif batch.status == 'completed_with_errors' %}badge-warning{% elif batch.status == 'failed' %}badge-error{% else %}badge-ghost{% endif %}">{{ batch.get_status_display }}</span>
                        </td>
                        <td class="text-right">{{ batch.success_count }}/{{ batch.total_count }}</td>
                        <td class="text-right">{{ batch.failed_count }}</td>
                        <td class="whitespace-nowrap">{{ batch.created_at|date:"d.m.Y H:i" }}</td>
                        <td>
                            <div class="flex justify-end gap-1">
                                {% if batch.status == 'pending' %}
                                    <form
                                        method="post"
                                        action="{% url 'diplome:batch_resume' batch.pk %}{% if request.GET.urlencode %}?{{ request.GET.urlencode }}{% endif %}"
                                        class="inline-flex"
                                        hx-post="{% url 'diplome:batch_resume' batch.pk %}{% if request.GET.urlencode %}?{{ request.GET.urlencode }}{% endif %}"
                                        hx-target="#history-panel"
                                        hx-swap="outerHTML show:top"
                                        hx-confirm="Reiei generarea acestui lot?"
                                    >
                                        {% csrf_token %}
                                        <button
                                            type="submit"
                                            class="btn btn-square btn-ghost btn-xs text-primary hover:bg-primary/10"
                                            aria-label="Reia generarea lotului"
                                            title="Reia generarea lotului"
                                        >
                                            <svg xmlns="http://www.w3.org/2000/svg" class="size-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M8.25 6.75v-3m0 0h-3m3 0L5.6 6.4a7.5 7.5 0 1 0 2.15-1.45M10 8.75l5 3.25-5 3.25v-6.5Z" />
                                            </svg>
                                        </button>
                                    </form>
                                {% endif %}
                                <a
                                    href="{% url 'diplome:batch_detail' batch.pk %}"
                                    class="btn btn-square btn-ghost btn-xs text-primary hover:bg-primary/10"
                                    aria-label="Vezi detaliile lotului"
                                    title="Vezi detaliile lotului"
                                >
                                    <svg xmlns="http://www.w3.org/2000/svg" class="size-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M14 3.75H6.75A1.75 1.75 0 0 0 5 5.5v13A1.75 1.75 0 0 0 6.75 20.25h6.5M14 3.75v4.5h4.5M14 3.75l4.5 4.5v3.25M17.25 14.25a3 3 0 1 0 0 6 3 3 0 0 0 0-6Zm2.15 5.15 2.1 2.1" />
                                    </svg>
                                </a>
                                {% if batch.success_count %}
                                    <a
                                        href="{% url 'diplome:batch_zip_download' batch.pk %}"
                                        class="btn btn-square btn-ghost btn-xs text-success hover:bg-success/10"
                                        aria-label="Descarcă lotul ca arhivă ZIP"
                                        title="Descarcă lotul ca arhivă ZIP"
                                    >
                                        <svg xmlns="http://www.w3.org/2000/svg" class="size-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M12 3.75v11.5m0 0 4-4m-4 4-4-4M5 19.25h14" />
                                        </svg>
                                    </a>
                                {% endif %}
                            </div>
                        </td>
                    </tr>
                {% empty %}
                    <tr><td colspan="7" class="py-10 text-center text-muted">Nu există loturi pentru filtrele selectate.</td></tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
```

## `apps/diplome/templates/diplome/includes/messages.html`

Size: 522 B

```html
{% if messages %}
    <div class="space-y-2">
        {% for message in messages %}
            <div
                class="alert {% if message.tags == 'error' %}alert-error{% elif message.tags == 'warning' %}alert-warning{% elif message.tags == 'info' %}alert-info{% else %}alert-success{% endif %} py-2 text-sm"
                role="{% if message.tags == 'error' %}alert{% else %}status{% endif %}"
            >
                <span>{{ message }}</span>
            </div>
        {% endfor %}
    </div>
{% endif %}
```

## `apps/diplome/templates/diplome/includes/participant_list_detail_panel.html`

Size: 2.9 KB

```html
<div id="participant-list-detail-panel" class="space-y-4">
    {% include "diplome/includes/messages.html" %}

    <div class="relative overflow-x-auto border border-base-300 bg-base-100" aria-live="polite">
        <div
            id="participant-detail-loading"
            class="htmx-indicator absolute inset-0 z-10 flex items-center justify-center bg-base-100/80"
            role="status"
        >
            <span class="inline-flex items-center gap-3 border border-base-300 bg-base-100 px-4 py-3 text-sm font-medium text-base-content shadow-sm">
                <span class="loading loading-spinner loading-md text-primary" aria-hidden="true"></span>
                Se actualizează participanții
            </span>
        </div>
        <table class="table table-sm">
            <thead class="bg-base-200 text-xs uppercase tracking-wide text-muted"><tr><th>#</th><th>Nume complet</th><th>Data nașterii</th><th>Locul nașterii</th><th>Număr certificat</th></tr></thead>
            <tbody>
                {% for participant in participants %}
                    <tr><td>{{ page_obj.start_index|add:forloop.counter0 }}</td><td class="font-medium">{{ participant.full_name }}</td><td>{{ participant.date_of_birth|date:"d.m.Y" }}</td><td>{{ participant.place_of_birth }}</td><td>{{ participant.certificate_number }}</td></tr>
                {% empty %}
                    <tr><td colspan="5" class="py-8 text-center text-muted">Lista nu conține participanți.</td></tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    {% if is_paginated %}
        <nav class="flex items-center justify-between text-sm" aria-label="Paginare participanți">
            <span class="text-muted">Pagina {{ page_obj.number }} din {{ page_obj.paginator.num_pages }}</span>
            <div class="join">
                {% if page_obj.has_previous %}
                    <a
                        href="?page={{ page_obj.previous_page_number }}"
                        class="btn btn-sm join-item"
                        hx-get="?page={{ page_obj.previous_page_number }}"
                        hx-target="#participant-list-detail-panel"
                        hx-swap="outerHTML show:top"
                        hx-push-url="true"
                        hx-indicator="#participant-detail-loading"
                    >Anterior</a>
                {% endif %}
                {% if page_obj.has_next %}
                    <a
                        href="?page={{ page_obj.next_page_number }}"
                        class="btn btn-sm join-item"
                        hx-get="?page={{ page_obj.next_page_number }}"
                        hx-target="#participant-list-detail-panel"
                        hx-swap="outerHTML show:top"
                        hx-push-url="true"
                        hx-indicator="#participant-detail-loading"
                    >Următor</a>
                {% endif %}
            </div>
        </nav>
    {% endif %}
</div>
```

## `apps/diplome/templates/diplome/includes/participant_list_panel.html`

Size: 5.3 KB

```html
<div id="participant-list-panel" class="space-y-4">
    {% include "diplome/includes/messages.html" %}

    <div class="relative overflow-hidden border border-base-300 bg-base-100" aria-live="polite">
        <div
            id="participant-list-loading"
            class="htmx-indicator absolute inset-0 z-10 flex items-center justify-center bg-base-100/80"
            role="status"
        >
            <span class="inline-flex items-center gap-3 border border-base-300 bg-base-100 px-4 py-3 text-sm font-medium text-base-content shadow-sm">
                <span class="loading loading-spinner loading-md text-primary" aria-hidden="true"></span>
                Se actualizează listele
            </span>
        </div>
        {% if participant_lists %}
            <div class="overflow-x-auto">
                <table class="table table-sm">
                    <thead class="bg-base-200 text-xs uppercase tracking-wide text-muted">
                        <tr><th>Listă</th><th>Curs</th><th>Participanți</th><th>Fișier sursă</th><th>Creată</th><th class="text-right">Acțiuni</th></tr>
                    </thead>
                    <tbody>
                        {% for participant_list in participant_lists %}
                            <tr>
                                <td>
                                    <a href="{% url 'diplome:participant_list_detail' participant_list.pk %}" class="font-semibold text-primary hover:underline">{{ participant_list.name }}</a>
                                    {% if participant_list.description %}<p class="mt-0.5 max-w-lg text-xs text-muted">{{ participant_list.description }}</p>{% endif %}
                                </td>
                                <td>{{ participant_list.course_name|default:"—" }}</td>
                                <td>{{ participant_list.participant_count }}</td>
                                <td>{{ participant_list.source_file_name }}</td>
                                <td class="whitespace-nowrap">{{ participant_list.created_at|date:"d.m.Y H:i" }}</td>
                                <td>
                                    <div class="flex justify-end gap-2">
                                        <a href="{% url 'diplome:participant_list_detail' participant_list.pk %}" class="btn btn-outline btn-primary btn-xs">Deschide</a>
                                        <form
                                            method="post"
                                            action="{% url 'diplome:participant_list_delete' participant_list.pk %}{% if request.GET.urlencode %}?{{ request.GET.urlencode }}{% endif %}"
                                            hx-post="{% url 'diplome:participant_list_delete' participant_list.pk %}{% if request.GET.urlencode %}?{{ request.GET.urlencode }}{% endif %}"
                                            hx-target="#participant-list-panel"
                                            hx-swap="outerHTML show:top"
                                            hx-confirm="Ștergi această listă de participanți?"
                                        >
                                            {% csrf_token %}
                                            <button type="submit" class="btn btn-ghost btn-xs text-error">Șterge</button>
                                        </form>
                                    </div>
                                </td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        {% else %}
            <div class="px-6 py-14 text-center">
                <h2 class="text-lg font-semibold text-base-content">Nu există liste de participanți</h2>
                <p class="mt-2 text-sm text-muted">Importă un fișier CSV sau XLSX pentru a crea prima listă.</p>
                <a href="{% url 'diplome:participant_import' %}" class="btn btn-primary btn-sm mt-5">Importă prima listă</a>
            </div>
        {% endif %}
    </div>
    {% if is_paginated %}
        <nav class="flex items-center justify-between text-sm" aria-label="Paginare liste participanți">
            <span class="text-muted">Pagina {{ page_obj.number }} din {{ page_obj.paginator.num_pages }}</span>
            <div class="join">
                {% if page_obj.has_previous %}
                    <a
                        href="?page={{ page_obj.previous_page_number }}"
                        class="btn btn-sm join-item"
                        hx-get="?page={{ page_obj.previous_page_number }}"
                        hx-target="#participant-list-panel"
                        hx-swap="outerHTML show:top"
                        hx-push-url="true"
                        hx-indicator="#participant-list-loading"
                    >Anterior</a>
                {% endif %}
                {% if page_obj.has_next %}
                    <a
                        href="?page={{ page_obj.next_page_number }}"
                        class="btn btn-sm join-item"
                        hx-get="?page={{ page_obj.next_page_number }}"
                        hx-target="#participant-list-panel"
                        hx-swap="outerHTML show:top"
                        hx-push-url="true"
                        hx-indicator="#participant-list-loading"
                    >Următor</a>
                {% endif %}
            </div>
        </nav>
    {% endif %}
</div>
```

## `apps/diplome/templates/diplome/includes/template_list_panel.html`

Size: 6.4 KB

```html
<div id="template-list-panel" class="space-y-4">
    {% include "diplome/includes/messages.html" %}

    <form
        method="get"
        action="{% url 'diplome:template_list' %}"
        class="flex flex-col gap-3 border border-base-300 bg-base-100 p-4 sm:flex-row sm:items-end"
        hx-get="{% url 'diplome:template_list' %}"
        hx-target="#template-list-panel"
        hx-swap="outerHTML show:top"
        hx-push-url="true"
        hx-indicator="#template-list-loading"
        hx-trigger="submit, change delay:250ms"
        hx-sync="this:replace"
        hx-disabled-elt="find select, find button"
    >
        <label class="form-control">
            <span class="label-text mb-1 text-xs font-semibold uppercase tracking-wide text-muted">Categorie</span>
            {{ filter_form.category }}
        </label>
        <div class="flex items-center gap-2">
            <button type="submit" class="btn btn-primary btn-sm">Filtrează</button>
            {% if selected_category %}
                <a
                    href="{% url 'diplome:template_list' %}"
                    class="btn btn-ghost btn-sm"
                    hx-get="{% url 'diplome:template_list' %}"
                    hx-target="#template-list-panel"
                    hx-swap="outerHTML show:top"
                    hx-push-url="true"
                    hx-indicator="#template-list-loading"
                >Șterge filtrul</a>
            {% endif %}
        </div>
    </form>

    <div class="relative overflow-hidden border border-base-300 bg-base-100" aria-live="polite">
        <div
            id="template-list-loading"
            class="htmx-indicator absolute inset-0 z-10 flex items-center justify-center bg-base-100/80"
            role="status"
        >
            <span class="inline-flex items-center gap-3 border border-base-300 bg-base-100 px-4 py-3 text-sm font-medium text-base-content shadow-sm">
                <span class="loading loading-spinner loading-md text-primary" aria-hidden="true"></span>
                Se actualizează template-urile
            </span>
        </div>
        {% if templates %}
            <div class="overflow-x-auto">
                <table class="table table-sm">
                    <thead class="bg-base-200 text-xs uppercase tracking-wide text-muted">
                        <tr>
                            <th>Nume</th>
                            <th>Categorie</th>
                            <th>Format</th>
                            <th>Stare</th>
                            <th>Actualizat</th>
                            <th class="text-right">Acțiuni</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for diploma_template in templates %}
                            <tr>
                                <td>
                                    <p class="font-semibold text-base-content">{{ diploma_template.name }}</p>
                                    {% if diploma_template.description %}<p class="mt-0.5 max-w-xl text-xs text-muted">{{ diploma_template.description }}</p>{% endif %}
                                </td>
                                <td><span class="badge badge-outline badge-sm">{{ diploma_template.category }}</span></td>
                                <td>{{ diploma_template.page_size }} · {{ diploma_template.get_orientation_display }}</td>
                                <td>{% if diploma_template.is_active %}<span class="text-success">Activ</span>{% else %}<span class="text-muted">Inactiv</span>{% endif %}</td>
                                <td>{{ diploma_template.updated_at|date:"d.m.Y H:i" }}</td>
                                <td>
                                    <div class="flex justify-end gap-2">
                                        <a href="{% url 'diplome:template_editor' diploma_template.pk %}" class="btn btn-outline btn-primary btn-xs">Editează</a>
                                        <a href="{% url 'diplome:template_preview' diploma_template.pk %}" class="btn btn-ghost btn-xs" target="_blank" rel="noopener">Preview</a>
                                        <form
                                            method="post"
                                            action="{% url 'diplome:template_delete' diploma_template.pk %}{% if request.GET.urlencode %}?{{ request.GET.urlencode }}{% endif %}"
                                            hx-post="{% url 'diplome:template_delete' diploma_template.pk %}{% if request.GET.urlencode %}?{{ request.GET.urlencode }}{% endif %}"
                                            hx-target="#template-list-panel"
                                            hx-swap="outerHTML show:top"
                                            hx-confirm="Ștergi acest template?"
                                        >
                                            {% csrf_token %}
                                            <button type="submit" class="btn btn-ghost btn-xs text-error">Șterge</button>
                                        </form>
                                    </div>
                                </td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        {% else %}
            <div class="px-6 py-14 text-center">
                {% if selected_category %}
                    <h2 class="text-lg font-semibold text-base-content">Niciun template în categoria „{{ selected_category }}”</h2>
                    <p class="mt-2 text-sm text-muted">Alege o altă categorie sau elimină filtrul curent.</p>
                    <a
                        href="{% url 'diplome:template_list' %}"
                        class="btn btn-outline btn-primary btn-sm mt-5"
                        hx-get="{% url 'diplome:template_list' %}"
                        hx-target="#template-list-panel"
                        hx-swap="outerHTML show:top"
                        hx-push-url="true"
                    >Afișează toate template-urile</a>
                {% else %}
                    <h2 class="text-lg font-semibold text-base-content">Nu există template-uri</h2>
                    <p class="mt-2 text-sm text-muted">Creează primul template și configurează-l în editorul vizual.</p>
                    <a href="{% url 'diplome:template_create' %}" class="btn btn-primary btn-sm mt-5">Creează primul template</a>
                {% endif %}
            </div>
        {% endif %}
    </div>
</div>
```

## `apps/diplome/templates/diplome/participant_import.html`

Size: 3.8 KB

```html
{% extends "layouts/base.html" %}
{% load static %}

{% block title %}Import participanți | Platforma TUVTK{% endblock %}

{% block content %}
<section class="mx-auto w-full max-w-2xl space-y-6">
    <div class="space-y-2">
        <div class="breadcrumbs p-0 text-sm text-muted"><ul><li>Diplome</li><li><a href="{% url 'diplome:list_index' %}">Liste participanți</a></li><li>Import</li></ul></div>
        <div>
            <h1 class="text-2xl font-bold text-primary">Importă participanți</h1>
            <p class="mt-1 text-sm text-muted">Completează detaliile listei și încarcă fișierul pentru verificare.</p>
        </div>
    </div>

    <form method="post" enctype="multipart/form-data" class="space-y-5 border border-base-300 bg-base-100 p-6" data-participant-import-form novalidate>
        {% csrf_token %}
        {% if form.non_field_errors %}<div class="alert alert-error py-2 text-sm">{{ form.non_field_errors }}</div>{% endif %}
        <label class="form-control w-full">
            <span class="label-text mb-1 text-sm font-semibold">Numele listei</span>
            {{ form.list_name }}
            {% for error in form.list_name.errors %}<span class="mt-1 text-xs text-error">{{ error }}</span>{% endfor %}
        </label>
        <label class="form-control w-full">
            <span class="label-text mb-1 text-sm font-semibold">Descriere <span class="font-normal text-muted">(opțional)</span></span>
            {{ form.description }}
            {% for error in form.description.errors %}<span class="mt-1 text-xs text-error">{{ error }}</span>{% endfor %}
        </label>
        <label class="form-control w-full">
            <span class="label-text mb-1 text-sm font-semibold">Denumirea cursului <span class="font-normal text-muted">(opțional)</span></span>
            {{ form.course_name }}
            {% for error in form.course_name.errors %}<span class="mt-1 text-xs text-error">{{ error }}</span>{% endfor %}
        </label>
        <label class="form-control w-full">
            <span class="label-text mb-1 text-sm font-semibold">Fișier CSV sau XLSX</span>
            {{ form.source_file }}
            <span class="mt-2 text-xs text-muted">Fișierul trebuie să conțină valorile pentru nume, data și locul nașterii și numărul certificatului. Denumirile coloanelor sunt libere și vor fi asociate în pasul următor. Pentru un XLSX cu mai multe foi valide, vei alege foaia pe care dorești să o imporți. Data trebuie scrisă strict DD.MM.YYYY.</span>
            {% for error in form.source_file.errors %}<span class="mt-1 text-xs text-error">{{ error }}</span>{% endfor %}
        </label>
        <label class="flex cursor-pointer items-center gap-3 border border-base-300 bg-base-200/50 p-3">
            {{ form.first_row_has_headers }}
            <span>
                <span class="block text-sm font-semibold">Primul rând conține denumirile coloanelor</span>
                <span class="block text-xs text-muted">Debifează pentru fișiere fără antet; coloanele vor fi numerotate automat.</span>
            </span>
        </label>
        <div class="flex justify-end gap-2 border-t border-base-300 pt-5">
            <a href="{% url 'diplome:list_index' %}" class="btn btn-ghost btn-sm">Renunță</a>
            <button type="submit" class="btn btn-primary btn-sm">Descoperă coloanele</button>
        </div>
    </form>
</section>

<div class="toast toast-top toast-end z-50{% if not form.list_name.errors %} hidden{% endif %}" data-participant-import-toast aria-live="assertive" aria-atomic="true">
    <div class="alert alert-error text-sm shadow-lg" role="alert">
        <span data-participant-import-toast-message>{% if form.list_name.errors %}{{ form.list_name.errors.0 }}{% endif %}</span>
    </div>
</div>
{% endblock %}

{% block page_scripts %}
<script src="{% static 'diplome/participant_import.js' %}" defer></script>
{% endblock %}
```

## `apps/diplome/templates/diplome/participant_import_mapping.html`

Size: 5.7 KB

```html
{% extends "layouts/base.html" %}
{% load static %}

{% block title %}Asociere coloane | Platforma TUVTK{% endblock %}

{% block content %}
<section class="mx-auto w-full max-w-6xl space-y-8">
    <div class="space-y-2">
        <div class="breadcrumbs p-0 text-sm text-muted"><ul><li>Diplome</li><li><a href="{% url 'diplome:list_index' %}">Liste participanți</a></li><li>Asociere coloane</li></ul></div>
        <div>
            <h1 class="text-2xl font-bold text-primary">Importă și asociază datele</h1>
            <p class="mt-1 text-sm text-muted">Fișierul {{ draft.source_file_name }} conține {{ draft.source_rows_json|length }} rânduri și {{ draft.source_columns_json|length }} coloane.</p>
        </div>
    </div>

    <section class="space-y-3" aria-labelledby="source-preview-title">
        <div>
            <h2 id="source-preview-title" class="text-lg font-semibold text-base-content"><span class="mr-2 inline-flex size-6 items-center justify-center rounded-full border border-base-content text-sm">1</span>Verifică datele importate</h2>
            <p class="mt-1 pl-8 text-sm text-muted">Primele cinci rânduri sunt afișate pentru orientare.</p>
        </div>
        <div class="overflow-x-auto border border-base-300 bg-base-100">
            <table class="table table-sm">
                <thead class="bg-base-200 text-xs uppercase tracking-wide text-muted">
                    <tr>{% for column in draft.source_columns_json %}<th>{{ column.label }}</th>{% endfor %}</tr>
                </thead>
                <tbody>
                    {% for row in draft.source_rows_json|slice:":5" %}
                        <tr>{% for value in row.values %}<td class="max-w-64 truncate">{{ value|default:"—" }}</td>{% endfor %}</tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </section>

    <form method="post" class="space-y-5" data-mapping-form>
        {% csrf_token %}
        <div>
            <h2 class="text-lg font-semibold text-base-content"><span class="mr-2 inline-flex size-6 items-center justify-center rounded-full border border-base-content text-sm">2</span>Asociază coloanele</h2>
            <p class="mt-1 pl-8 text-sm text-muted">Pentru fiecare coloană din fișier, selectează câmpul predefinit din sistem. Coloanele suplimentare pot rămâne pe „Nu importa”.</p>
        </div>

        {% if form.non_field_errors %}
            <div class="alert alert-error py-3 text-sm" role="alert">{{ form.non_field_errors }}</div>
        {% endif %}

        <div class="hidden grid-cols-[minmax(10rem,0.8fr)_minmax(16rem,1.5fr)_minmax(14rem,1fr)_7rem] gap-5 px-5 text-xs font-semibold uppercase tracking-wide text-muted md:grid">
            <span>Coloană din fișier</span>
            <span>Date detectate</span>
            <span>Câmp în sistem</span>
            <span>Stare</span>
        </div>

        <div class="space-y-3">
            {% for row in mapping_rows %}
                <div class="grid gap-4 border border-base-300 bg-base-100 p-5 transition-colors md:grid-cols-[minmax(10rem,0.8fr)_minmax(16rem,1.5fr)_minmax(14rem,1fr)_7rem] md:items-center md:gap-5" data-mapping-row>
                    <div>
                        <span class="mb-1 block text-xs font-semibold uppercase tracking-wide text-muted md:hidden">Coloană din fișier</span>
                        <p class="font-semibold text-base-content">{{ row.column.label }}</p>
                    </div>
                    <div>
                        <span class="mb-1 block text-xs font-semibold uppercase tracking-wide text-muted md:hidden">Date detectate</span>
                        <ul class="space-y-0.5 text-sm text-base-content">
                            {% for sample in row.column.samples %}<li class="truncate">{{ sample }}</li>{% empty %}<li class="text-muted">—</li>{% endfor %}
                        </ul>
                    </div>
                    <label class="form-control w-full">
                        <span class="mb-1 block text-xs font-semibold uppercase tracking-wide text-muted md:hidden">Câmp în sistem</span>
                        {{ row.field }}
                        {% for error in row.field.errors %}<span class="mt-1 text-xs text-error">{{ error }}</span>{% endfor %}
                    </label>
                    <div class="flex items-center gap-2 text-sm text-muted" data-mapping-status>
                        <svg class="hidden size-5 text-success" data-mapped-icon viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path fill-rule="evenodd" d="M10 18a8 8 0 1 0 0-16 8 8 0 0 0 0 16Zm3.7-9.3a1 1 0 0 0-1.4-1.4L9 10.6 7.7 9.3a1 1 0 0 0-1.4 1.4l2 2a1 1 0 0 0 1.4 0l4-4Z" clip-rule="evenodd"/></svg>
                        <svg class="size-5" data-ignored-icon viewBox="0 0 20 20" fill="currentColor" aria-hidden="true"><path fill-rule="evenodd" d="M4 10a1 1 0 0 1 1-1h10a1 1 0 1 1 0 2H5a1 1 0 0 1-1-1Z" clip-rule="evenodd"/></svg>
                        <span data-status-label>Ignorată</span>
                    </div>
                </div>
            {% endfor %}
        </div>

        <div class="flex flex-col gap-3 border-t border-base-300 pt-5 sm:flex-row sm:items-center sm:justify-between">
            <p class="text-sm text-muted"><span class="font-semibold text-base-content" data-mapped-count>0</span> din 4 câmpuri obligatorii asociate</p>
            <div class="flex justify-end gap-2">
                <a href="{% url 'diplome:participant_import' %}" class="btn btn-ghost btn-sm">Încarcă alt fișier</a>
                <button type="submit" class="btn btn-primary btn-sm">Continuă la verificare</button>
            </div>
        </div>
    </form>
</section>
{% endblock %}

{% block page_scripts %}
<script src="{% static 'diplome/participant_mapping.js' %}" defer></script>
{% endblock %}
```

## `apps/diplome/templates/diplome/participant_import_preview.html`

Size: 3.5 KB

```html
{% extends "layouts/base.html" %}

{% block title %}Verificare import | Platforma TUVTK{% endblock %}

{% block content %}
<section class="mx-auto w-full max-w-7xl space-y-6">
    <div class="space-y-2">
        <div class="breadcrumbs p-0 text-sm text-muted"><ul><li>Diplome</li><li><a href="{% url 'diplome:list_index' %}">Liste participanți</a></li><li>Verificare import</li></ul></div>
        <div>
            <h1 class="text-2xl font-bold text-primary">Verifică lista „{{ draft.list_name }}”</h1>
            <p class="mt-1 text-sm text-muted">{{ draft.source_file_name }} · {{ draft.valid_rows_json|length }} rânduri valide · {{ draft.invalid_rows_json|length }} rânduri invalide</p>
        </div>
    </div>

    {% if messages %}{% for message in messages %}<div class="alert alert-error py-2 text-sm" role="alert"><span>{{ message }}</span></div>{% endfor %}{% endif %}
    {% if draft.warnings_json %}
        <div class="alert alert-warning items-start py-3 text-sm" role="status">
            <div><p class="font-semibold">Avertismente</p><ul class="mt-1 list-disc pl-5">{% for warning in draft.warnings_json %}<li>{{ warning }}</li>{% endfor %}</ul></div>
        </div>
    {% endif %}

    {% if draft.invalid_rows_json %}
        <div class="space-y-2">
            <h2 class="text-lg font-semibold text-error">Rânduri invalide</h2>
            <div class="overflow-x-auto border border-error/30 bg-base-100">
                <table class="table table-sm">
                    <thead class="bg-error/10"><tr><th>Rând</th><th>Nume complet</th><th>Data nașterii</th><th>Locul nașterii</th><th>Număr certificat</th><th>Erori</th></tr></thead>
                    <tbody>{% for row in draft.invalid_rows_json %}<tr><td>{{ row.source_row }}</td><td>{{ row.full_name|default:"—" }}</td><td>{{ row.date_of_birth|default:"—" }}</td><td>{{ row.place_of_birth|default:"—" }}</td><td>{{ row.certificate_number|default:"—" }}</td><td class="text-error">{{ row.errors|join:" " }}</td></tr>{% endfor %}</tbody>
                </table>
            </div>
        </div>
    {% endif %}

    <div class="space-y-2">
        <h2 class="text-lg font-semibold text-base-content">Rânduri valide</h2>
        <div class="overflow-x-auto border border-base-300 bg-base-100">
            {% if draft.valid_rows_json %}
                <table class="table table-sm">
                    <thead class="bg-base-200"><tr><th>Rând</th><th>Nume complet</th><th>Data nașterii</th><th>Locul nașterii</th><th>Număr certificat</th></tr></thead>
                    <tbody>{% for row in draft.valid_rows_json %}<tr><td>{{ row.source_row }}</td><td class="font-medium">{{ row.full_name }}</td><td>{{ row.date_of_birth }}</td><td>{{ row.place_of_birth }}</td><td>{{ row.certificate_number }}</td></tr>{% endfor %}</tbody>
                </table>
            {% else %}
                <p class="px-5 py-8 text-center text-sm text-muted">Nu există rânduri valide pentru import.</p>
            {% endif %}
        </div>
    </div>

    <div class="flex justify-end gap-2 border-t border-base-300 pt-5">
        <a href="{% url 'diplome:participant_import' %}" class="btn btn-ghost btn-sm">Încarcă alt fișier</a>
        <form method="post" action="{% url 'diplome:participant_import_confirm' draft.pk %}">
            {% csrf_token %}
            <button type="submit" class="btn btn-primary btn-sm" {% if not draft.valid_rows_json %}disabled{% endif %}>Confirmă importul</button>
        </form>
    </div>
</section>
{% endblock %}
```

## `apps/diplome/templates/diplome/participant_import_sheet.html`

Size: 1.8 KB

```html
{% extends "layouts/base.html" %}

{% block title %}Selectare foaie XLSX | Platforma TUVTK{% endblock %}

{% block content %}
<section class="mx-auto w-full max-w-2xl space-y-6">
    <div class="space-y-2">
        <div class="breadcrumbs p-0 text-sm text-muted"><ul><li>Diplome</li><li><a href="{% url 'diplome:list_index' %}">Liste participanți</a></li><li>Selectare foaie</li></ul></div>
        <div>
            <h1 class="text-2xl font-bold text-primary">Alege foaia de importat</h1>
            <p class="mt-1 text-sm text-muted">Fișierul {{ draft.source_file_name }} conține mai multe foi cu date. Va fi importată numai foaia selectată.</p>
        </div>
    </div>

    <form method="post" class="space-y-5 border border-base-300 bg-base-100 p-6">
        {% csrf_token %}
        <fieldset class="space-y-3">
            <legend class="text-sm font-semibold text-base-content">Foi disponibile</legend>
            {% for choice in form.sheet_index %}
                <label class="flex cursor-pointer items-center gap-3 border border-base-300 bg-base-100 p-4 transition-colors hover:bg-base-200/50">
                    {{ choice.tag }}
                    <span class="text-sm text-base-content">{{ choice.choice_label }}</span>
                </label>
            {% endfor %}
            {% for error in form.sheet_index.errors %}<p class="text-sm text-error" role="alert">{{ error }}</p>{% endfor %}
        </fieldset>
        <div class="flex justify-end gap-2 border-t border-base-300 pt-5">
            <a href="{% url 'diplome:participant_import' %}" class="btn btn-ghost btn-sm">Încarcă alt fișier</a>
            <button type="submit" class="btn btn-primary btn-sm">Continuă la asocierea coloanelor</button>
        </div>
    </form>
</section>
{% endblock %}
```

## `apps/diplome/templates/diplome/participant_list.html`

Size: 891 B

```html
{% extends "layouts/base.html" %}

{% block title %}Liste participanți | Platforma TUVTK{% endblock %}

{% block content %}
<section class="mx-auto w-full max-w-6xl space-y-6">
    <div class="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div class="space-y-2">
            <div class="breadcrumbs p-0 text-sm text-muted"><ul><li>Diplome</li><li>Liste participanți</li></ul></div>
            <div>
                <h1 class="text-2xl font-bold text-primary">Liste participanți</h1>
                <p class="mt-1 text-sm text-muted">Listele confirmate rămân disponibile până când alegi să le ștergi.</p>
            </div>
        </div>
        <a href="{% url 'diplome:participant_import' %}" class="btn btn-primary btn-sm">Importă o listă</a>
    </div>

    {% include "diplome/includes/participant_list_panel.html" %}
</section>
{% endblock %}
```

## `apps/diplome/templates/diplome/participant_list_detail.html`

Size: 1.4 KB

```html
{% extends "layouts/base.html" %}

{% block title %}{{ participant_list.name }} | Platforma TUVTK{% endblock %}

{% block content %}
<section class="mx-auto w-full max-w-7xl space-y-6">
    <div class="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div class="space-y-2">
            <div class="breadcrumbs p-0 text-sm text-muted"><ul><li>Diplome</li><li><a href="{% url 'diplome:list_index' %}">Liste participanți</a></li><li>{{ participant_list.name }}</li></ul></div>
            <div>
                <h1 class="text-2xl font-bold text-primary">{{ participant_list.name }}</h1>
                {% if participant_list.description %}<p class="mt-1 text-sm text-muted">{{ participant_list.description }}</p>{% endif %}
                <p class="mt-2 text-xs text-muted">{% if participant_list.course_name %}Curs: {{ participant_list.course_name }} · {% endif %}Fișier: {{ participant_list.source_file_name }} · {{ participant_list.participant_count }} participanți</p>
            </div>
        </div>
        <form method="post" action="{% url 'diplome:participant_list_delete' participant_list.pk %}">
            {% csrf_token %}
            <button type="submit" class="btn btn-outline btn-error btn-sm">Șterge lista</button>
        </form>
    </div>

    {% include "diplome/includes/participant_list_detail_panel.html" %}
</section>
{% endblock %}
```

## `apps/diplome/templates/diplome/placeholder.html`

Size: 687 B

```html
{% extends "layouts/base.html" %}

{% block title %}{{ page_title }} | Platforma TUVTK{% endblock %}

{% block content %}
<section class="mx-auto w-full max-w-4xl space-y-5">
    <div class="breadcrumbs p-0 text-sm text-muted"><ul><li>Diplome</li><li>{{ page_title }}</li></ul></div>
    <div class="border border-base-300 bg-base-100 px-6 py-12 text-center">
        <h1 class="text-2xl font-bold text-primary">{{ page_title }}</h1>
        <p class="mx-auto mt-3 max-w-2xl text-sm text-muted">{{ page_description }}</p>
        <a href="{% url 'diplome:template_list' %}" class="btn btn-outline btn-primary btn-sm mt-6">Deschide template-urile</a>
    </div>
</section>
{% endblock %}
```

## `apps/diplome/templates/diplome/template_editor.html`

Size: 24.2 KB

```html
{% extends "layouts/base.html" %}
{% load static %}

{% block title %}Editor {{ diploma_template.name }} | Platforma TUVTK{% endblock %}
{% block sidebar_start_collapsed %}true{% endblock %}

{% block page_styles %}
<link rel="stylesheet" href="{% static 'diplome/template_editor.css' %}">
{% endblock %}

{% block content %}
<section
    id="diploma-editor"
    class="diploma-editor"
    data-save-url="{% url 'diplome:template_editor' diploma_template.pk %}"
    data-preview-url="{% url 'diplome:template_preview' diploma_template.pk %}"
    data-template-list-url="{% url 'diplome:template_list' %}"
    data-is-draft-template="{{ is_draft_template|yesno:'true,false' }}"
    data-media-assets-api-url="{{ media_assets_api_url }}"
    data-media-assets-upload-url="{{ media_assets_upload_url }}"
>
    <header class="editor-heading">
        <div class="editor-heading-actions">
            <button type="button" class="btn btn-primary btn-sm" data-action="save">Salvează</button>
            <a href="{% url 'diplome:template_preview' diploma_template.pk %}" class="btn btn-outline btn-primary btn-sm" data-action="preview">Previzualizează</a>
            <button type="button" class="btn btn-outline btn-error btn-sm" data-action="close-editor">Închide</button>
        </div>
    </header>

    <form id="editor-save-form" class="hidden">{% csrf_token %}</form>
    <form id="editor-discard-form" method="post" action="{% url 'diplome:template_delete' diploma_template.pk %}" class="hidden">{% csrf_token %}</form>

    <dialog id="editor-confirm-dialog" class="modal" aria-labelledby="editor-confirm-title">
        <div class="modal-box max-w-md">
            <h2 id="editor-confirm-title" class="text-lg font-bold">Confirmă acțiunea</h2>
            <p id="editor-confirm-message" class="mt-3 text-sm text-base-content/75"></p>
            <div class="modal-action">
                <button type="button" id="editor-confirm-cancel" class="btn btn-ghost" data-confirm-cancel>Renunță</button>
                <button type="button" class="btn btn-error" data-confirm-accept>Șterge</button>
            </div>
        </div>
        <form method="dialog" class="modal-backdrop"><button data-confirm-cancel>Închide</button></form>
    </dialog>

    <div
        id="editor-media-picker"
        class="editor-media-picker"
        role="dialog"
        aria-modal="true"
        aria-labelledby="editor-media-picker-title"
        hidden
    >
        <button type="button" class="editor-media-picker-backdrop" data-action="close-media-picker" aria-label="Închide selectorul media" tabindex="-1"></button>
        <div class="editor-media-picker-panel">
            <header class="editor-media-picker-header">
                <div>
                    <h2 id="editor-media-picker-title">Alege un fișier media</h2>
                    <p id="editor-media-picker-description">Selectează un fișier din biblioteca ta.</p>
                </div>
                <button type="button" class="editor-media-picker-close" data-action="close-media-picker" aria-label="Închide">×</button>
            </header>
            <div class="editor-media-picker-body">
                <section class="editor-media-library" aria-label="Fișiere media disponibile">
                    <div class="editor-media-library-toolbar">
                        <strong>Biblioteca mea</strong>
                        <button type="button" class="editor-media-secondary-action" data-action="refresh-media-assets">Reîmprospătează</button>
                    </div>
                    <p id="editor-media-picker-feedback" class="editor-media-feedback" role="status" hidden></p>
                    <div id="editor-media-picker-grid" class="editor-media-picker-grid" role="listbox" aria-label="Fișiere media"></div>
                    <div id="editor-media-picker-empty" class="editor-media-picker-empty" hidden>
                        <strong>Biblioteca media este goală.</strong>
                        <span>Încarcă un fișier fără să părăsești editorul.</span>
                    </div>
                </section>
                <aside class="editor-media-upload" aria-label="Încarcă un fișier media">
                    <h3>Încarcă un fișier nou</h3>
                    <p>SVG, PNG, JPG sau WEBP.</p>
                    <form id="editor-media-upload-form" enctype="multipart/form-data">
                        {% csrf_token %}
                        <label class="editor-field">Nume în bibliotecă
                            <input type="text" name="name" maxlength="160" placeholder="Opțional">
                        </label>
                        <label class="editor-field">Fișier
                            <input type="file" name="file" required accept=".svg,.png,.jpg,.jpeg,.webp,image/svg+xml,image/png,image/jpeg,image/webp">
                        </label>
                        <p id="editor-media-upload-error" class="editor-media-upload-error" role="alert" hidden></p>
                        <button type="submit" class="btn btn-primary btn-sm w-full">Încarcă</button>
                    </form>
                </aside>
            </div>
            <footer class="editor-media-picker-footer">
                <span id="editor-media-picker-selection">Niciun fișier selectat</span>
                <div>
                    <button type="button" class="btn btn-ghost btn-sm" data-action="close-media-picker">Renunță</button>
                    <button type="button" class="btn btn-primary btn-sm" data-action="apply-media-asset" disabled>Folosește fișierul</button>
                </div>
            </footer>
        </div>
    </div>

    <div class="editor-toolbar" role="toolbar" aria-label="Instrumente editor">
        <button type="button" class="editor-tool" data-action="undo" title="Anulează ultima modificare" disabled>↶ <span>Undo</span></button>
        <button type="button" class="editor-tool" data-action="redo" title="Reface ultima modificare" disabled>↷ <span>Redo</span></button>
        <span class="editor-toolbar-divider"></span>
        <div class="editor-zoom-controls" role="group" aria-label="Zoom canvas">
            <button type="button" class="editor-tool editor-zoom-button" data-action="zoom-out" aria-label="Micșorează zoomul" title="Micșorează zoomul">−</button>
            <label class="editor-tool-field">Zoom
                <select data-action="zoom" aria-label="Nivel zoom" title="Poți folosi și Ctrl + rotița mouse-ului">
                    <option value="fit" selected>Încadrează pagina</option>
                    <option value="0.25">25%</option>
                    <option value="0.5">50%</option>
                    <option value="0.75">75%</option>
                    <option value="1">100%</option>
                    <option value="1.25">125%</option>
                    <option value="1.5">150%</option>
                    <option value="2">200%</option>
                    <option value="" data-zoom-custom hidden></option>
                </select>
            </label>
            <button type="button" class="editor-tool editor-zoom-button" data-action="zoom-in" aria-label="Mărește zoomul" title="Mărește zoomul">+</button>
            <button type="button" class="editor-tool" data-action="fit-page" title="Încadrează pagina în spațiul disponibil">Încadrează</button>
        </div>
        <button type="button" class="editor-tool is-active" data-action="toggle-grid" aria-pressed="true">▦ <span>Grid</span></button>
        <button type="button" class="editor-tool is-active" data-action="toggle-guides" aria-pressed="true">┼ <span>Ghidaje</span></button>
        <button type="button" class="editor-tool" data-action="fit-content" title="Potrivește caseta la conținut" disabled>↙↗ <span>Potrivește</span></button>
    </div>

    <div class="editor-workspace">
        <aside class="editor-panel editor-layers-panel" aria-label="Straturi">
            <div class="editor-panel-title"><h2>Straturi</h2><span aria-hidden="true">▤</span></div>
            <div id="editor-layers" class="editor-layers"></div>
            <div class="editor-align-actions" role="toolbar" aria-label="Aliniere selecție">
                <button type="button" data-align="left" title="Aliniază la stânga">⊢</button>
                <button type="button" data-align="center" title="Centrează orizontal">↔</button>
                <button type="button" data-align="right" title="Aliniază la dreapta">⊣</button>
                <button type="button" data-align="top" title="Aliniază sus">⊤</button>
                <button type="button" data-align="middle" title="Centrează vertical">↕</button>
                <button type="button" data-align="bottom" title="Aliniază jos">⊥</button>
                <button type="button" data-distribute="horizontal" title="Distribuie orizontal">⋯</button>
                <button type="button" data-distribute="vertical" title="Distribuie vertical">⋮</button>
            </div>
            <div class="editor-guide-controls">
                <div class="editor-guide-input-row">
                    <label>Poziție (mm)<input type="number" id="editor-guide-position" min="0" step="1" value="10"></label>
                    <button type="button" data-action="add-guide-x" title="Adaugă ghid vertical">+ V</button>
                    <button type="button" data-action="add-guide-y" title="Adaugă ghid orizontal">+ O</button>
                </div>
                <small>Elementele se fixează automat pe ghidaje când sunt mutate.</small>
                <div id="editor-custom-guides" class="editor-custom-guides"></div>
            </div>
            <div class="editor-layer-actions">
                <button type="button" data-action="layer-up">↑ Mută în sus</button>
                <button type="button" data-action="layer-down">↓ Mută în jos</button>
            </div>
        </aside>

        <main class="editor-canvas-viewport" id="editor-canvas-viewport">
            <div class="editor-canvas-shell" id="editor-canvas-shell">
                <div class="editor-ruler-corner"></div>
                <div class="editor-ruler editor-ruler-top" id="editor-ruler-top"></div>
                <div class="editor-ruler editor-ruler-left" id="editor-ruler-left"></div>
                <div class="editor-stage" id="editor-stage">
                    <div class="diploma-canvas has-grid" id="diploma-canvas" tabindex="0" aria-label="Canvas template diplomă">
                        <div class="editor-guide editor-guide-x" hidden></div>
                        <div class="editor-guide editor-guide-y" hidden></div>
                    </div>
                </div>
            </div>
        </main>

        <aside class="editor-panel editor-inspector-panel" aria-label="Inspector template">
            <div class="editor-inspector-tabs" role="tablist" aria-label="Panouri inspector">
                <button type="button" id="editor-tab-elements" class="editor-inspector-tab is-active" role="tab" aria-selected="true" aria-controls="editor-panel-elements" data-inspector-tab="elements">Elemente</button>
                <button type="button" id="editor-tab-properties" class="editor-inspector-tab" role="tab" aria-selected="false" aria-controls="editor-panel-properties" data-inspector-tab="properties" tabindex="-1">Proprietăți</button>
            </div>

            <div id="editor-panel-elements" class="editor-inspector-pane editor-inspector-pane-elements" role="tabpanel" aria-labelledby="editor-tab-elements" data-inspector-panel="elements">
                <div class="editor-panel-title"><h2>Adaugă element</h2><span aria-hidden="true">＋</span></div>
                <div class="editor-element-library">
                    <div class="editor-element-actions">
                        <button type="button" class="editor-element-action" data-action="add-text"><span class="editor-element-icon" aria-hidden="true">A</span><span><strong>Text</strong><small>Bloc de text liber</small></span></button>
                        <button type="button" class="editor-element-action" data-action="add-list"><span class="editor-element-icon" aria-hidden="true">•</span><span><strong>Listă</strong><small>Listă cu marcatori</small></span></button>
                        <button type="button" class="editor-element-action" data-action="add-image"><span class="editor-element-icon" aria-hidden="true">▧</span><span><strong>Imagine</strong><small>Fișier din bibliotecă</small></span></button>
                        <button type="button" class="editor-element-action" data-action="add-background"><span class="editor-element-icon" aria-hidden="true">▣</span><span><strong>Fundal</strong><small>Imagine pe întreaga pagină</small></span></button>
                        <button type="button" class="editor-element-action" data-action="add-icon"><span class="editor-element-icon" aria-hidden="true">☆</span><span><strong>Icon</strong><small>Simbol sau grafică</small></span></button>
                        <button type="button" class="editor-element-action" data-action="add-table"><span class="editor-element-icon" aria-hidden="true">▦</span><span><strong>Tabel</strong><small>Rânduri și coloane</small></span></button>
                    </div>
                    <section class="editor-variable-library" aria-labelledby="editor-variable-library-title">
                        <h3 id="editor-variable-library-title">Variabile participant</h3>
                        <div>
                            <button type="button" data-add-variable="full_name">Nume complet</button>
                            <button type="button" data-add-variable="date_of_birth">Data nașterii</button>
                            <button type="button" data-add-variable="place_of_birth">Locul nașterii</button>
                            <button type="button" data-add-variable="certificate_number">Număr certificat</button>
                        </div>
                    </section>
                </div>
            </div>

            <div id="editor-panel-properties" class="editor-inspector-pane editor-inspector-pane-properties" role="tabpanel" aria-labelledby="editor-tab-properties" data-inspector-panel="properties" hidden>
                <div class="editor-panel-title"><h2>Element selectat</h2><span id="property-lock-indicator" aria-hidden="true">○</span></div>
                <div id="editor-empty-properties" class="editor-empty-properties">Selectează un element pentru a-i edita proprietățile.</div>
                <div id="editor-multi-properties" class="editor-empty-properties" hidden>
                    <strong data-multi-count>0 elemente selectate</strong>
                    <span>Folosește instrumentele de aliniere din panoul Straturi sau trage selecția pentru a muta elementele deblocate împreună.</span>
                </div>
                <div id="editor-properties" class="editor-properties" hidden>
                <section>
                    <h3>Poziție și dimensiune</h3>
                    <div class="editor-field-grid">
                        <label>X (mm)<input type="number" data-prop="x_mm" step="1"></label>
                        <label>Y (mm)<input type="number" data-prop="y_mm" step="1"></label>
                        <label>Lățime (mm)<input type="number" data-prop="width_mm" min="1" step="1"></label>
                        <label>Înălțime (mm)<input type="number" data-prop="height_mm" min="1" step="1"></label>
                        <label>Rotire<input type="number" data-prop="rotation" min="-180" max="180"></label>
                        <label>Ordine strat<input type="number" data-prop="zIndex" min="0" max="1000"></label>
                    </div>
                </section>
                <section data-section="typography">
                    <h3>Tipografie</h3>
                    <label class="editor-field">Familie font
                        <select data-style="fontFamily">
                            <option>Lora</option><option>Inter</option><option>Georgia</option><option>Arial</option><option>Times New Roman</option>
                        </select>
                    </label>
                    <div class="editor-field-grid">
                        <label>Dimensiune<input type="number" data-style="fontSize" min="8" max="200"></label>
                        <label>Culoare<input type="color" data-style="color"></label>
                    </div>
                    <div class="editor-toggle-row">
                        <button type="button" data-style-toggle="bold" aria-pressed="false"><strong>B</strong></button>
                        <button type="button" data-style-toggle="italic" aria-pressed="false"><em>I</em></button>
                        <button type="button" data-style-toggle="underline" aria-pressed="false"><u>U</u></button>
                    </div>
                    <label class="editor-field">Aliniere
                        <select data-style="align"><option value="left">Stânga</option><option value="center">Centru</option><option value="right">Dreapta</option></select>
                    </label>
                    <div class="editor-field-grid">
                        <label>Înălțime rând<input type="number" data-style="lineHeight" min="0.8" max="3" step="0.01"></label>
                        <label>Spațiere litere (px)<input type="number" data-style="letterSpacing" min="-5" max="20" step="0.1"></label>
                    </div>
                    <label class="editor-field">Transformare text
                        <select data-style="textTransform"><option value="none">Niciuna</option><option value="uppercase">MAJUSCULE</option><option value="lowercase">minuscule</option></select>
                    </label>
                </section>
                <section data-section="list" hidden>
                    <h3>Listă</h3>
                    <label class="editor-field">Elemente (unul pe rând)<textarea data-list-items rows="6" maxlength="4019"></textarea></label>
                    <div class="editor-field-grid">
                        <label>Tip
                            <select data-style="listType"><option value="bullet">Marcatori</option><option value="number">Numerotată</option></select>
                        </label>
                        <label>Indentare (mm)<input type="number" data-style="indent_mm" min="0" max="50" step="1"></label>
                    </div>
                </section>
                <section data-section="media" hidden>
                    <h3>Fișier media</h3>
                    <div id="editor-media-current-preview" class="editor-media-current-preview"></div>
                    <label class="editor-field">Fișier din bibliotecă
                        <select data-prop="assetId"></select>
                    </label>
                    <div class="editor-media-property-actions">
                        <button type="button" data-action="open-media-picker">Alege sau înlocuiește</button>
                        <button type="button" class="is-danger" data-action="remove-media-element">Elimină din template</button>
                    </div>
                    <div class="editor-field-grid">
                        <label>Încadrare
                            <select data-style="fit"><option value="contain">Conține</option><option value="cover">Acoperă</option><option value="stretch">Întinde</option></select>
                        </label>
                        <label>Opacitate<input type="number" data-style="opacity" min="0" max="1" step="0.05"></label>
                    </div>
                    <label class="editor-field">Text alternativ<input type="text" data-prop="alt" maxlength="160"></label>
                    <a href="{% url 'media_library:index' %}" class="mt-2 inline-flex text-xs font-semibold text-primary hover:underline">Deschide biblioteca media</a>
                </section>
                <section data-section="icon" hidden>
                    <h3>Icon</h3>
                    <div id="editor-icon-current-preview" class="editor-media-current-preview"></div>
                    <label class="editor-field">Icon inclus
                        <select data-prop="iconName">
                            <option value="award">Medalie</option>
                            <option value="patch-check">Validare</option>
                            <option value="star">Stea</option>
                        </select>
                    </label>
                    <div class="editor-field-grid">
                        <label>Culoare<input type="color" data-icon-style="color"></label>
                        <label>Opacitate<input type="number" data-icon-style="opacity" min="0" max="1" step="0.05"></label>
                    </div>
                    <div class="editor-media-property-actions">
                        <button type="button" data-action="open-icon-media-picker">Alege sau încarcă grafică</button>
                        <button type="button" class="is-danger" data-action="remove-icon-asset">Revino la iconul inclus</button>
                    </div>
                </section>
                <section data-section="table" hidden>
                    <h3>Tabel</h3>
                    <label class="editor-field">Coloane (una pe rând)<textarea data-table-columns rows="4" maxlength="967"></textarea></label>
                    <label class="editor-field">Rânduri (celule separate prin |)<textarea data-table-rows rows="6" maxlength="25619"></textarea></label>
                    <div class="editor-field-grid">
                        <label>Font
                            <select data-table-style="fontFamily"><option>Inter</option><option>Lora</option><option>Georgia</option><option>Arial</option><option>Times New Roman</option></select>
                        </label>
                        <label>Dimensiune<input type="number" data-table-style="fontSize" min="8" max="72"></label>
                        <label>Culoare text<input type="color" data-table-style="color"></label>
                        <label>Culoare bordură<input type="color" data-table-style="borderColor"></label>
                        <label>Fundal antet<input type="color" data-table-style="headerBackground"></label>
                        <label>Aliniere
                            <select data-table-style="align"><option value="left">Stânga</option><option value="center">Centru</option><option value="right">Dreapta</option></select>
                        </label>
                    </div>
                    <label class="editor-checkbox-field"><input type="checkbox" data-table-style="bold"> Text îngroșat</label>
                </section>
                <section>
                    <h3>Conținut</h3>
                    <label class="editor-field">Etichetă<input type="text" data-prop="label" maxlength="120"></label>
                    <label class="editor-field" data-content-field="text">Text<textarea data-prop="text" rows="3" maxlength="500"></textarea></label>
                    <label class="editor-field" data-content-field="placeholder">Placeholder<input type="text" data-prop="placeholder" maxlength="500"></label>
                    <label class="editor-field" data-content-field="variable">Variabilă
                        <select data-prop="variable">
                            <option value="full_name">Nume complet</option>
                            <option value="date_of_birth">Data nașterii</option>
                            <option value="place_of_birth">Locul nașterii</option>
                            <option value="certificate_number">Număr certificat</option>
                        </select>
                    </label>
                </section>
                </div>
            </div>
        </aside>
    </div>

    <footer class="editor-statusbar">
        <span>▦ Grid <strong data-status="grid">1 mm / 10 mm</strong></span>
        <span>Zoom <strong data-status="zoom">75%</strong></span>
        <span>▤ <strong data-status="page">A4 landscape</strong></span>
        <span class="editor-save-status" data-status="save"><i></i><strong>Modificări salvate</strong></span>
    </footer>

    {{ layout|json_script:"diploma-layout-data" }}
    {{ media_assets|json_script:"diploma-media-assets-data" }}
</section>
{% endblock %}

{% block page_scripts %}
<script src="{% static 'diplome/template_renderer.js' %}" defer></script>
<script src="{% static 'diplome/template_editor.js' %}" defer></script>
{% endblock %}
```

## `apps/diplome/templates/diplome/template_form.html`

Size: 2.6 KB

```html
{% extends "layouts/base.html" %}

{% block title %}Template nou | Platforma TUVTK{% endblock %}

{% block content %}
<section class="w-full max-w-2xl space-y-6">
    <div class="space-y-2">
        <div class="breadcrumbs p-0 text-sm text-muted">
            <ul><li>Diplome</li><li><a href="{% url 'diplome:template_list' %}">Template-uri</a></li><li>Template nou</li></ul>
        </div>
        <div>
            <h1 class="text-2xl font-bold text-primary">Creează un template</h1>
            <p class="mt-1 text-sm text-muted">Configurează documentul de bază. Elementele vizuale se editează în pasul următor.</p>
        </div>
    </div>

    <form method="post" class="space-y-5 border border-base-300 bg-base-100 p-6">
        {% csrf_token %}
        {% if form.non_field_errors %}<div class="alert alert-error py-2 text-sm">{{ form.non_field_errors }}</div>{% endif %}
        <label class="form-control w-full">
            <span class="label-text mb-1 text-sm font-semibold">Nume</span>
            {{ form.name }}
            {% for error in form.name.errors %}<span class="mt-1 text-xs text-error">{{ error }}</span>{% endfor %}
        </label>
        <label class="form-control w-full">
            <span class="label-text mb-1 text-sm font-semibold">Categorie</span>
            {{ form.category }}
            <span class="mt-1 text-xs text-muted">Folosită pentru organizarea și filtrarea template-urilor.</span>
            {% for error in form.category.errors %}<span class="mt-1 text-xs text-error">{{ error }}</span>{% endfor %}
        </label>
        <label class="form-control w-full">
            <span class="label-text mb-1 text-sm font-semibold">Descriere</span>
            {{ form.description }}
            {% for error in form.description.errors %}<span class="mt-1 text-xs text-error">{{ error }}</span>{% endfor %}
        </label>
        <div class="grid gap-4 sm:grid-cols-2">
            <label class="form-control w-full">
                <span class="label-text mb-1 text-sm font-semibold">Format pagină</span>
                {{ form.page_size }}
            </label>
            <label class="form-control w-full">
                <span class="label-text mb-1 text-sm font-semibold">Orientare</span>
                {{ form.orientation }}
            </label>
        </div>
        <div class="flex justify-end gap-2 border-t border-base-300 pt-5">
            <a href="{% url 'diplome:template_list' %}" class="btn btn-ghost btn-sm">Renunță</a>
            <button type="submit" class="btn btn-primary btn-sm">Creează și deschide editorul</button>
        </div>
    </form>
</section>
{% endblock %}
```

## `apps/diplome/templates/diplome/template_list.html`

Size: 902 B

```html
{% extends "layouts/base.html" %}

{% block title %}Template-uri diplome | Platforma TUVTK{% endblock %}

{% block content %}
<section class="mx-auto w-full max-w-6xl space-y-6">
    <div class="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div class="space-y-2">
            <div class="breadcrumbs p-0 text-sm text-muted">
                <ul><li>Diplome</li><li>Template-uri</li></ul>
            </div>
            <div>
                <h1 class="text-2xl font-bold text-primary">Template-uri diplome</h1>
                <p class="mt-1 text-sm text-muted">Creează și administrează machetele vizuale folosite pentru diplome.</p>
            </div>
        </div>
        <a href="{% url 'diplome:template_create' %}" class="btn btn-primary btn-sm">Template nou</a>
    </div>

    {% include "diplome/includes/template_list_panel.html" %}
</section>
{% endblock %}
```

## `apps/diplome/templates/diplome/template_preview.html`

Size: 1.5 KB

```html
{% extends "layouts/base.html" %}
{% load static %}

{% block title %}Preview {{ diploma_template.name }} | Platforma TUVTK{% endblock %}
{% block sidebar_start_collapsed %}true{% endblock %}

{% block page_styles %}
<link rel="stylesheet" href="{% static 'diplome/template_editor.css' %}">
{% endblock %}

{% block content %}
<section id="diploma-preview" class="diploma-preview-page">
    <header class="preview-heading">
        <div>
            <div class="breadcrumbs p-0 text-xs text-muted">
                <ul><li>Diplome</li><li><a href="{% url 'diplome:template_list' %}">Template-uri</a></li><li>Preview</li></ul>
            </div>
            <h1>Previzualizare diplomă</h1>
            <p>{{ diploma_template.name }} · date demonstrative</p>
        </div>
        <a href="{% url 'diplome:template_editor' diploma_template.pk %}" class="btn btn-outline btn-primary btn-sm">Înapoi la editor</a>
    </header>
    <div class="preview-workspace">
        <div class="preview-canvas-frame" id="preview-canvas-frame">
            <div class="diploma-canvas preview-canvas" id="preview-canvas" aria-label="Previzualizare template diplomă"></div>
        </div>
    </div>
    {{ layout|json_script:"diploma-layout-data" }}
    {{ sample_participant|json_script:"diploma-sample-data" }}
    {{ media_assets|json_script:"diploma-media-assets-data" }}
</section>
{% endblock %}

{% block page_scripts %}
<script src="{% static 'diplome/template_renderer.js' %}" defer></script>
<script src="{% static 'diplome/template_preview.js' %}" defer></script>
{% endblock %}
```

## `apps/diplome/tests.py`

Size: 31.7 KB

Redacted secret-like assignments: 2

```python
import json
from copy import deepcopy

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from apps.media_library.models import MediaAsset

from .forms import DiplomaTemplateCreateForm
from .models import DiplomaGenerationBatch, DiplomaTemplate, ParticipantList
from .pdf_renderer import _fitted_box
from .services import build_default_layout, create_diploma_template
from .validators import MAX_LAYOUT_JSON_BYTES, validate_layout_json
from .views import DRAFT_TEMPLATE_IDS_SESSION_KEY


class DiplomaTemplateViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="diploma-owner",
            password=<redacted>
            first_name="Ana",
            last_name="Operator",
        )
        cls.other_user = get_user_model().objects.create_user(
            username="other-owner",
            password=<redacted>
        )

    def setUp(self):
        self.client.force_login(self.user)

    def create_template(
        self,
        *,
        owner=None,
        name="Diplomă absolvire",
        category="General",
        with_sample_layout=False,
    ):
        template = create_diploma_template(
            owner=owner or self.user,
            data={
                "name": name,
                "category": category,
                "description": "Template pentru cursuri",
                "page_size": "A4",
                "orientation": "landscape",
            },
        )
        if with_sample_layout:
            template.layout_json = build_default_layout()
            template.full_clean()
            template.save(update_fields=("layout_json", "updated_at"))
        return template

    def create_media_asset(self, *, owner=None, name="Logo"):
        asset = MediaAsset(
            owner=owner or self.user,
            name=name,
            original_filename="logo.png",
            kind=MediaAsset.Kind.RASTER,
            extension=".png",
            mime_type="image/png",
            size_bytes=128,
            width_px=32,
            height_px=20,
            sha256="a" * 64,
        )
        asset.file.name = f"media_library/tests/{asset.pk}.png"
        asset.save()
        return asset

    def append_media_element(self, layout, asset, *, element_id="logo"):
        layout["elements"].append({
            "id": element_id,
            "type": "image",
            "label": "Logo",
            "x_mm": 10,
            "y_mm": 10,
            "width_mm": 30,
            "height_mm": 20,
            "rotation": 0,
            "zIndex": 100,
            "locked": False,
            "visible": True,
            "style": {"fit": "contain", "opacity": 1},
            "assetId": str(asset.pk),
            "alt": asset.name,
        })

    def test_all_diploma_pages_require_login(self):
        template = self.create_template()
        routes = (
            reverse("diplome:list_index"),
            reverse("diplome:template_list"),
            reverse("diplome:template_create"),
            reverse("diplome:template_editor", kwargs={"template_id": template.pk}),
            reverse("diplome:template_preview", kwargs={"template_id": template.pk}),
            reverse("diplome:generation_index"),
            reverse("diplome:history_index"),
        )
        self.client.logout()
        for url in routes:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response.url.startswith(reverse("login")))

    def test_user_can_create_template_with_blank_layout(self):
        response = self.client.post(
            reverse("diplome:template_create"),
            {
                "name": "Diplomă Inspector SSM",
                "category": "  SSM   avansat  ",
                "description": "Model A4 pentru absolvire",
                "page_size": "A4",
                "orientation": "landscape",
            },
        )

        template = DiplomaTemplate.objects.get()
        self.assertRedirects(
            response,
            reverse("diplome:template_editor", kwargs={"template_id": template.pk}),
        )
        self.assertEqual(template.owner, self.user)
        self.assertEqual(template.category, "SSM avansat")
        self.assertEqual(template.page_width_mm, 297)
        self.assertEqual(template.page_height_mm, 210)
        self.assertEqual(template.grid_size_mm, 1)
        self.assertEqual(template.major_grid_size_mm, 10)
        self.assertEqual(template.layout_json["version"], 2)
        self.assertEqual(template.layout_json["page"]["width_mm"], 297)
        self.assertEqual(template.layout_json["page"]["height_mm"], 210)
        self.assertEqual(template.layout_json["page"]["grid_mm"], 1)
        self.assertEqual(template.layout_json["guides"], {"vertical": [], "horizontal": []})
        self.assertEqual(template.layout_json["elements"], [])
        self.assertIn(
            str(template.pk),
            self.client.session[DRAFT_TEMPLATE_IDS_SESSION_KEY],
        )

    def test_nonempty_save_finalizes_new_template_draft(self):
        self.client.post(
            reverse("diplome:template_create"),
            {
                "name": "Template finalizat",
                "category": "General",
                "description": "",
                "page_size": "A4",
                "orientation": "landscape",
            },
        )
        template = DiplomaTemplate.objects.get()
        layout = build_default_layout()

        response = self.client.post(
            reverse("diplome:template_editor", kwargs={"template_id": template.pk}),
            {"layout_json": json.dumps(layout)},
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["isDraft"])
        self.assertNotIn(
            str(template.pk),
            self.client.session.get(DRAFT_TEMPLATE_IDS_SESSION_KEY, []),
        )
    def test_empty_save_keeps_new_template_as_draft(self):
        self.client.post(
            reverse("diplome:template_create"),
            {
                "name": "Template încă gol",
                "category": "General",
                "description": "",
                "page_size": "A4",
                "orientation": "landscape",
            },
        )
        template = DiplomaTemplate.objects.get()

        response = self.client.post(
            reverse("diplome:template_editor", kwargs={"template_id": template.pk}),
            {"layout_json": json.dumps(template.layout_json)},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["isDraft"])
        self.assertIn(
            str(template.pk),
            self.client.session[DRAFT_TEMPLATE_IDS_SESSION_KEY],
        )

    def test_ajax_discard_deletes_new_template_draft(self):
        self.client.post(
            reverse("diplome:template_create"),
            {
                "name": "Template abandonat",
                "category": "General",
                "description": "",
                "page_size": "A4",
                "orientation": "landscape",
            },
        )
        template = DiplomaTemplate.objects.get()

        response = self.client.post(
            reverse("diplome:template_delete", kwargs={"template_id": template.pk}),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
            HTTP_ACCEPT="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        self.assertFalse(DiplomaTemplate.objects.filter(pk=template.pk).exists())
        self.assertNotIn(
            str(template.pk),
            self.client.session.get(DRAFT_TEMPLATE_IDS_SESSION_KEY, []),
        )
        list_response = self.client.get(reverse("diplome:template_list"))
        self.assertNotContains(list_response, "Template-ul a fost creat.")

    def test_create_form_does_not_validate_an_incomplete_model_instance(self):
        form = DiplomaTemplateCreateForm(data={
            "name": "Diplomă Inspector SSM",
            "category": "SSM",
            "description": "Model cu diacritice pentru Brașov",
            "page_size": "A4",
            "orientation": "landscape",
        })

        self.assertTrue(form.is_valid(), form.errors)
        self.assertNotIn("layout_json", form.errors)

    def test_template_list_only_contains_owned_templates(self):
        own = self.create_template(name="Template propriu")
        other = self.create_template(owner=self.other_user, name="Template străin")

        response = self.client.get(reverse("diplome:template_list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "diplome/template_list.html")
        self.assertContains(response, own.name)
        self.assertNotContains(response, other.name)

    def test_template_list_filters_by_owned_category(self):
        ssm = self.create_template(name="Template SSM", category="SSM")
        psi = self.create_template(name="Template PSI", category="PSI")
        other = self.create_template(
            owner=self.other_user,
            name="Template străin",
            category="Categorie privată",
        )

        response = self.client.get(reverse("diplome:template_list"), {"category": "SSM"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, ssm.name)
        self.assertNotContains(response, psi.name)
        self.assertNotContains(response, other.name)
        self.assertContains(response, "SSM")
        self.assertNotContains(response, "Categorie privată")

    def test_template_list_htmx_returns_partial_panel(self):
        ssm = self.create_template(name="Template SSM", category="SSM")
        psi = self.create_template(name="Template PSI", category="PSI")

        response = self.client.get(
            reverse("diplome:template_list"),
            {"category": "SSM"},
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "diplome/includes/template_list_panel.html")
        self.assertContains(response, 'id="template-list-panel"')
        self.assertContains(response, ssm.name)
        self.assertNotContains(response, psi.name)
        self.assertNotContains(response, "<title>")

    def test_template_delete_htmx_refreshes_list_panel(self):
        template = self.create_template(name="Template de șters")
        keep = self.create_template(name="Template păstrat")

        response = self.client.post(
            reverse("diplome:template_delete", kwargs={"template_id": template.pk}),
            HTTP_HX_REQUEST="true",
            HTTP_HX_TARGET="template-list-panel",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "diplome/includes/template_list_panel.html")
        self.assertFalse(DiplomaTemplate.objects.filter(pk=template.pk).exists())
        self.assertContains(response, "Template-ul a fost șters.")
        self.assertContains(response, keep.name)
        self.assertNotContains(response, template.name)

    def test_user_can_open_own_editor_and_navigation_is_active(self):
        template = self.create_template()

        response = self.client.get(
            reverse("diplome:template_editor", kwargs={"template_id": template.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "diplome/template_editor.html")
        self.assertContains(
            response,
            f"<title>Editor {template.name} | Platforma TUVTK</title>",
            html=True,
        )
        self.assertContains(response, "diplome/template_editor.js")
        self.assertContains(response, 'data-sidebar-start-collapsed="true"')
        self.assertContains(response, 'aria-current="page"')
        self.assertContains(response, reverse("diplome:list_index"))
        self.assertContains(response, reverse("diplome:generation_index"))
        self.assertContains(response, reverse("diplome:history_index"))
        self.assertContains(response, 'data-action="undo"')
        self.assertContains(response, 'data-action="redo"')
        self.assertContains(response, 'id="editor-guide-position"')
        self.assertContains(response, 'id="editor-confirm-dialog"')
        self.assertContains(response, 'data-table-columns')
        self.assertContains(response, 'data-action="open-icon-media-picker"')

    def test_editor_page_includes_media_api_urls(self):
        template = self.create_template()

        response = self.client.get(
            reverse("diplome:template_editor", kwargs={"template_id": template.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'data-media-assets-api-url="{reverse("media_library:api_assets")}"')
        self.assertContains(response, f'data-media-assets-upload-url="{reverse("media_library:api_upload")}"')

    def test_editor_includes_owned_media_assets(self):
        template = self.create_template()
        asset = self.create_media_asset(name="Logo propriu")

        response = self.client.get(
            reverse("diplome:template_editor", kwargs={"template_id": template.pk})
        )

        self.assertContains(response, str(asset.pk))
        self.assertContains(response, "Logo propriu")

    def test_editor_does_not_include_foreign_media_assets(self):
        template = self.create_template()
        foreign_asset = self.create_media_asset(owner=self.other_user, name="Logo străin")

        response = self.client.get(
            reverse("diplome:template_editor", kwargs={"template_id": template.pk})
        )

        self.assertNotContains(response, str(foreign_asset.pk))
        self.assertNotContains(response, "Logo străin")

    def test_cross_owner_template_routes_return_404(self):
        template = self.create_template(owner=self.other_user)
        editor_url = reverse("diplome:template_editor", kwargs={"template_id": template.pk})
        routes = (
            ("get", editor_url, None),
            ("get", reverse("diplome:template_preview", kwargs={"template_id": template.pk}), None),
            ("post", editor_url, {"layout_json": json.dumps(build_default_layout())}),
            ("post", reverse("diplome:template_delete", kwargs={"template_id": template.pk}), {}),
        )
        for method, url, data in routes:
            with self.subTest(method=method, url=url):
                response = getattr(self.client, method)(url, data or {})
                self.assertEqual(response.status_code, 404)

    def test_valid_layout_json_saves(self):
        template = self.create_template(with_sample_layout=True)
        layout = deepcopy(template.layout_json)
        full_name = next(item for item in layout["elements"] if item["id"] == "full_name")
        full_name["x_mm"] = 72
        full_name["style"]["color"] = "#d41131"

        response = self.client.post(
            reverse("diplome:template_editor", kwargs={"template_id": template.pk}),
            {"layout_json": json.dumps(layout)},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        template.refresh_from_db()
        saved = next(item for item in template.layout_json["elements"] if item["id"] == "full_name")
        self.assertEqual(saved["x_mm"], 72)
        self.assertEqual(saved["style"]["color"], "#d41131")

    def test_editor_saves_custom_guides(self):
        template = self.create_template()
        layout = deepcopy(template.layout_json)
        layout["guides"] = {"vertical": [10, 148], "horizontal": [25, 105]}

        response = self.client.post(
            reverse("diplome:template_editor", kwargs={"template_id": template.pk}),
            {"layout_json": json.dumps(layout)},
        )

        self.assertEqual(response.status_code, 200)
        template.refresh_from_db()
        self.assertEqual(
            template.layout_json["guides"],
            {"vertical": [10, 148], "horizontal": [25, 105]},
        )

    def test_legacy_layout_without_guides_is_normalized(self):
        layout = build_default_layout()
        layout.pop("guides")

        normalized = validate_layout_json(layout)

        self.assertEqual(normalized["guides"], {"vertical": [], "horizontal": []})

    def test_guides_are_sorted_deduplicated_and_page_bounded(self):
        layout = build_default_layout()
        layout["guides"] = {"vertical": [148, 10, 10], "horizontal": [105, 25]}

        normalized = validate_layout_json(layout)

        self.assertEqual(normalized["guides"]["vertical"], [10, 148])
        invalid = deepcopy(layout)
        invalid["guides"]["vertical"] = [298]
        with self.assertRaises(ValidationError):
            validate_layout_json(invalid)

    def test_legacy_typography_is_normalized_with_defaults(self):
        layout = build_default_layout()
        element = next(item for item in layout["elements"] if item["type"] == "text")
        for key in ("lineHeight", "letterSpacing", "textTransform"):
            element["style"].pop(key)

        normalized = validate_layout_json(layout)
        style = next(item for item in normalized["elements"] if item["id"] == element["id"])["style"]

        self.assertEqual(style["lineHeight"], 1.18)
        self.assertEqual(style["letterSpacing"], 0)
        self.assertEqual(style["textTransform"], "none")

    def test_typography_values_are_normalized_and_validated(self):
        layout = build_default_layout()
        element = next(item for item in layout["elements"] if item["type"] == "variable")
        element["style"].update({
            "lineHeight": 1.5,
            "letterSpacing": 2,
            "textTransform": "uppercase",
        })
        normalized = validate_layout_json(layout)
        style = next(item for item in normalized["elements"] if item["id"] == element["id"])["style"]
        self.assertEqual(style["lineHeight"], 1.5)
        self.assertEqual(style["letterSpacing"], 2.0)
        self.assertEqual(style["textTransform"], "uppercase")

        invalid_values = {
            "lineHeight": 3.1,
            "letterSpacing": 21,
            "textTransform": "capitalize",
        }
        for key, value in invalid_values.items():
            with self.subTest(key=key):
                invalid = deepcopy(layout)
                next(item for item in invalid["elements"] if item["id"] == element["id"])["style"][key] = value
                with self.assertRaises(ValidationError):
                    validate_layout_json(invalid)

    def test_list_element_validates_and_rejects_unsafe_items(self):
        layout = build_default_layout()
        list_element = {
            "id": "requirements",
            "type": "list",
            "label": "Cerințe",
            "x_mm": 20,
            "y_mm": 80,
            "width_mm": 120,
            "height_mm": 40,
            "rotation": 0,
            "zIndex": 100,
            "locked": False,
            "visible": True,
            "style": {
                "fontFamily": "Inter",
                "fontSize": 14,
                "bold": False,
                "italic": False,
                "underline": False,
                "color": "#111827",
                "align": "left",
                "lineHeight": 1.2,
                "letterSpacing": 0,
                "textTransform": "none",
                "listType": "bullet",
                "indent_mm": 5,
            },
            "items": ["Primul punct", "Al doilea punct"],
        }
        layout["elements"].append(list_element)

        normalized = validate_layout_json(layout)
        self.assertEqual(normalized["elements"][-1]["items"], list_element["items"])

        too_many = deepcopy(layout)
        too_many["elements"][-1]["items"] = [f"Punct {index}" for index in range(21)]
        with self.assertRaises(ValidationError):
            validate_layout_json(too_many)
        for unsafe in ("<b>HTML</b>", "javascript:alert(1)", "https://example.com"):
            with self.subTest(unsafe=unsafe):
                invalid = deepcopy(layout)
                invalid["elements"][-1]["items"] = [unsafe]
                with self.assertRaises(ValidationError):
                    validate_layout_json(invalid)

    def test_editor_saves_typography_and_list_elements(self):
        template = self.create_template(with_sample_layout=True)
        layout = deepcopy(template.layout_json)
        layout["elements"][0]["style"].update({
            "lineHeight": 1.4,
            "letterSpacing": 1.5,
            "textTransform": "lowercase",
        })
        list_style = {
            **layout["elements"][0]["style"],
            "listType": "number",
            "indent_mm": 5,
        }
        layout["elements"].append({
            "id": "agenda", "type": "list", "label": "Agendă",
            "x_mm": 10, "y_mm": 10, "width_mm": 80, "height_mm": 40,
            "rotation": 0, "zIndex": 101, "locked": False, "visible": True,
            "style": list_style, "items": ["Introducere", "Evaluare"],
        })

        response = self.client.post(
            reverse("diplome:template_editor", kwargs={"template_id": template.pk}),
            {"layout_json": json.dumps(layout)},
        )

        self.assertEqual(response.status_code, 200)
        template.refresh_from_db()
        self.assertEqual(template.layout_json["elements"][-1]["type"], "list")

    def test_editor_rejects_invalid_typography_with_400(self):
        template = self.create_template(with_sample_layout=True)
        layout = deepcopy(template.layout_json)
        layout["elements"][0]["style"]["lineHeight"] = 0.5

        response = self.client.post(
            reverse("diplome:template_editor", kwargs={"template_id": template.pk}),
            {"layout_json": json.dumps(layout)},
        )

        self.assertEqual(response.status_code, 400)

    def test_background_stretch_is_valid(self):
        asset = self.create_media_asset()
        layout = build_default_layout()
        layout["elements"].append({
            "id": "background", "type": "background", "label": "Fundal",
            "x_mm": 0, "y_mm": 0, "width_mm": 297, "height_mm": 210,
            "rotation": 0, "zIndex": 0, "locked": True, "visible": True,
            "style": {"fit": "stretch", "opacity": 1},
            "assetId": str(asset.pk), "alt": "",
        })

        self.assertEqual(validate_layout_json(layout)["elements"][-1]["style"]["fit"], "stretch")
        self.assertEqual(
            _fitted_box(
                source_width=100,
                source_height=50,
                x=0,
                y=0,
                width=297,
                height=210,
                fit="stretch",
            ),
            (0, 0, 297, 210),
        )

    def test_layout_with_owned_asset_id_saves(self):
        template = self.create_template()
        asset = self.create_media_asset()
        layout = deepcopy(template.layout_json)
        self.append_media_element(layout, asset)

        response = self.client.post(
            reverse("diplome:template_editor", kwargs={"template_id": template.pk}),
            {"layout_json": json.dumps(layout)},
        )

        self.assertEqual(response.status_code, 200)
        template.refresh_from_db()
        saved = next(element for element in template.layout_json["elements"] if element["id"] == "logo")
        self.assertEqual(saved["assetId"], str(asset.pk))

    def test_custom_icon_asset_validates_and_saves(self):
        template = self.create_template()
        asset = self.create_media_asset(name="Icon personalizat")
        layout = deepcopy(template.layout_json)
        layout["elements"].append({
            "id": "custom_icon",
            "type": "icon",
            "label": "Icon personalizat",
            "x_mm": 20,
            "y_mm": 20,
            "width_mm": 15,
            "height_mm": 15,
            "rotation": 0,
            "zIndex": 110,
            "locked": False,
            "visible": True,
            "style": {"color": "#164194", "opacity": 0.8},
            "iconName": "award",
            "assetId": str(asset.pk),
            "alt": "Icon personalizat",
        })

        response = self.client.post(
            reverse("diplome:template_editor", kwargs={"template_id": template.pk}),
            {"layout_json": json.dumps(layout)},
        )

        self.assertEqual(response.status_code, 200)
        template.refresh_from_db()
        saved = next(element for element in template.layout_json["elements"] if element["id"] == "custom_icon")
        self.assertEqual(saved["assetId"], str(asset.pk))
        self.assertEqual(saved["iconName"], "award")

    def test_table_content_and_styles_save(self):
        template = self.create_template(with_sample_layout=True)
        layout = deepcopy(template.layout_json)
        table = next(element for element in layout["elements"] if element["type"] == "table")
        table["columns"] = ["Curs", "Ore"]
        table["rows"] = [["SSM", "80"], ["PSI", "40"]]
        table["style"].update({
            "fontSize": 16,
            "bold": True,
            "align": "left",
            "borderColor": "#d41131",
            "headerBackground": "#f3f4f6",
        })

        response = self.client.post(
            reverse("diplome:template_editor", kwargs={"template_id": template.pk}),
            {"layout_json": json.dumps(layout)},
        )

        self.assertEqual(response.status_code, 200)
        template.refresh_from_db()
        saved = next(element for element in template.layout_json["elements"] if element["type"] == "table")
        self.assertEqual(saved["columns"], ["Curs", "Ore"])
        self.assertEqual(saved["rows"], [["SSM", "80"], ["PSI", "40"]])
        self.assertEqual(saved["style"]["borderColor"], "#d41131")

    def test_layout_with_foreign_asset_id_fails(self):
        template = self.create_template()
        foreign_asset = self.create_media_asset(owner=self.other_user)
        original_layout = deepcopy(template.layout_json)
        layout = deepcopy(original_layout)
        self.append_media_element(layout, foreign_asset, element_id="foreign_logo")

        response = self.client.post(
            reverse("diplome:template_editor", kwargs={"template_id": template.pk}),
            {"layout_json": json.dumps(layout)},
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()["success"])
        template.refresh_from_db()
        self.assertEqual(template.layout_json, original_layout)

    def test_invalid_layout_json_is_rejected_without_modifying_template(self):
        template = self.create_template(with_sample_layout=True)
        original = deepcopy(template.layout_json)
        cases = []

        invalid_type = deepcopy(original)
        invalid_type["elements"][0]["type"] = "video"
        cases.append(("element type", json.dumps(invalid_type)))

        invalid_variable = deepcopy(original)
        next(item for item in invalid_variable["elements"] if item["type"] == "variable")["variable"] = "email"
        cases.append(("variable", json.dumps(invalid_variable)))

        invalid_color = deepcopy(original)
        next(item for item in invalid_color["elements"] if item["type"] == "text")["style"]["color"] = "navy"
        cases.append(("color", json.dumps(invalid_color)))

        invalid_geometry = deepcopy(original)
        invalid_geometry["elements"][0]["x_mm"] = -1
        cases.append(("geometry", json.dumps(invalid_geometry)))

        unsafe_html = deepcopy(original)
        next(item for item in unsafe_html["elements"] if item["type"] == "text")["text"] = "<script>alert(1)</script>"
        cases.append(("unsafe html", json.dumps(unsafe_html)))

        duplicate_id = deepcopy(original)
        duplicate_id["elements"][1]["id"] = duplicate_id["elements"][0]["id"]
        cases.append(("duplicate id", json.dumps(duplicate_id)))

        cases.append(("oversized", "x" * (MAX_LAYOUT_JSON_BYTES + 1)))

        url = reverse("diplome:template_editor", kwargs={"template_id": template.pk})
        for label, payload in cases:
            with self.subTest(label=label):
                response = self.client.post(url, {"layout_json": payload})
                self.assertEqual(response.status_code, 400)
                self.assertFalse(response.json()["success"])
                template.refresh_from_db()
                self.assertEqual(template.layout_json, original)

    def test_version_one_pixel_layout_is_converted_to_millimeters(self):
        metric_layout = build_default_layout()
        pixel_layout = deepcopy(metric_layout)
        pixel_layout["version"] = 1
        pixel_layout["page"] = {
            "size": "A4",
            "orientation": "landscape",
            "width": 1123,
            "height": 794,
            "gridSize": 10,
            "background": None,
        }
        for element in pixel_layout["elements"]:
            element["x"] = round(element.pop("x_mm") * 1123 / 297)
            element["y"] = round(element.pop("y_mm") * 794 / 210)
            element["width"] = round(element.pop("width_mm") * 1123 / 297)
            element["height"] = round(element.pop("height_mm") * 794 / 210)

        converted = validate_layout_json(pixel_layout)

        self.assertEqual(converted["version"], 2)
        self.assertEqual(converted["page"]["width_mm"], 297)
        self.assertEqual(converted["page"]["height_mm"], 210)
        self.assertNotIn("x", converted["elements"][0])
        self.assertIn("x_mm", converted["elements"][0])

    def test_preview_renders_sample_participant_data(self):
        template = self.create_template()

        response = self.client.get(
            reverse("diplome:template_preview", kwargs={"template_id": template.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "diplome/template_preview.html")
        self.assertContains(response, 'data-sidebar-start-collapsed="true"')
        self.assertEqual(response.context["sample_participant"]["full_name"], "Andrei Popescu")
        self.assertEqual(response.context["sample_participant"]["date_of_birth"], "12.04.1990")
        self.assertEqual(response.context["sample_participant"]["place_of_birth"], "Brașov")
        self.assertEqual(response.context["sample_participant"]["certificate_number"], "TTK-2026-001")
        self.assertContains(response, "Andrei Popescu")
        self.assertContains(response, "TTK-2026-001")

    def test_delete_is_post_only(self):
        template = self.create_template()
        url = reverse("diplome:template_delete", kwargs={"template_id": template.pk})

        self.assertEqual(self.client.get(url).status_code, 405)
        response = self.client.post(url)

        self.assertRedirects(response, reverse("diplome:template_list"))
        self.assertFalse(DiplomaTemplate.objects.filter(pk=template.pk).exists())

    def test_used_template_delete_preserves_batch_history_snapshot(self):
        template = self.create_template()
        participant_list = ParticipantList.objects.create(
            owner=self.user,
            name="Lista cu istoric",
            source_file_name="istoric.csv",
        )
        DiplomaGenerationBatch.objects.create(
            owner=self.user,
            participant_list=participant_list,
            template=template,
            participant_list_name=participant_list.name,
            template_name=template.name,
            output_folder=f"diplomas/{self.user.pk}/batch-test",
        )

        response = self.client.post(
            reverse("diplome:template_delete", kwargs={"template_id": template.pk}),
            follow=True,
        )

        self.assertRedirects(response, reverse("diplome:template_list"))
        self.assertContains(response, "Template-ul a fost șters.")
        self.assertFalse(DiplomaTemplate.objects.filter(pk=template.pk).exists())
        batch = DiplomaGenerationBatch.objects.get()
        self.assertIsNone(batch.template_id)
        self.assertEqual(batch.template_display_name, "Diplomă absolvire")
```

## `apps/diplome/tests_bulk_generation.py`

Size: 20.1 KB

Redacted secret-like assignments: 2

```python
import tempfile
from io import BytesIO
from unittest.mock import patch
from zipfile import ZipFile

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.test import TestCase, override_settings
from django.urls import reverse

from . import services
from .models import (
    DiplomaGenerationBatch,
    GeneratedDiploma,
    Participant,
    ParticipantList,
)
from .services import (
    create_diploma_template,
    create_generation_batch,
    generate_diploma_batch,
    run_generation_batch,
)


class BulkDiplomaGenerationTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls._media_directory = tempfile.TemporaryDirectory()
        cls._media_override = override_settings(MEDIA_ROOT=cls._media_directory.name)
        cls._media_override.enable()
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls._media_override.disable()
        cls._media_directory.cleanup()

    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        cls.user = user_model.objects.create_user(
            username="bulk-owner",
            password=<redacted>
        )
        cls.other_user = user_model.objects.create_user(
            username="bulk-other",
            password=<redacted>
        )
        cls.participant_list = ParticipantList.objects.create(
            owner=cls.user,
            name="Grupa vară / 2026",
            source_file_name="participanti.csv",
            participant_count=2,
        )
        cls.participant = Participant.objects.create(
            owner=cls.user,
            participant_list=cls.participant_list,
            full_name="Ana Șerban",
            date_of_birth="1990-04-12",
            place_of_birth="Brașov",
            certificate_number="CERT/2026 001",
            source_row=2,
        )
        cls.second_participant = Participant.objects.create(
            owner=cls.user,
            participant_list=cls.participant_list,
            full_name="Ion Ionescu",
            date_of_birth="1991-05-13",
            place_of_birth="Sibiu",
            certificate_number="CERT-002",
            source_row=3,
        )
        cls.template = create_diploma_template(
            owner=cls.user,
            data={
                "name": "Diplomă lot",
                "category": "SSM",
                "description": "",
                "page_size": "A4",
                "orientation": "landscape",
            },
        )
        cls.foreign_list = ParticipantList.objects.create(
            owner=cls.other_user,
            name="Lista străină",
            source_file_name="foreign.csv",
            participant_count=1,
        )
        cls.foreign_participant = Participant.objects.create(
            owner=cls.other_user,
            participant_list=cls.foreign_list,
            full_name="Participant străin",
            date_of_birth="1985-01-01",
            place_of_birth="Cluj-Napoca",
            certificate_number="OTHER-001",
            source_row=2,
        )
        cls.foreign_template = create_diploma_template(
            owner=cls.other_user,
            data={
                "name": "Template străin",
                "category": "General",
                "description": "",
                "page_size": "A4",
                "orientation": "portrait",
            },
        )

    def setUp(self):
        self.client.force_login(self.user)

    def bulk_payload(self, **overrides):
        payload = {
            "participant_list": str(self.participant_list.pk),
            "template": str(self.template.pk),
        }
        payload.update(overrides)
        return payload

    def generate_batch(self):
        return generate_diploma_batch(
            self.user,
            self.participant_list.pk,
            self.template.pk,
        )

    def test_bulk_and_history_pages_require_login(self):
        batch = self.generate_batch()
        routes = (
            reverse("diplome:generation_index"),
            reverse("diplome:history_index"),
            reverse("diplome:batch_detail", kwargs={"batch_id": batch.pk}),
            reverse("diplome:batch_zip_download", kwargs={"batch_id": batch.pk}),
        )
        self.client.logout()
        for url in routes:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response.url.startswith(reverse("login")))

    def test_user_can_bulk_generate_owned_list_and_template(self):
        response = self.client.post(
            reverse("diplome:generation_bulk_create"),
            self.bulk_payload(),
        )

        batch = DiplomaGenerationBatch.objects.get()
        generated = GeneratedDiploma.objects.filter(batch=batch)
        self.assertRedirects(
            response,
            reverse("diplome:batch_detail", kwargs={"batch_id": batch.pk}),
        )
        self.assertEqual(batch.status, DiplomaGenerationBatch.Status.COMPLETED)
        self.assertEqual(batch.total_count, 2)
        self.assertEqual(batch.success_count, 2)
        self.assertEqual(batch.failed_count, 0)
        self.assertEqual(generated.count(), 2)
        for diploma in generated:
            self.assertTrue(diploma.pdf_file.storage.exists(diploma.pdf_file.name))
            self.assertTrue(diploma.pdf_file.name.startswith(f"{batch.output_folder}/"))

    def test_one_participant_failure_completes_with_errors(self):
        original_renderer = services.render_diploma_pdf

        def render_with_one_failure(*, template, participant):
            if participant.pk == self.second_participant.pk:
                raise RuntimeError("renderer details must not reach the UI")
            return original_renderer(template=template, participant=participant)

        with patch(
            "apps.diplome.services.render_diploma_pdf",
            side_effect=render_with_one_failure,
        ):
            batch = self.generate_batch()

        self.assertEqual(
            batch.status,
            DiplomaGenerationBatch.Status.COMPLETED_WITH_ERRORS,
        )
        self.assertEqual(batch.success_count, 1)
        self.assertEqual(batch.failed_count, 1)
        self.assertEqual(GeneratedDiploma.objects.filter(batch=batch).count(), 1)
        self.assertEqual(batch.error_summary[0]["participant_name"], "Ion Ionescu")
        self.assertNotIn("renderer details", str(batch.error_summary))

    def test_batch_fails_when_no_pdf_is_generated(self):
        with patch(
            "apps.diplome.services.render_diploma_pdf",
            side_effect=RuntimeError("renderer unavailable"),
        ):
            batch = self.generate_batch()

        self.assertEqual(batch.status, DiplomaGenerationBatch.Status.FAILED)
        self.assertEqual(batch.success_count, 0)
        self.assertEqual(batch.failed_count, 2)
        self.assertFalse(GeneratedDiploma.objects.filter(batch=batch).exists())

    def test_batch_startup_failure_is_recorded_as_failed(self):
        with patch(
            "apps.diplome.services.run_generation_batch",
            side_effect=RuntimeError("runner unavailable"),
        ):
            with self.assertRaises(RuntimeError):
                self.generate_batch()

        batch = DiplomaGenerationBatch.objects.get()
        self.assertEqual(batch.status, DiplomaGenerationBatch.Status.FAILED)
        self.assertEqual(batch.failed_count, batch.total_count)
        self.assertEqual(
            batch.error_summary,
            [{"message": "Generarea lotului nu a putut porni."}],
        )

    def test_empty_participant_list_is_rejected(self):
        empty_list = ParticipantList.objects.create(
            owner=self.user,
            name="Listă goală",
            source_file_name="empty.csv",
            participant_count=8,
        )
        response = self.client.post(
            reverse("diplome:generation_bulk_create"),
            self.bulk_payload(participant_list=str(empty_list.pk)),
        )

        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "Lista selectată nu conține participanți.", status_code=400)
        self.assertFalse(DiplomaGenerationBatch.objects.exists())

    def test_cross_owner_list_and_template_cannot_be_used(self):
        cases = (
            {"participant_list": str(self.foreign_list.pk)},
            {"template": str(self.foreign_template.pk)},
        )
        for override in cases:
            with self.subTest(override=override):
                response = self.client.post(
                    reverse("diplome:generation_bulk_create"),
                    self.bulk_payload(**override),
                )
                self.assertEqual(response.status_code, 400)
        self.assertFalse(DiplomaGenerationBatch.objects.exists())

    def test_cross_owner_batch_detail_and_zip_return_404(self):
        foreign_batch = generate_diploma_batch(
            self.other_user,
            self.foreign_list.pk,
            self.foreign_template.pk,
        )

        detail = self.client.get(
            reverse("diplome:batch_detail", kwargs={"batch_id": foreign_batch.pk})
        )
        archive = self.client.get(
            reverse(
                "diplome:batch_zip_download",
                kwargs={"batch_id": foreign_batch.pk},
            )
        )

        self.assertEqual(detail.status_code, 404)
        self.assertEqual(archive.status_code, 404)

    def test_zip_contains_only_pdfs_from_requested_batch(self):
        batch = self.generate_batch()
        other_batch = self.generate_batch()
        response = self.client.get(
            reverse("diplome:batch_zip_download", kwargs={"batch_id": batch.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/zip")
        self.assertIn("diplome_grupa_vara_2026_", response["Content-Disposition"])
        with ZipFile(BytesIO(response.content)) as archive:
            names = archive.namelist()
        self.assertEqual(len(names), 2)
        self.assertTrue(all(name.endswith(".pdf") for name in names))
        requested_names = {
            diploma.pdf_file.name.rsplit("/", 1)[-1]
            for diploma in GeneratedDiploma.objects.filter(batch=batch)
        }
        other_names = {
            diploma.pdf_file.name.rsplit("/", 1)[-1]
            for diploma in GeneratedDiploma.objects.filter(batch=other_batch)
        }
        self.assertSetEqual(set(names), requested_names)
        self.assertSetEqual(requested_names, other_names)

    def test_history_and_detail_are_owner_scoped(self):
        owned_batch = self.generate_batch()
        foreign_batch = generate_diploma_batch(
            self.other_user,
            self.foreign_list.pk,
            self.foreign_template.pk,
        )

        history = self.client.get(reverse("diplome:history_index"))
        detail = self.client.get(
            reverse("diplome:batch_detail", kwargs={"batch_id": owned_batch.pk})
        )

        self.assertContains(history, self.participant_list.name)
        self.assertNotContains(history, self.foreign_list.name)
        self.assertContains(detail, self.participant.full_name)
        self.assertContains(detail, self.second_participant.full_name)
        self.assertNotContains(detail, self.foreign_participant.full_name)
        self.assertFalse(
            detail.context["generated_diplomas"].filter(batch=foreign_batch).exists()
        )

    def test_history_exposes_accessible_detail_and_zip_icon_actions(self):
        batch = create_generation_batch(
            self.user,
            self.participant_list.pk,
            self.template.pk,
        )
        batch.success_count = 1
        batch.total_count = 1
        batch.save(update_fields=["success_count", "total_count"])
        generated = GeneratedDiploma.objects.create(
            owner=self.user,
            participant_list=self.participant_list,
            participant=self.participant,
            template=self.template,
            batch=batch,
            certificate_number=self.participant.certificate_number,
            participant_name=self.participant.full_name,
            pdf_file=ContentFile(b"%PDF-1.4", name="diploma-test.pdf"),
        )

        history = self.client.get(reverse("diplome:history_index"))
        detail = self.client.get(
            reverse("diplome:batch_detail", kwargs={"batch_id": batch.pk})
        )

        self.assertContains(history, 'class="table table-xs"')
        self.assertContains(
            history,
            f'href="{reverse("diplome:batch_detail", kwargs={"batch_id": batch.pk})}"',
        )
        self.assertContains(history, 'aria-label="Vezi detaliile lotului"')
        self.assertContains(history, 'class="text-right">Acțiuni</th>')
        self.assertContains(
            history,
            f'action="{reverse("diplome:batch_resume", kwargs={"batch_id": batch.pk})}"',
        )
        self.assertContains(history, 'aria-label="Reia generarea lotului"')
        self.assertContains(history, "text-primary hover:bg-primary/10")
        self.assertContains(
            history,
            f'href="{reverse("diplome:batch_zip_download", kwargs={"batch_id": batch.pk})}"',
        )
        self.assertContains(history, 'aria-label="Descarcă lotul ca arhivă ZIP"')
        self.assertContains(history, "text-success hover:bg-success/10")
        self.assertNotContains(history, ">Detalii</a>")
        self.assertContains(detail, 'class="table table-xs"')
        self.assertContains(detail, 'class="text-right">Acțiuni</th>')
        self.assertContains(
            detail,
            f'href="{reverse("diplome:generation_download", kwargs={"generated_diploma_id": generated.pk})}"',
        )
        self.assertContains(detail, 'aria-label="Descarcă diploma PDF"')
        self.assertContains(detail, "text-success hover:bg-success/10")
        self.assertNotContains(detail, ">Descarcă PDF</a>")

    def test_history_htmx_returns_partial_panel(self):
        owned_batch = create_generation_batch(
            self.user,
            self.participant_list.pk,
            self.template.pk,
        )
        foreign_batch = create_generation_batch(
            self.other_user,
            self.foreign_list.pk,
            self.foreign_template.pk,
        )

        response = self.client.get(
            reverse("diplome:history_index"),
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "diplome/includes/history_panel.html")
        self.assertContains(response, 'id="history-panel"')
        self.assertContains(response, owned_batch.participant_list_display_name)
        self.assertNotContains(response, foreign_batch.participant_list_display_name)
        self.assertNotContains(response, "<title>")

    def test_pending_batch_resume_from_history_htmx_refreshes_history_panel(self):
        batch = create_generation_batch(
            self.user,
            self.participant_list.pk,
            self.template.pk,
        )

        response = self.client.post(
            reverse("diplome:batch_resume", kwargs={"batch_id": batch.pk}),
            HTTP_HX_REQUEST="true",
            HTTP_HX_TARGET="history-panel",
        )

        batch.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "diplome/includes/history_panel.html")
        self.assertEqual(batch.status, DiplomaGenerationBatch.Status.COMPLETED)
        self.assertContains(response, "Lot finalizat")
        self.assertContains(response, batch.participant_list_display_name)
        self.assertContains(response, batch.get_status_display())
        self.assertNotContains(response, "<title>")

    def test_batch_detail_htmx_and_resume_refresh_detail_panel(self):
        batch = create_generation_batch(
            self.user,
            self.participant_list.pk,
            self.template.pk,
        )
        detail_url = reverse("diplome:batch_detail", kwargs={"batch_id": batch.pk})

        detail = self.client.get(detail_url, HTTP_HX_REQUEST="true")
        self.assertEqual(detail.status_code, 200)
        self.assertTemplateUsed(detail, "diplome/includes/batch_detail_panel.html")
        self.assertContains(detail, 'id="batch-detail-panel"')
        self.assertContains(detail, "Reia generarea")
        self.assertNotContains(detail, "<title>")

        response = self.client.post(
            reverse("diplome:batch_resume", kwargs={"batch_id": batch.pk}),
            HTTP_HX_REQUEST="true",
            HTTP_HX_TARGET="batch-detail-panel",
        )

        batch.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "diplome/includes/batch_detail_panel.html")
        self.assertEqual(batch.status, DiplomaGenerationBatch.Status.COMPLETED)
        self.assertContains(response, "Lot finalizat")
        self.assertContains(response, batch.get_status_display())
        self.assertNotContains(response, "Reia generarea")
        self.assertContains(response, reverse("diplome:batch_zip_download", kwargs={"batch_id": batch.pk}))

    def test_pending_batch_can_be_resumed(self):
        batch = create_generation_batch(
            self.user,
            self.participant_list.pk,
            self.template.pk,
        )

        response = self.client.post(
            reverse("diplome:batch_resume", kwargs={"batch_id": batch.pk})
        )

        self.assertRedirects(
            response,
            reverse("diplome:batch_detail", kwargs={"batch_id": batch.pk}),
        )
        batch.refresh_from_db()
        self.assertEqual(batch.status, DiplomaGenerationBatch.Status.COMPLETED)
        self.assertEqual(batch.success_count, 2)
        self.assertEqual(batch.failed_count, 0)

    def test_batch_resume_is_post_only_and_owner_scoped(self):
        owned_batch = create_generation_batch(
            self.user,
            self.participant_list.pk,
            self.template.pk,
        )
        foreign_batch = create_generation_batch(
            self.other_user,
            self.foreign_list.pk,
            self.foreign_template.pk,
        )

        get_response = self.client.get(
            reverse("diplome:batch_resume", kwargs={"batch_id": owned_batch.pk})
        )
        foreign_response = self.client.post(
            reverse("diplome:batch_resume", kwargs={"batch_id": foreign_batch.pk})
        )

        self.assertEqual(get_response.status_code, 405)
        self.assertEqual(foreign_response.status_code, 404)
        foreign_batch.refresh_from_db()
        self.assertEqual(foreign_batch.status, DiplomaGenerationBatch.Status.PENDING)

    def test_individual_download_still_works_for_batch_pdf(self):
        batch = self.generate_batch()
        generated = GeneratedDiploma.objects.filter(batch=batch).first()
        response = self.client.get(
            reverse(
                "diplome:generation_download",
                kwargs={"generated_diploma_id": generated.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertEqual(b"".join(response.streaming_content)[:5], b"%PDF-")

    def test_run_generation_batch_needs_only_the_batch_id(self):
        batch = create_generation_batch(
            self.user,
            self.participant_list.pk,
            self.template.pk,
        )

        result = run_generation_batch(batch.pk)

        self.assertEqual(result.status, DiplomaGenerationBatch.Status.COMPLETED)
        self.assertEqual(result.success_count, 2)

    def test_navigation_active_state_for_generation_and_history(self):
        generation = self.client.get(reverse("diplome:generation_index"))
        batch = self.generate_batch()
        history_detail = self.client.get(
            reverse("diplome:batch_detail", kwargs={"batch_id": batch.pk})
        )

        self.assertContains(
            generation,
            f'href="{reverse("diplome:generation_index")}" class="transition-none active font-semibold" aria-current="page"',
        )
        self.assertContains(
            history_detail,
            f'href="{reverse("diplome:history_index")}" class="transition-none active font-semibold" aria-current="page"',
        )
```

## `apps/diplome/tests_generation.py`

Size: 15.3 KB

Redacted secret-like assignments: 2

```python
import tempfile
from html import escape
from urllib.parse import urlencode

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import GeneratedDiploma, Participant, ParticipantList
from .services import build_default_layout, create_diploma_template, generate_single_diploma


class DiplomaGenerationTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls._media_directory = tempfile.TemporaryDirectory()
        cls._media_override = override_settings(MEDIA_ROOT=cls._media_directory.name)
        cls._media_override.enable()
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls._media_override.disable()
        cls._media_directory.cleanup()

    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        cls.user = user_model.objects.create_user(
            username="generation-owner",
            password=<redacted>
        )
        cls.other_user = user_model.objects.create_user(
            username="generation-other",
            password=<redacted>
        )
        cls.participant_list = ParticipantList.objects.create(
            owner=cls.user,
            name="Grupa SSM iulie",
            course_name="Inspector SSM",
            source_file_name="participanti.csv",
            participant_count=2,
        )
        cls.participant = Participant.objects.create(
            owner=cls.user,
            participant_list=cls.participant_list,
            full_name="Ana Șerban",
            date_of_birth="1990-04-12",
            place_of_birth="Brașov",
            certificate_number="CERT/2026 001",
            source_row=2,
        )
        cls.other_participant = Participant.objects.create(
            owner=cls.user,
            participant_list=cls.participant_list,
            full_name="Ion Ionescu",
            date_of_birth="1991-05-13",
            place_of_birth="Sibiu",
            certificate_number="CERT-002",
            source_row=3,
        )
        cls.template = create_diploma_template(
            owner=cls.user,
            data={
                "name": "Diplomă SSM",
                "category": "SSM",
                "description": "Template de test",
                "page_size": "A4",
                "orientation": "landscape",
            },
        )
        cls.foreign_list = ParticipantList.objects.create(
            owner=cls.other_user,
            name="Lista altui utilizator",
            source_file_name="foreign.csv",
            participant_count=1,
        )
        cls.foreign_participant = Participant.objects.create(
            owner=cls.other_user,
            participant_list=cls.foreign_list,
            full_name="Participant străin",
            date_of_birth="1988-01-02",
            place_of_birth="Cluj-Napoca",
            certificate_number="FOREIGN-001",
            source_row=2,
        )
        cls.foreign_template = create_diploma_template(
            owner=cls.other_user,
            data={
                "name": "Template străin",
                "category": "General",
                "description": "",
                "page_size": "A4",
                "orientation": "portrait",
            },
        )

    def setUp(self):
        self.client.force_login(self.user)

    def selection_payload(self, **overrides):
        payload = {
            "participant_list": str(self.participant_list.pk),
            "participant": str(self.participant.pk),
            "template": str(self.template.pk),
        }
        payload.update(overrides)
        return payload

    def preview_url(self):
        return f"{reverse('diplome:generation_preview')}?{urlencode(self.selection_payload())}"

    def generate_record(self):
        return generate_single_diploma(
            owner=self.user,
            participant_list_id=self.participant_list.pk,
            participant_id=self.participant.pk,
            template_id=self.template.pk,
        )

    def test_pdf_generation_supports_typography_and_list_elements(self):
        layout = build_default_layout(
            page_size=self.template.page_size,
            orientation=self.template.orientation,
        )
        title = next(element for element in layout["elements"] if element["type"] == "text")
        title["style"].update({
            "lineHeight": 1.35,
            "letterSpacing": 1.25,
            "textTransform": "uppercase",
        })
        layout["elements"].append({
            "id": "pdf_list",
            "type": "list",
            "label": "Listă PDF",
            "x_mm": 20,
            "y_mm": 110,
            "width_mm": 90,
            "height_mm": 35,
            "rotation": 0,
            "zIndex": 95,
            "locked": False,
            "visible": True,
            "style": {
                "fontFamily": "Inter",
                "fontSize": 14,
                "bold": False,
                "italic": False,
                "underline": False,
                "color": "#111827",
                "align": "left",
                "lineHeight": 1.2,
                "letterSpacing": 0.5,
                "textTransform": "none",
                "listType": "number",
                "indent_mm": 5,
            },
            "items": ["Primul punct", "Al doilea punct"],
        })
        self.template.layout_json = layout
        self.template.save(update_fields=("layout_json", "updated_at"))

        generated = self.generate_record()

        with generated.pdf_file.open("rb") as pdf_file:
            self.assertEqual(pdf_file.read(5), b"%PDF-")

    def test_generation_pages_require_login(self):
        generated = self.generate_record()
        routes = (
            ("get", reverse("diplome:generation_index"), None),
            ("get", self.preview_url(), None),
            ("post", reverse("diplome:generation_create"), self.selection_payload()),
            (
                "get",
                reverse(
                    "diplome:generation_download",
                    kwargs={"generated_diploma_id": generated.pk},
                ),
                None,
            ),
        )
        self.client.logout()
        for method, url, data in routes:
            with self.subTest(url=url):
                response = getattr(self.client, method)(url, data or {})
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response.url.startswith(reverse("login")))

    def test_generation_index_lists_only_owned_templates_and_lists(self):
        response = self.client.get(reverse("diplome:generation_index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.participant_list.name)
        self.assertContains(response, self.template.name)
        self.assertNotContains(response, self.foreign_list.name)
        self.assertNotContains(response, self.foreign_template.name)

    def test_generation_index_restores_preview_selection_from_query_string(self):
        response = self.client.get(
            reverse("diplome:generation_index"),
            self.selection_payload(),
        )

        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertEqual(str(form["participant_list"].value()), str(self.participant_list.pk))
        self.assertEqual(str(form["participant"].value()), str(self.participant.pk))
        self.assertEqual(str(form["template"].value()), str(self.template.pk))

    def test_generation_index_renders_single_select_participant_table(self):
        response = self.client.get(reverse("diplome:generation_index"))

        self.assertContains(response, "data-participant-table")
        self.assertContains(
            response,
            f'data-participant-id="{self.participant.pk}"',
        )
        self.assertContains(response, 'type="radio"', count=2)

    def test_multiple_participants_are_rejected(self):
        payload = self.selection_payload()
        payload["participant"] = [
            str(self.participant.pk),
            str(self.other_participant.pk),
        ]

        response = self.client.post(reverse("diplome:generation_create"), payload)

        self.assertEqual(response.status_code, 400)
        self.assertFormError(
            response.context["form"],
            "participant",
            "Selectează un singur participant.",
        )
        self.assertFalse(GeneratedDiploma.objects.exists())

    def test_participant_must_belong_to_selected_owned_list(self):
        second_list = ParticipantList.objects.create(
            owner=self.user,
            name="Altă listă",
            source_file_name="alta.csv",
            participant_count=0,
        )
        response = self.client.post(
            reverse("diplome:generation_index"),
            self.selection_payload(participant_list=str(second_list.pk)),
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "participant",
            "Participantul nu aparține listei selectate.",
        )

    def test_cross_owner_objects_cannot_be_used_for_generation(self):
        cases = (
            {"participant_list": str(self.foreign_list.pk)},
            {"participant": str(self.foreign_participant.pk)},
            {"template": str(self.foreign_template.pk)},
        )
        for override in cases:
            with self.subTest(override=override):
                response = self.client.post(
                    reverse("diplome:generation_create"),
                    self.selection_payload(**override),
                )
                self.assertEqual(response.status_code, 400)
                self.assertTrue(response.context["form"].errors)
        self.assertFalse(GeneratedDiploma.objects.exists())

    def test_preview_renders_real_participant_values(self):
        response = self.client.get(self.preview_url())

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "diplome/generation_preview.html")
        self.assertContains(response, self.participant.full_name)
        self.assertContains(response, "12.04.1990")
        self.assertContains(response, self.participant.place_of_birth)
        self.assertContains(response, self.participant.certificate_number)
        self.assertContains(response, self.template.name)
        self.assertContains(response, self.participant_list.name)
        self.assertContains(
            response,
            f'{reverse("diplome:generation_index")}?'
            f'{escape(response.context["selection_query"])}',
            count=2,
        )

    def test_preview_rejects_malformed_or_cross_owner_selection(self):
        malformed = self.client.get(
            reverse("diplome:generation_preview"),
            {
                "participant_list": "invalid",
                "participant": self.participant.pk,
                "template": self.template.pk,
            },
        )
        foreign = self.client.get(
            reverse("diplome:generation_preview"),
            self.selection_payload(template=str(self.foreign_template.pk)),
        )

        self.assertEqual(malformed.status_code, 404)
        self.assertEqual(foreign.status_code, 404)

    def test_generate_single_diploma_stores_pdf_and_snapshot(self):
        response = self.client.post(
            reverse("diplome:generation_create"),
            self.selection_payload(),
        )

        generated = GeneratedDiploma.objects.get()
        self.assertEqual(response.status_code, 302)
        self.assertIn(f"generated={generated.pk}", response.url)
        self.assertEqual(generated.owner, self.user)
        self.assertEqual(generated.participant_name, self.participant.full_name)
        self.assertEqual(
            generated.certificate_number,
            self.participant.certificate_number,
        )
        self.assertTrue(generated.pdf_file.storage.exists(generated.pdf_file.name))
        self.assertTrue(
            generated.pdf_file.name.startswith(
                f"diplomas/{self.user.pk}/{self.participant_list.pk}/"
            )
        )
        with generated.pdf_file.open("rb") as pdf_file:
            self.assertEqual(pdf_file.read(5), b"%PDF-")

    def test_download_returns_owned_pdf_with_safe_filename(self):
        generated = self.generate_record()
        response = self.client.get(
            reverse(
                "diplome:generation_download",
                kwargs={"generated_diploma_id": generated.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertIn("attachment;", response["Content-Disposition"])
        self.assertIn("diploma_cert_2026_001_ana_serban.pdf", response["Content-Disposition"])
        self.assertEqual(b"".join(response.streaming_content)[:5], b"%PDF-")

    def test_cross_owner_download_returns_404(self):
        generated = generate_single_diploma(
            owner=self.other_user,
            participant_list_id=self.foreign_list.pk,
            participant_id=self.foreign_participant.pk,
            template_id=self.foreign_template.pk,
        )

        response = self.client.get(
            reverse(
                "diplome:generation_download",
                kwargs={"generated_diploma_id": generated.pk},
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_source_records_can_be_deleted_without_losing_pdf_history(self):
        generated = self.generate_record()
        stored_name = generated.pdf_file.name

        template_response = self.client.post(
            reverse(
                "diplome:template_delete",
                kwargs={"template_id": self.template.pk},
            )
        )
        list_response = self.client.post(
            reverse(
                "diplome:participant_list_delete",
                kwargs={"participant_list_id": self.participant_list.pk},
            )
        )

        self.assertRedirects(template_response, reverse("diplome:template_list"))
        self.assertRedirects(list_response, reverse("diplome:list_index"))
        generated.refresh_from_db()
        self.assertIsNone(generated.template_id)
        self.assertIsNone(generated.participant_list_id)
        self.assertIsNone(generated.participant_id)
        self.assertEqual(generated.template_name, "Diplomă SSM")
        self.assertEqual(generated.participant_list_name, "Grupa SSM iulie")
        self.assertTrue(generated.pdf_file.storage.exists(stored_name))
        download = self.client.get(
            reverse(
                "diplome:generation_download",
                kwargs={"generated_diploma_id": generated.pk},
            )
        )
        self.assertEqual(download.status_code, 200)
        self.assertEqual(b"".join(download.streaming_content)[:5], b"%PDF-")

    def test_invalid_selection_returns_form_errors(self):
        response = self.client.post(reverse("diplome:generation_create"), {})

        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.context["form"].errors)
        self.assertFalse(GeneratedDiploma.objects.exists())

    def test_generation_navigation_is_active_on_preview(self):
        response = self.client.get(self.preview_url())

        self.assertContains(
            response,
            f'href="{reverse("diplome:generation_index")}" class="transition-none active font-semibold" aria-current="page"',
        )
```

## `apps/diplome/tests_participants.py`

Size: 23.7 KB

Redacted secret-like assignments: 2

```python
from datetime import datetime, timedelta
from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from openpyxl import Workbook

from .models import (
    DiplomaGenerationBatch,
    Participant,
    ParticipantImportDraft,
    ParticipantList,
)
from .services import (
    PARTICIPANT_DATE_ERROR,
    create_diploma_template,
    parse_participant_upload,
)


def csv_upload(*rows, name="participanti.csv"):
    content = "\n".join(
        (
            "Nume complet;Data nașterii;Locul nașterii;Număr certificat",
            *rows,
        )
    )
    return SimpleUploadedFile(name, content.encode("utf-8"), content_type="text/csv")


def xlsx_upload(*, number_format="DD.MM.YYYY", date_value=None):
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.append(
        ["Nume complet", "Data nașterii", "Locul nașterii", "Număr certificat"]
    )
    worksheet.append(
        [
            "Ana Popescu",
            date_value if date_value is not None else datetime(1990, 4, 12),
            "Brașov",
            "CERT-001",
        ]
    )
    worksheet["B2"].number_format = number_format
    buffer = BytesIO()
    workbook.save(buffer)
    return SimpleUploadedFile(
        "participanti.xlsx",
        buffer.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


def multi_sheet_xlsx_upload():
    workbook = Workbook()
    notes = workbook.active
    notes.title = "Instrucțiuni"
    notes.append(["Această foaie nu conține participanți."])

    headers = [
        "Nume complet",
        "Data nașterii",
        "Locul nașterii",
        "Număr certificat",
    ]
    first = workbook.create_sheet("Grupa 1")
    first.append(headers)
    first.append(["Ana Popescu", datetime(1990, 4, 12), "Brașov", "CERT-001"])
    first["B2"].number_format = "DD.MM.YYYY"

    second = workbook.create_sheet("Grupa 2")
    second.append(headers)
    second.append(["Ion Ionescu", datetime(1991, 5, 13), "Sibiu", "CERT-002"])
    second["B2"].number_format = "DD.MM.YYYY"

    buffer = BytesIO()
    workbook.save(buffer)
    return SimpleUploadedFile(
        "participanti-mai-multe-foi.xlsx",
        buffer.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


def mapping_payload():
    return {
        "column_0": "full_name",
        "column_1": "date_of_birth",
        "column_2": "place_of_birth",
        "column_3": "certificate_number",
    }


class ParticipantImportTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="participant-owner",
            password=<redacted>
        )
        cls.other_user = get_user_model().objects.create_user(
            username="participant-other",
            password=<redacted>
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_participant_pages_require_login(self):
        participant_list = ParticipantList.objects.create(
            owner=self.user,
            name="Lista permanentă",
            source_file_name="participanti.csv",
        )
        draft = ParticipantImportDraft.objects.create(
            owner=self.user,
            list_name="Import",
            source_file_name="participanti.csv",
            mapping_confirmed=True,
            valid_rows_json=[],
            invalid_rows_json=[],
            warnings_json=[],
            expires_at=timezone.now() + timedelta(hours=1),
        )
        routes = (
            reverse("diplome:list_index"),
            reverse("diplome:participant_import"),
            reverse(
                "diplome:participant_import_sheet", kwargs={"draft_id": draft.pk}
            ),
            reverse("diplome:participant_import_mapping", kwargs={"draft_id": draft.pk}),
            reverse("diplome:participant_import_preview", kwargs={"draft_id": draft.pk}),
            reverse(
                "diplome:participant_list_detail",
                kwargs={"participant_list_id": participant_list.pk},
            ),
        )
        self.client.logout()
        for url in routes:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response.url.startswith(reverse("login")))

    def test_csv_accepts_only_strict_dd_mm_yyyy_dates(self):
        valid = parse_participant_upload(
            upload=csv_upload("Ana Popescu;12.04.1990;Brașov;CERT-001")
        )
        self.assertEqual(valid["valid_rows"][0]["date_of_birth"], "12.04.1990")

        invalid_dates = ("12/04/1990", "1990-04-12", "1.4.1990", "31.02.1990")
        for value in invalid_dates:
            with self.subTest(value=value):
                parsed = parse_participant_upload(
                    upload=csv_upload(f"Ana Popescu;{value};Brașov;CERT-001")
                )
                self.assertEqual(parsed["valid_rows"], [])
                self.assertIn(PARTICIPANT_DATE_ERROR, parsed["invalid_rows"][0]["errors"])

    def test_excel_date_cell_is_normalized_independently_of_locale_format(self):
        accepted_formats = (
            "DD.MM.YYYY",
            "dd.mm.yyyy;@",
            '[$-ro-RO]dd"."mm"."yyyy',
            r"dd\.mm\.yyyy",
            "YYYY-MM-DD",
            "mm-dd-yy",
        )
        for number_format in accepted_formats:
            with self.subTest(number_format=number_format):
                accepted = parse_participant_upload(
                    upload=xlsx_upload(number_format=number_format)
                )
                self.assertEqual(
                    accepted["valid_rows"][0]["date_of_birth"],
                    "12.04.1990",
                )

    def test_excel_text_date_still_requires_dd_mm_yyyy(self):
        rejected = parse_participant_upload(
            upload=xlsx_upload(date_value="1990-04-12", number_format="@")
        )

        self.assertEqual(rejected["valid_rows"], [])
        self.assertIn(PARTICIPANT_DATE_ERROR, rejected["invalid_rows"][0]["errors"])

    def test_xlsx_import_uses_only_the_selected_visible_sheet(self):
        parsed = parse_participant_upload(
            upload=multi_sheet_xlsx_upload(),
            worksheet_name="Grupa 2",
        )

        self.assertEqual(
            [row["full_name"] for row in parsed["valid_rows"]],
            ["Ion Ionescu"],
        )
        self.assertEqual(parsed["valid_rows"][0]["source_row"], 2)
        self.assertEqual(parsed["invalid_rows"], [])

    def test_multi_sheet_xlsx_prompts_for_a_sheet_before_column_mapping(self):
        response = self.client.post(
            reverse("diplome:participant_import"),
            {
                "list_name": "Grupe separate",
                "first_row_has_headers": "on",
                "source_file": multi_sheet_xlsx_upload(),
            },
        )

        draft = ParticipantImportDraft.objects.get()
        self.assertRedirects(
            response,
            reverse("diplome:participant_import_sheet", kwargs={"draft_id": draft.pk}),
        )
        self.assertEqual(
            [sheet["name"] for sheet in draft.source_sheets_json],
            ["Grupa 1", "Grupa 2"],
        )
        self.assertEqual(draft.source_columns_json, [])
        self.assertEqual(draft.source_rows_json, [])

        selection_page = self.client.get(response.url)
        self.assertContains(selection_page, "Grupa 1")
        self.assertContains(selection_page, "Grupa 2")
        self.assertNotContains(selection_page, "Instrucțiuni")

        selection_response = self.client.post(response.url, {"sheet_index": "1"})
        draft.refresh_from_db()
        self.assertRedirects(
            selection_response,
            reverse("diplome:participant_import_mapping", kwargs={"draft_id": draft.pk}),
        )
        self.assertEqual(len(draft.source_rows_json), 1)
        self.assertEqual(draft.source_rows_json[0]["values"][0], "Ion Ionescu")

    def test_missing_list_name_uses_application_validation_message(self):
        response = self.client.post(
            reverse("diplome:participant_import"),
            {"source_file": xlsx_upload(), "first_row_has_headers": "on"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Numele listei este obligatoriu.", count=2)
        self.assertContains(response, "data-participant-import-toast")
        self.assertFalse(ParticipantImportDraft.objects.exists())

    def test_upload_creates_preview_draft_without_creating_a_list(self):
        response = self.client.post(
            reverse("diplome:participant_import"),
            {
                "list_name": "  Curs   SSM  ",
                "description": "Grupa iulie",
                "course_name": "Inspector SSM",
                "first_row_has_headers": "on",
                "source_file": csv_upload(
                    "Ana Popescu;12.04.1990;Brașov;CERT-001",
                    "Ion Ionescu;1991-05-13;Sibiu;CERT-002",
                ),
            },
        )

        draft = ParticipantImportDraft.objects.get()
        self.assertRedirects(
            response,
            reverse("diplome:participant_import_mapping", kwargs={"draft_id": draft.pk}),
        )
        self.assertEqual(draft.owner, self.user)
        self.assertEqual(draft.list_name, "Curs SSM")
        self.assertEqual(len(draft.source_columns_json), 4)
        self.assertEqual(len(draft.source_rows_json), 2)
        self.assertEqual(draft.valid_rows_json, [])
        self.assertEqual(draft.invalid_rows_json, [])
        self.assertFalse(ParticipantList.objects.exists())

        mapping_response = self.client.post(
            reverse("diplome:participant_import_mapping", kwargs={"draft_id": draft.pk}),
            mapping_payload(),
        )
        draft.refresh_from_db()
        self.assertRedirects(
            mapping_response,
            reverse("diplome:participant_import_preview", kwargs={"draft_id": draft.pk}),
        )
        self.assertEqual(len(draft.valid_rows_json), 1)
        self.assertEqual(len(draft.invalid_rows_json), 1)
        self.assertFalse(ParticipantList.objects.exists())

    def test_confirm_import_creates_permanent_owned_list_and_participants(self):
        upload_response = self.client.post(
            reverse("diplome:participant_import"),
            {
                "list_name": "Grupa iulie",
                "description": "Participanți validați",
                "course_name": "Inspector SSM",
                "first_row_has_headers": "on",
                "source_file": csv_upload(
                    "Ana Popescu;12.04.1990;Brașov;CERT-001",
                    "Ion Ionescu;13.05.1991;Sibiu;CERT-002",
                ),
            },
        )
        draft = ParticipantImportDraft.objects.get()
        self.client.post(
            reverse("diplome:participant_import_mapping", kwargs={"draft_id": draft.pk}),
            mapping_payload(),
        )

        response = self.client.post(
            reverse("diplome:participant_import_confirm", kwargs={"draft_id": draft.pk})
        )

        participant_list = ParticipantList.objects.get()
        self.assertRedirects(
            response,
            reverse(
                "diplome:participant_list_detail",
                kwargs={"participant_list_id": participant_list.pk},
            ),
        )
        self.assertEqual(participant_list.owner, self.user)
        self.assertEqual(participant_list.participant_count, 2)
        self.assertEqual(participant_list.course_name, "Inspector SSM")
        self.assertEqual(Participant.objects.filter(owner=self.user).count(), 2)
        self.assertFalse(ParticipantImportDraft.objects.exists())

    def test_custom_headers_are_discovered_and_mapped_by_the_user(self):
        upload = SimpleUploadedFile(
            "custom.csv",
            (
                "Persoană;Născut la;Localitate;Serie\n"
                "Ana Popescu;12.04.1990;Brașov;CERT-001"
            ).encode("utf-8"),
            content_type="text/csv",
        )
        response = self.client.post(
            reverse("diplome:participant_import"),
            {
                "list_name": "Antet personalizat",
                "first_row_has_headers": "on",
                "source_file": upload,
            },
        )
        draft = ParticipantImportDraft.objects.get()

        self.assertRedirects(
            response,
            reverse("diplome:participant_import_mapping", kwargs={"draft_id": draft.pk}),
        )
        self.assertEqual(
            [column["label"] for column in draft.source_columns_json],
            ["Persoană", "Născut la", "Localitate", "Serie"],
        )
        self.assertEqual(draft.column_mapping_json, {})

        mapping_response = self.client.post(
            reverse("diplome:participant_import_mapping", kwargs={"draft_id": draft.pk}),
            mapping_payload(),
        )
        draft.refresh_from_db()

        self.assertRedirects(
            mapping_response,
            reverse("diplome:participant_import_preview", kwargs={"draft_id": draft.pk}),
        )
        self.assertTrue(draft.mapping_confirmed)
        self.assertEqual(draft.valid_rows_json[0]["full_name"], "Ana Popescu")

    def test_headerless_file_generates_columns_without_losing_first_participant(self):
        upload = SimpleUploadedFile(
            "fara-antet.csv",
            (
                "Ana Popescu;12.04.1990;Brașov;CERT-001\n"
                "Ion Ionescu;13.05.1991;Sibiu;CERT-002"
            ).encode("utf-8"),
            content_type="text/csv",
        )
        self.client.post(
            reverse("diplome:participant_import"),
            {"list_name": "Fără antet", "source_file": upload},
        )
        draft = ParticipantImportDraft.objects.get()

        self.assertEqual(
            [column["label"] for column in draft.source_columns_json],
            ["Coloana 1", "Coloana 2", "Coloana 3", "Coloana 4"],
        )
        self.assertEqual(len(draft.source_rows_json), 2)
        self.assertEqual(draft.source_rows_json[0]["source_row"], 1)

        self.client.post(
            reverse("diplome:participant_import_mapping", kwargs={"draft_id": draft.pk}),
            mapping_payload(),
        )
        draft.refresh_from_db()
        self.assertEqual(len(draft.valid_rows_json), 2)
        self.assertEqual(draft.valid_rows_json[0]["full_name"], "Ana Popescu")

    def test_confirm_refuses_draft_without_valid_rows(self):
        draft = ParticipantImportDraft.objects.create(
            owner=self.user,
            list_name="Import invalid",
            source_file_name="participanti.csv",
            mapping_confirmed=True,
            valid_rows_json=[],
            invalid_rows_json=[],
            warnings_json=[],
            expires_at=timezone.now() + timedelta(hours=1),
        )

        response = self.client.post(
            reverse("diplome:participant_import_confirm", kwargs={"draft_id": draft.pk})
        )

        self.assertRedirects(
            response,
            reverse("diplome:participant_import_preview", kwargs={"draft_id": draft.pk}),
        )
        self.assertFalse(ParticipantList.objects.exists())

    def test_list_and_detail_are_owner_scoped(self):
        own = ParticipantList.objects.create(
            owner=self.user,
            name="Lista proprie",
            source_file_name="own.csv",
        )
        foreign = ParticipantList.objects.create(
            owner=self.other_user,
            name="Lista străină",
            source_file_name="foreign.csv",
        )

        response = self.client.get(reverse("diplome:list_index"))

        self.assertContains(response, own.name)
        self.assertNotContains(response, foreign.name)
        self.assertEqual(
            self.client.get(
                reverse(
                    "diplome:participant_list_detail",
                    kwargs={"participant_list_id": foreign.pk},
                )
            ).status_code,
            404,
        )

    def test_participant_list_htmx_returns_partial_panel(self):
        own = ParticipantList.objects.create(
            owner=self.user,
            name="Lista proprie",
            source_file_name="own.csv",
        )
        foreign = ParticipantList.objects.create(
            owner=self.other_user,
            name="Lista străină",
            source_file_name="foreign.csv",
        )

        response = self.client.get(
            reverse("diplome:list_index"),
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "diplome/includes/participant_list_panel.html")
        self.assertContains(response, 'id="participant-list-panel"')
        self.assertContains(response, own.name)
        self.assertNotContains(response, foreign.name)
        self.assertNotContains(response, "<title>")

    def test_participant_list_delete_htmx_refreshes_list_panel(self):
        participant_list = ParticipantList.objects.create(
            owner=self.user,
            name="Lista de șters",
            source_file_name="delete.csv",
        )
        keep = ParticipantList.objects.create(
            owner=self.user,
            name="Lista păstrată",
            source_file_name="keep.csv",
        )

        response = self.client.post(
            reverse(
                "diplome:participant_list_delete",
                kwargs={"participant_list_id": participant_list.pk},
            ),
            HTTP_HX_REQUEST="true",
            HTTP_HX_TARGET="participant-list-panel",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "diplome/includes/participant_list_panel.html")
        self.assertFalse(ParticipantList.objects.filter(pk=participant_list.pk).exists())
        self.assertContains(response, "Lista de participanți a fost ștearsă.")
        self.assertContains(response, keep.name)
        self.assertNotContains(response, participant_list.name)

    def test_participant_detail_htmx_pagination_returns_partial_panel(self):
        participant_list = ParticipantList.objects.create(
            owner=self.user,
            name="Lista paginată",
            source_file_name="participanti.csv",
            participant_count=101,
        )
        participants = [
            Participant(
                owner=self.user,
                participant_list=participant_list,
                full_name=f"Participant {index:03d}",
                date_of_birth=datetime(1990, 4, 12).date(),
                place_of_birth="Brașov",
                certificate_number=f"CERT-{index:03d}",
                source_row=index,
            )
            for index in range(1, 102)
        ]
        Participant.objects.bulk_create(participants)

        response = self.client.get(
            reverse(
                "diplome:participant_list_detail",
                kwargs={"participant_list_id": participant_list.pk},
            ),
            {"page": "2"},
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "diplome/includes/participant_list_detail_panel.html",
        )
        self.assertContains(response, 'id="participant-list-detail-panel"')
        self.assertContains(response, "Participant 101")
        self.assertNotContains(response, "Participant 001")
        self.assertNotContains(response, "<title>")

    def test_confirmed_list_does_not_expire(self):
        participant_list = ParticipantList.objects.create(
            owner=self.user,
            name="Lista veche",
            source_file_name="veche.csv",
        )
        ParticipantList.objects.filter(pk=participant_list.pk).update(
            created_at=timezone.now() - timedelta(days=3650),
            updated_at=timezone.now() - timedelta(days=3650),
        )

        list_response = self.client.get(reverse("diplome:list_index"))
        detail_response = self.client.get(
            reverse(
                "diplome:participant_list_detail",
                kwargs={"participant_list_id": participant_list.pk},
            )
        )

        self.assertContains(list_response, "Lista veche")
        self.assertEqual(detail_response.status_code, 200)

    def test_delete_is_post_only_owner_scoped_and_cascades(self):
        participant_list = ParticipantList.objects.create(
            owner=self.user,
            name="De șters",
            source_file_name="delete.csv",
            participant_count=1,
        )
        Participant.objects.create(
            owner=self.user,
            participant_list=participant_list,
            full_name="Ana Popescu",
            date_of_birth=datetime(1990, 4, 12).date(),
            place_of_birth="Brașov",
            certificate_number="CERT-001",
            source_row=2,
        )
        url = reverse(
            "diplome:participant_list_delete",
            kwargs={"participant_list_id": participant_list.pk},
        )

        self.assertEqual(self.client.get(url).status_code, 405)
        response = self.client.post(url)

        self.assertRedirects(response, reverse("diplome:list_index"))
        self.assertFalse(ParticipantList.objects.exists())
        self.assertFalse(Participant.objects.exists())

    def test_used_list_delete_preserves_batch_history_snapshot(self):
        participant_list = ParticipantList.objects.create(
            owner=self.user,
            name="Lista folosită",
            source_file_name="istoric.csv",
        )
        template = create_diploma_template(
            owner=self.user,
            data={
                "name": "Template istoric",
                "category": "General",
                "description": "",
                "page_size": "A4",
                "orientation": "landscape",
            },
        )
        DiplomaGenerationBatch.objects.create(
            owner=self.user,
            participant_list=participant_list,
            template=template,
            participant_list_name=participant_list.name,
            template_name=template.name,
            output_folder=f"diplomas/{self.user.pk}/batch-list-test",
        )

        response = self.client.post(
            reverse(
                "diplome:participant_list_delete",
                kwargs={"participant_list_id": participant_list.pk},
            ),
            follow=True,
        )

        self.assertRedirects(response, reverse("diplome:list_index"))
        self.assertContains(response, "Lista de participanți a fost ștearsă.")
        self.assertFalse(ParticipantList.objects.filter(pk=participant_list.pk).exists())
        batch = DiplomaGenerationBatch.objects.get()
        self.assertIsNone(batch.participant_list_id)
        self.assertEqual(batch.participant_list_display_name, "Lista folosită")

    def test_expired_and_foreign_drafts_are_not_viewable(self):
        for owner, expires_at in (
            (self.other_user, timezone.now() + timedelta(hours=1)),
            (self.user, timezone.now() - timedelta(seconds=1)),
        ):
            draft = ParticipantImportDraft.objects.create(
                owner=owner,
                list_name="Draft privat",
                source_file_name="draft.csv",
                valid_rows_json=[],
                invalid_rows_json=[],
                warnings_json=[],
                expires_at=expires_at,
            )
            with self.subTest(owner=owner, expires_at=expires_at):
                response = self.client.get(
                    reverse(
                        "diplome:participant_import_preview",
                        kwargs={"draft_id": draft.pk},
                    )
                )
                self.assertEqual(response.status_code, 404)
```

## `apps/diplome/urls.py`

Size: 3.6 KB

```python
from django.urls import path

from .views import (
    BulkDiplomaGenerationCreateView,
    DiplomaGenerationBatchDetailView,
    DiplomaGenerationBatchResumeView,
    DiplomaGenerationBatchZipDownloadView,
    DiplomaGenerationCreateView,
    DiplomaGenerationDownloadView,
    DiplomaGenerationHistoryView,
    DiplomaGenerationIndexView,
    DiplomaGenerationPreviewView,
    DiplomaTemplateCreateView,
    DiplomaTemplateDeleteView,
    DiplomaTemplateEditorView,
    DiplomaTemplateListView,
    DiplomaTemplatePreviewView,
    ParticipantImportConfirmView,
    ParticipantImportMappingView,
    ParticipantImportPreviewView,
    ParticipantImportSheetView,
    ParticipantImportView,
    ParticipantListDeleteView,
    ParticipantListDetailView,
    ParticipantListView,
)


app_name = "diplome"

urlpatterns = [
    path("generare/", DiplomaGenerationIndexView.as_view(), name="generation_index"),
    path(
        "generare/preview/",
        DiplomaGenerationPreviewView.as_view(),
        name="generation_preview",
    ),
    path(
        "generare/creeaza/",
        DiplomaGenerationCreateView.as_view(),
        name="generation_create",
    ),
    path(
        "generare/lot/",
        BulkDiplomaGenerationCreateView.as_view(),
        name="generation_bulk_create",
    ),
    path(
        "generare/<uuid:generated_diploma_id>/download/",
        DiplomaGenerationDownloadView.as_view(),
        name="generation_download",
    ),
    path("liste/", ParticipantListView.as_view(), name="list_index"),
    path("liste/nou/", ParticipantImportView.as_view(), name="participant_import"),
    path(
        "liste/import/<uuid:draft_id>/foaie/",
        ParticipantImportSheetView.as_view(),
        name="participant_import_sheet",
    ),
    path(
        "liste/import/<uuid:draft_id>/coloane/",
        ParticipantImportMappingView.as_view(),
        name="participant_import_mapping",
    ),
    path(
        "liste/import/<uuid:draft_id>/",
        ParticipantImportPreviewView.as_view(),
        name="participant_import_preview",
    ),
    path(
        "liste/import/<uuid:draft_id>/confirma/",
        ParticipantImportConfirmView.as_view(),
        name="participant_import_confirm",
    ),
    path(
        "liste/<uuid:participant_list_id>/",
        ParticipantListDetailView.as_view(),
        name="participant_list_detail",
    ),
    path(
        "liste/<uuid:participant_list_id>/sterge/",
        ParticipantListDeleteView.as_view(),
        name="participant_list_delete",
    ),
    path("template-uri/", DiplomaTemplateListView.as_view(), name="template_list"),
    path("template-uri/nou/", DiplomaTemplateCreateView.as_view(), name="template_create"),
    path(
        "template-uri/<uuid:template_id>/editor/",
        DiplomaTemplateEditorView.as_view(),
        name="template_editor",
    ),
    path(
        "template-uri/<uuid:template_id>/preview/",
        DiplomaTemplatePreviewView.as_view(),
        name="template_preview",
    ),
    path(
        "template-uri/<uuid:template_id>/sterge/",
        DiplomaTemplateDeleteView.as_view(),
        name="template_delete",
    ),
    path("istoric/", DiplomaGenerationHistoryView.as_view(), name="history_index"),
    path(
        "istoric/<uuid:batch_id>/",
        DiplomaGenerationBatchDetailView.as_view(),
        name="batch_detail",
    ),
    path(
        "istoric/<uuid:batch_id>/zip/",
        DiplomaGenerationBatchZipDownloadView.as_view(),
        name="batch_zip_download",
    ),
    path(
        "istoric/<uuid:batch_id>/reia/",
        DiplomaGenerationBatchResumeView.as_view(),
        name="batch_resume",
    ),
]
```

## `apps/diplome/validators.py`

Size: 20.4 KB

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

## `apps/diplome/views.py`

Size: 26.7 KB

```python
import logging
from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import FormView, ListView, TemplateView

from apps.media_library.selectors import list_owned_media_assets
from apps.media_library.services import require_owned_layout_assets, serialize_media_assets

from .forms import (
    BulkDiplomaGenerationForm,
    DiplomaGenerationSelectionForm,
    DiplomaGenerationHistoryFilterForm,
    DiplomaTemplateCreateForm,
    DiplomaTemplateFilterForm,
    DiplomaTemplateLayoutForm,
    ParticipantColumnMappingForm,
    ParticipantListImportForm,
    ParticipantSheetSelectionForm,
)
from .selectors import (
    get_owned_generation_batch,
    get_owned_import_draft,
    get_owned_participant_list,
    get_owned_template,
    list_owned_participants,
    list_owned_participant_lists,
    list_generated_diplomas_for_batch,
    list_owned_template_categories,
    list_owned_templates,
)
from .services import (
    apply_participant_import_mapping,
    build_batch_zip_response,
    build_diploma_preview_context,
    build_generation_history_context,
    build_generated_diploma_filename,
    build_preview_data,
    confirm_participant_import,
    create_diploma_template,
    create_participant_import_draft,
    delete_diploma_template,
    delete_participant_list,
    generate_single_diploma,
    generate_diploma_batch,
    get_generated_diploma_download,
    resume_generation_batch,
    select_participant_import_sheet,
    update_diploma_template_layout,
)


logger = logging.getLogger(__name__)


DRAFT_TEMPLATE_IDS_SESSION_KEY = "diplome_draft_template_ids"


def _is_htmx(request) -> bool:
    return request.headers.get("HX-Request") == "true"


class HtmxPartialMixin:
    partial_template_name = ""

    def render_to_response(self, context, **response_kwargs):
        if _is_htmx(self.request) and self.partial_template_name:
            response_kwargs.setdefault("content_type", self.content_type)
            return self.response_class(
                request=self.request,
                template=self.partial_template_name,
                context=context,
                using=self.template_engine,
                **response_kwargs,
            )
        return super().render_to_response(context, **response_kwargs)


def _draft_template_ids(request) -> list[str]:
    return list(request.session.get(DRAFT_TEMPLATE_IDS_SESSION_KEY, []))


def _is_draft_template(request, template_id) -> bool:
    return str(template_id) in _draft_template_ids(request)


def _mark_draft_template(request, template_id) -> None:
    template_id = str(template_id)
    draft_ids = _draft_template_ids(request)
    if template_id not in draft_ids:
        draft_ids.append(template_id)
        request.session[DRAFT_TEMPLATE_IDS_SESSION_KEY] = draft_ids


def _clear_draft_template(request, template_id) -> None:
    template_id = str(template_id)
    draft_ids = [item for item in _draft_template_ids(request) if item != template_id]
    if draft_ids:
        request.session[DRAFT_TEMPLATE_IDS_SESSION_KEY] = draft_ids
    else:
        request.session.pop(DRAFT_TEMPLATE_IDS_SESSION_KEY, None)


class DiplomaTemplateListView(HtmxPartialMixin, LoginRequiredMixin, ListView):
    template_name = "diplome/template_list.html"
    partial_template_name = "diplome/includes/template_list_panel.html"
    context_object_name = "templates"

    def get_filter_form(self):
        if not hasattr(self, "_filter_form"):
            categories = list_owned_template_categories(user=self.request.user)
            self._filter_form = DiplomaTemplateFilterForm(
                data=self.request.GET,
                categories=categories,
            )
        return self._filter_form

    def get_queryset(self):
        form = self.get_filter_form()
        category = form.cleaned_data["category"] if form.is_valid() else ""
        self.selected_category = category
        return list_owned_templates(user=self.request.user, category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "filter_form": self.get_filter_form(),
            "selected_category": getattr(self, "selected_category", ""),
        })
        return context


def _generation_index_context(form, bulk_form):
    return {
        "form": form,
        "bulk_form": bulk_form,
        "selected_participant_id": str(form["participant"].value() or ""),
        "has_participant_lists": form.fields["participant_list"].queryset.exists(),
        "has_templates": form.fields["template"].queryset.exists(),
    }


def _add_batch_result_message(request, batch):
    message = (
        f"Lot finalizat: {batch.success_count} din {batch.total_count} "
        f"diplome generate, {batch.failed_count} eșuate."
    )
    if batch.status == batch.Status.COMPLETED:
        messages.success(request, message)
    elif batch.status == batch.Status.COMPLETED_WITH_ERRORS:
        messages.warning(request, message)
    else:
        messages.error(request, message)


class DiplomaGenerationIndexView(LoginRequiredMixin, FormView):
    template_name = "diplome/generation_index.html"
    form_class = DiplomaGenerationSelectionForm

    def get_initial(self):
        initial = super().get_initial()
        for field_name in ("participant_list", "participant", "template"):
            value = self.request.GET.get(field_name)
            if value:
                initial[field_name] = value
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bulk_form = kwargs.get("bulk_form") or BulkDiplomaGenerationForm(
            user=self.request.user
        )
        context.update(_generation_index_context(context["form"], bulk_form))
        return context

    def form_valid(self, form):
        query = urlencode(
            {
                "participant_list": form.cleaned_data["participant_list"].pk,
                "participant": form.cleaned_data["participant"].pk,
                "template": form.cleaned_data["template"].pk,
            }
        )
        return redirect(f"{reverse('diplome:generation_preview')}?{query}")


class DiplomaGenerationPreviewView(LoginRequiredMixin, TemplateView):
    template_name = "diplome/generation_preview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selection = {
            "participant_list_id": self.request.GET.get("participant_list"),
            "participant_id": self.request.GET.get("participant"),
            "template_id": self.request.GET.get("template"),
        }
        if not all(selection.values()):
            raise Http404("Selecția pentru previzualizare este incompletă.")
        context.update(
            build_diploma_preview_context(owner=self.request.user, **selection)
        )
        context["selection_query"] = urlencode(
            {
                "participant_list": context["participant_list"].pk,
                "participant": context["participant"].pk,
                "template": context["diploma_template"].pk,
            }
        )
        generated_id = self.request.GET.get("generated")
        if generated_id:
            generated = get_generated_diploma_download(
                owner=self.request.user,
                generated_diploma_id=generated_id,
            )
            if (
                generated.participant_list_id
                != context["participant_list"].pk
                or generated.participant_id != context["participant"].pk
                or generated.template_id != context["diploma_template"].pk
            ):
                raise Http404("Fișierul generat nu corespunde selecției curente.")
            context["generated_diploma"] = generated
        return context


class DiplomaGenerationCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = DiplomaGenerationSelectionForm(request.POST, user=request.user)
        if not form.is_valid():
            return render(
                request,
                "diplome/generation_index.html",
                _generation_index_context(
                    form,
                    BulkDiplomaGenerationForm(user=request.user),
                ),
                status=400,
            )
        generated = generate_single_diploma(
            owner=request.user,
            participant_list_id=form.cleaned_data["participant_list"].pk,
            participant_id=form.cleaned_data["participant"].pk,
            template_id=form.cleaned_data["template"].pk,
        )
        query = urlencode(
            {
                "participant_list": generated.participant_list_id,
                "participant": generated.participant_id,
                "template": generated.template_id,
                "generated": generated.pk,
            }
        )
        return redirect(f"{reverse('diplome:generation_preview')}?{query}")


class DiplomaGenerationDownloadView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        generated = get_generated_diploma_download(
            owner=request.user,
            generated_diploma_id=kwargs["generated_diploma_id"],
        )
        try:
            if not generated.pdf_file.name or not generated.pdf_file.storage.exists(
                generated.pdf_file.name
            ):
                raise Http404("Fișierul PDF nu mai este disponibil.")
            pdf_file = generated.pdf_file.open("rb")
        except (OSError, ValueError) as exc:
            raise Http404("Fișierul PDF nu mai este disponibil.") from exc
        return FileResponse(
            pdf_file,
            as_attachment=True,
            filename=build_generated_diploma_filename(generated),
            content_type="application/pdf",
        )


class BulkDiplomaGenerationCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = BulkDiplomaGenerationForm(request.POST, user=request.user)
        if not form.is_valid():
            return render(
                request,
                "diplome/generation_index.html",
                _generation_index_context(
                    DiplomaGenerationSelectionForm(user=request.user),
                    form,
                ),
                status=400,
            )
        try:
            batch = generate_diploma_batch(
                request.user,
                form.cleaned_data["participant_list"].pk,
                form.cleaned_data["template"].pk,
            )
        except ValidationError as exc:
            form.add_error(None, exc)
            return render(
                request,
                "diplome/generation_index.html",
                _generation_index_context(
                    DiplomaGenerationSelectionForm(user=request.user),
                    form,
                ),
                status=400,
            )
        _add_batch_result_message(request, batch)
        return redirect("diplome:batch_detail", batch_id=batch.pk)


class DiplomaGenerationHistoryView(HtmxPartialMixin, LoginRequiredMixin, TemplateView):
    template_name = "diplome/history_index.html"
    partial_template_name = "diplome/includes/history_panel.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter_form = DiplomaGenerationHistoryFilterForm(
            self.request.GET,
            user=self.request.user,
        )
        filters = filter_form.cleaned_data if filter_form.is_valid() else {}
        context.update(build_generation_history_context(self.request.user, filters))
        context["filter_form"] = filter_form
        return context


class DiplomaGenerationBatchDetailView(HtmxPartialMixin, LoginRequiredMixin, TemplateView):
    template_name = "diplome/batch_detail.html"
    partial_template_name = "diplome/includes/batch_detail_panel.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        batch = get_owned_generation_batch(
            self.request.user,
            kwargs["batch_id"],
        )
        context.update(
            {
                "batch": batch,
                "generated_diplomas": list_generated_diplomas_for_batch(
                    self.request.user,
                    batch.pk,
                ),
            }
        )
        return context


class DiplomaGenerationBatchResumeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        batch_id = kwargs["batch_id"]
        try:
            batch = resume_generation_batch(request.user, batch_id)
        except Http404:
            raise
        except ValidationError as exc:
            messages.error(request, " ".join(exc.messages))
        except Exception:
            logger.exception(
                "Could not resume diploma generation batch %s",
                batch_id,
            )
            messages.error(
                request,
                "Generarea lotului nu a putut fi reluată.",
            )
        else:
            _add_batch_result_message(request, batch)
        if _is_htmx(request):
            target = request.headers.get("HX-Target", "")
            if target == "history-panel":
                filter_form = DiplomaGenerationHistoryFilterForm(
                    request.GET,
                    user=request.user,
                )
                filters = filter_form.cleaned_data if filter_form.is_valid() else {}
                context = build_generation_history_context(request.user, filters)
                context["filter_form"] = filter_form
                return render(
                    request,
                    "diplome/includes/history_panel.html",
                    context,
                )
            batch = get_owned_generation_batch(request.user, batch_id)
            return render(
                request,
                "diplome/includes/batch_detail_panel.html",
                {
                    "batch": batch,
                    "generated_diplomas": list_generated_diplomas_for_batch(
                        request.user,
                        batch.pk,
                    ),
                },
            )
        return redirect("diplome:batch_detail", batch_id=batch_id)


class DiplomaGenerationBatchZipDownloadView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return build_batch_zip_response(request.user, kwargs["batch_id"])


class DiplomaTemplateCreateView(LoginRequiredMixin, FormView):
    template_name = "diplome/template_form.html"
    form_class = DiplomaTemplateCreateForm

    def form_valid(self, form):
        template = create_diploma_template(owner=self.request.user, data=form.cleaned_data)
        _mark_draft_template(self.request, template.pk)
        return redirect("diplome:template_editor", template_id=template.pk)


class DiplomaTemplateEditorView(LoginRequiredMixin, TemplateView):
    template_name = "diplome/template_editor.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        template = get_owned_template(
            user=self.request.user,
            template_id=self.kwargs["template_id"],
        )
        context.update({
            "diploma_template": template,
            "layout": template.layout_json,
            "media_assets": serialize_media_assets(
                list_owned_media_assets(user=self.request.user)
            ),
            "media_assets_api_url": reverse("media_library:api_assets"),
            "media_assets_upload_url": reverse("media_library:api_upload"),
            "is_draft_template": _is_draft_template(self.request, template.pk),
        })
        return context

    def post(self, request, *args, **kwargs):
        get_owned_template(user=request.user, template_id=kwargs["template_id"])
        form = DiplomaTemplateLayoutForm(request.POST)
        if not form.is_valid():
            return JsonResponse(
                {"success": False, "errors": form.errors.get_json_data()},
                status=400,
            )
        try:
            template = update_diploma_template_layout(
                owner=request.user,
                template_id=kwargs["template_id"],
                layout=form.cleaned_data["layout_json"],
            )
        except ValidationError as exc:
            return JsonResponse(
                {
                    "success": False,
                    "errors": {
                        "layout_json": [
                            {"message": message, "code": "invalid_asset"}
                            for message in exc.messages
                        ]
                    },
                },
                status=400,
            )
        if template.layout_json["elements"]:
            _clear_draft_template(request, template.pk)
        return JsonResponse({
            "success": True,
            "message": "Template salvat.",
            "updatedAt": template.updated_at.isoformat(),
            "isDraft": _is_draft_template(request, template.pk),
        })


class DiplomaTemplatePreviewView(LoginRequiredMixin, TemplateView):
    template_name = "diplome/template_preview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        template = get_owned_template(
            user=self.request.user,
            template_id=self.kwargs["template_id"],
        )
        context.update({
            "diploma_template": template,
            "layout": template.layout_json,
            "sample_participant": build_preview_data(),
            "media_assets": serialize_media_assets(
                require_owned_layout_assets(
                    owner=self.request.user,
                    layout=template.layout_json,
                ).values()
            ),
        })
        return context


class DiplomaTemplateDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        template_id = kwargs["template_id"]
        delete_diploma_template(
            owner=request.user,
            template_id=template_id,
        )
        _clear_draft_template(request, template_id)
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": True})
        messages.success(request, "Template-ul a fost șters.")
        if _is_htmx(request):
            view = DiplomaTemplateListView()
            view.setup(request)
            view.object_list = view.get_queryset()
            return render(
                request,
                "diplome/includes/template_list_panel.html",
                view.get_context_data(),
            )
        return redirect("diplome:template_list")


class ParticipantListView(HtmxPartialMixin, LoginRequiredMixin, ListView):
    template_name = "diplome/participant_list.html"
    partial_template_name = "diplome/includes/participant_list_panel.html"
    context_object_name = "participant_lists"
    paginate_by = 50

    def get_queryset(self):
        return list_owned_participant_lists(user=self.request.user)


class ParticipantImportView(LoginRequiredMixin, FormView):
    template_name = "diplome/participant_import.html"
    form_class = ParticipantListImportForm

    def form_valid(self, form):
        try:
            draft = create_participant_import_draft(
                owner=self.request.user,
                data=form.cleaned_data,
            )
        except ValidationError as exc:
            form.add_error("source_file", exc)
            return self.form_invalid(form)
        if draft.source_sheets_json:
            return redirect("diplome:participant_import_sheet", draft_id=draft.pk)
        return redirect("diplome:participant_import_mapping", draft_id=draft.pk)


class ParticipantImportSheetView(LoginRequiredMixin, FormView):
    template_name = "diplome/participant_import_sheet.html"
    form_class = ParticipantSheetSelectionForm

    def get_draft(self):
        if not hasattr(self, "_draft"):
            self._draft = get_owned_import_draft(
                user=self.request.user,
                draft_id=self.kwargs["draft_id"],
            )
        return self._draft

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["sheets"] = self.get_draft().source_sheets_json
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["draft"] = self.get_draft()
        return context

    def form_valid(self, form):
        try:
            draft = select_participant_import_sheet(
                owner=self.request.user,
                draft_id=self.kwargs["draft_id"],
                sheet_index=form.selected_index(),
            )
        except ValidationError as exc:
            form.add_error("sheet_index", exc)
            return self.form_invalid(form)
        return redirect("diplome:participant_import_mapping", draft_id=draft.pk)


class ParticipantImportMappingView(LoginRequiredMixin, FormView):
    template_name = "diplome/participant_import_mapping.html"
    form_class = ParticipantColumnMappingForm

    def get_draft(self):
        if not hasattr(self, "_draft"):
            self._draft = get_owned_import_draft(
                user=self.request.user,
                draft_id=self.kwargs["draft_id"],
            )
        return self._draft

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        draft = self.get_draft()
        kwargs.update(
            {
                "columns": draft.source_columns_json,
                "suggested_mapping": draft.column_mapping_json,
            }
        )
        return kwargs

    def get(self, request, *args, **kwargs):
        draft = self.get_draft()
        if draft.source_sheets_json and not draft.source_columns_json:
            return redirect("diplome:participant_import_sheet", draft_id=draft.pk)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        draft = self.get_draft()
        form = context["form"]
        context.update(
            {
                "draft": draft,
                "mapping_rows": [
                    {
                        "column": column,
                        "field": form[f"column_{column['index']}"],
                    }
                    for column in draft.source_columns_json
                ],
            }
        )
        return context

    def form_valid(self, form):
        try:
            draft = apply_participant_import_mapping(
                owner=self.request.user,
                draft_id=self.kwargs["draft_id"],
                column_mapping=form.get_column_mapping(),
            )
        except ValidationError as exc:
            form.add_error(None, exc)
            return self.form_invalid(form)
        return redirect("diplome:participant_import_preview", draft_id=draft.pk)


class ParticipantImportPreviewView(LoginRequiredMixin, TemplateView):
    template_name = "diplome/participant_import_preview.html"

    def get(self, request, *args, **kwargs):
        draft = get_owned_import_draft(
            user=request.user,
            draft_id=kwargs["draft_id"],
        )
        if not draft.mapping_confirmed:
            return redirect("diplome:participant_import_mapping", draft_id=draft.pk)
        self._draft = draft
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["draft"] = self._draft
        return context


class ParticipantImportConfirmView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            participant_list = confirm_participant_import(
                owner=request.user,
                draft_id=kwargs["draft_id"],
            )
        except ValidationError as exc:
            messages.error(request, "; ".join(exc.messages))
            return redirect(
                "diplome:participant_import_preview",
                draft_id=kwargs["draft_id"],
            )
        messages.success(request, "Lista de participanți a fost importată.")
        return redirect(
            "diplome:participant_list_detail",
            participant_list_id=participant_list.pk,
        )


class ParticipantListDetailView(HtmxPartialMixin, LoginRequiredMixin, TemplateView):
    template_name = "diplome/participant_list_detail.html"
    partial_template_name = "diplome/includes/participant_list_detail_panel.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        participant_list = get_owned_participant_list(
            user=self.request.user,
            participant_list_id=self.kwargs["participant_list_id"],
        )
        paginator = Paginator(
            list_owned_participants(
                user=self.request.user,
                participant_list=participant_list,
            ),
            100,
        )
        page_obj = paginator.get_page(self.request.GET.get("page"))
        context.update(
            {
                "participant_list": participant_list,
                "participants": page_obj.object_list,
                "page_obj": page_obj,
                "is_paginated": page_obj.has_other_pages(),
            }
        )
        return context


class ParticipantListDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        delete_participant_list(
            owner=request.user,
            participant_list_id=kwargs["participant_list_id"],
        )
        messages.success(request, "Lista de participanți a fost ștearsă.")
        if _is_htmx(request):
            view = ParticipantListView()
            view.setup(request)
            view.object_list = view.get_queryset()
            return render(
                request,
                "diplome/includes/participant_list_panel.html",
                view.get_context_data(object_list=view.object_list),
            )
        return redirect("diplome:list_index")


class DiplomaPlaceholderView(LoginRequiredMixin, TemplateView):
    template_name = "diplome/placeholder.html"
    page_title = "Diplome"
    page_description = "Această secțiune va fi disponibilă într-o etapă viitoare."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "page_title": self.page_title,
            "page_description": self.page_description,
        })
        return context
```

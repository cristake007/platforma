# apps/flota/forms.py

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `apps/flota/forms.py`
- App: `flota`
- App guide: `codex-context/apps/flota.md`
- Role: `backend`
- Size: 5215 bytes
- Source SHA-256: `51d74e51d471e04212aacce61456c9f888ade5d4288934f713ae887b34e54c1a`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```python
from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Q

from .models import MaintenanceRecord, MaintenanceType, Vehicle


INPUT_CLASS = "input input-bordered input-sm w-full"
SELECT_CLASS = "select select-bordered select-sm w-full"
TEXTAREA_CLASS = "textarea textarea-bordered min-h-28 w-full"


class VehicleForm(forms.ModelForm):
    assignee = forms.ModelChoiceField(
        queryset=get_user_model().objects.none(),
        required=False,
        label="Responsabil",
        empty_label="Neatribuit",
        widget=forms.Select(attrs={"class": SELECT_CLASS}),
    )

    class Meta:
        model = Vehicle
        fields = (
            "registration_number",
            "vin",
            "brand",
            "model",
            "manufacture_year",
            "current_mileage",
            "emblem",
            "status",
        )
        labels = {
            "registration_number": "Număr de înmatriculare",
            "vin": "VIN",
            "brand": "Marcă",
            "model": "Model",
            "manufacture_year": "An fabricație",
            "current_mileage": "Kilometraj curent",
            "emblem": "Emblemă marcă",
            "status": "Status operațional",
        }
        help_texts = {
            "vin": "Opțional. 17 caractere, fără I, O sau Q.",
            "emblem": "JPEG, PNG sau WebP, maximum 2 MB.",
        }
        widgets = {
            "registration_number": forms.TextInput(attrs={"class": INPUT_CLASS, "autofocus": True}),
            "vin": forms.TextInput(attrs={"class": INPUT_CLASS, "maxlength": 17}),
            "brand": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "model": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "manufacture_year": forms.NumberInput(attrs={"class": INPUT_CLASS, "min": 1886}),
            "current_mileage": forms.NumberInput(attrs={"class": INPUT_CLASS, "min": 0}),
            "emblem": forms.ClearableFileInput(
                attrs={"class": "file-input file-input-bordered file-input-sm w-full", "accept": ".jpg,.jpeg,.png,.webp,image/jpeg,image/png,image/webp"}
            ),
            "status": forms.Select(attrs={"class": SELECT_CLASS}),
        }

    def __init__(self, *args, current_assignment=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["assignee"].queryset = get_user_model().objects.filter(is_active=True).order_by(
            "first_name", "last_name", "username"
        )
        if current_assignment and not self.is_bound:
            self.initial["assignee"] = current_assignment.assignee_id


class MaintenanceRecordForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRecord
        fields = ("maintenance_type", "completed_on", "next_due_on", "mileage", "provider", "cost", "notes")
        labels = {
            "maintenance_type": "Tip mentenanță",
            "completed_on": "Efectuat la",
            "next_due_on": "Următorul termen",
            "mileage": "Kilometraj",
            "provider": "Furnizor",
            "cost": "Cost (lei)",
            "notes": "Observații",
        }
        widgets = {
            "maintenance_type": forms.Select(attrs={"class": SELECT_CLASS}),
            "completed_on": forms.DateInput(attrs={"class": INPUT_CLASS, "type": "date"}),
            "next_due_on": forms.DateInput(attrs={"class": INPUT_CLASS, "type": "date"}),
            "mileage": forms.NumberInput(attrs={"class": INPUT_CLASS, "min": 0}),
            "provider": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "cost": forms.NumberInput(attrs={"class": INPUT_CLASS, "min": 0, "step": "0.01"}),
            "notes": forms.Textarea(attrs={"class": TEXTAREA_CLASS}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        queryset = MaintenanceType.objects.filter(is_active=True)
        if self.instance and self.instance.pk:
            queryset = MaintenanceType.objects.filter(Q(is_active=True) | Q(pk=self.instance.maintenance_type_id))
        self.fields["maintenance_type"].queryset = queryset.order_by("display_order", "name")


class MaintenanceTypeForm(forms.ModelForm):
    class Meta:
        model = MaintenanceType
        fields = ("name", "code", "display_order", "is_active")
        labels = {
            "name": "Denumire",
            "code": "Cod",
            "display_order": "Ordine",
            "is_active": "Activ",
        }
        help_texts = {"code": "Identificator tehnic cu litere mici, cifre, cratimă sau underscore."}
        widgets = {
            "name": forms.TextInput(attrs={"class": INPUT_CLASS, "autofocus": True}),
            "code": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "display_order": forms.NumberInput(attrs={"class": INPUT_CLASS, "min": 0}),
            "is_active": forms.CheckboxInput(attrs={"class": "toggle toggle-primary toggle-sm"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.is_system:
            self.fields["code"].disabled = True
            self.fields["is_active"].disabled = True
```

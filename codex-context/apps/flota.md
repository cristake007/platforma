# Django app: flota

Migrations are excluded by default. Tests are included unless `--no-tests` is used.

## `apps/flota/__init__.py`

Size: 1 B

```python

```

## `apps/flota/admin.py`

Size: 2.2 KB

```python
from django.contrib import admin

from .models import MaintenanceRecord, MaintenanceType, Vehicle, VehicleAssignment


class VehicleAssignmentInline(admin.TabularInline):
    model = VehicleAssignment
    extra = 0
    readonly_fields = ("starts_at", "ends_at", "assigned_by", "ended_by")
    can_delete = False


class MaintenanceRecordInline(admin.TabularInline):
    model = MaintenanceRecord
    extra = 0
    readonly_fields = ("created_by", "created_at", "updated_at")
    can_delete = False


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("registration_number", "brand", "model", "status", "current_mileage", "archived_at")
    list_filter = ("status", "archived_at")
    search_fields = ("registration_number", "vin", "brand", "model")
    inlines = (VehicleAssignmentInline, MaintenanceRecordInline)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(MaintenanceType)
class MaintenanceTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "display_order", "is_active", "is_system")
    list_filter = ("is_active", "is_system")
    search_fields = ("name", "code")

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.is_system:
            return ("code", "is_active", "is_system")
        return ("is_system",)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(VehicleAssignment)
class VehicleAssignmentAdmin(admin.ModelAdmin):
    list_display = ("vehicle", "assignee", "starts_at", "ends_at", "assigned_by")
    list_filter = ("ends_at",)
    search_fields = ("vehicle__registration_number", "assignee__username")
    list_select_related = ("vehicle", "assignee", "assigned_by")

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = ("vehicle", "maintenance_type", "completed_on", "next_due_on", "mileage", "provider")
    list_filter = ("maintenance_type",)
    search_fields = ("vehicle__registration_number", "provider", "notes")
    list_select_related = ("vehicle", "maintenance_type", "created_by")

    def has_delete_permission(self, request, obj=None):
        return False
```

## `apps/flota/AGENTS.md`

Size: 2.6 KB

````markdown
# Flota App Instructions

## Scope

This app owns fleet vehicles, current and historical user assignments, maintenance types, maintenance records, due-state calculations, and the fleet list/detail workflows.

## Read before editing

- Root `AGENTS.md`.
- `coding-standards.md`.
- `frontend.md` for UI/template work.
- This file.
- Only the files for the selected workflow.

Use `codex-context/apps/flota.md` only when a path is unknown.

## Architecture

- Keep request validation in `forms.py`.
- Keep reusable invariants in `validators.py`.
- Keep transactional writes in `services.py`.
- Keep permission-filtered reads in `selectors.py`.
- PostgreSQL is authoritative.
- JavaScript may refresh displayed countdown labels but must not own validation, authorization, or persistence.
- All pages require authentication.
- Staff manage the fleet.
- Non-staff users have read-only access only to currently assigned, non-archived vehicles.
- Return 404 for vehicles outside the current user's visibility.
- Use POST with CSRF for archive, restore, and maintenance-type state changes.
- Archive vehicles and custom maintenance types instead of exposing destructive deletion.
- System maintenance types cannot be archived.

## Domain contracts

- A vehicle has at most one open assignment.
- Assignment changes must go through transactional services so history remains complete.
- Seed and retain the system types ITP, Insurance, Oil change, and Service.
- Custom types are fleet-wide and staff-managed.
- Maintenance deadlines are manual dates.
- `next_due_on` must follow `completed_on`.
- Due states are: valid beyond 30 days, due soon within 30 days, due today, overdue, or not recorded.
- Vehicle emblems are optional JPEG, PNG, or WebP uploads of at most 2 MB.

## Reuse and UI standards

- Reuse existing vehicle, maintenance, assignment, table, message, and action patterns.
- Extend `layouts/base.html` and use shared semantic daisyUI/Tailwind tokens.
- Keep the fleet overview table horizontally scrollable.
- Keep detail layout stacked on narrow screens.
- The four system maintenance types remain the overview columns.
- Custom types appear on vehicle details and contribute to summary deadline counts.
- Keep forms and navigation usable without JavaScript.
- Preserve visible keyboard focus.
- Use sharp bordered operational panels instead of decorative rounded cards.

## Focused checks

```powershell
python manage.py test apps.flota
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py tailwind build
```
````

## `apps/flota/apps.py`

Size: 148 B

```python
from django.apps import AppConfig


class FlotaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.flota"

```

## `apps/flota/forms.py`

Size: 5.1 KB

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

## `apps/flota/IMPLEMENTATION_PLAN.md`

Size: 2.0 KB

```markdown
# Flota - Phased Implementation Plan

## Phase 1 - Scaffold and Instructions

- Create the Django app package, namespaced URLs, templates, static files, migrations, tests, admin registration, and app instructions.
- Register the app at `/flota/`, add it to Operations navigation, and register its templates and scripts as Tailwind sources.
- Require authentication throughout.

## Phase 2 - Persistence

- Add persistent vehicles, assignment intervals, maintenance types, and maintenance records.
- Seed protected system types for ITP, insurance, oil changes, and service while permitting staff-managed custom types.
- Normalize vehicle identifiers, validate dates and uploads, and preserve all records through archival.

## Phase 3 - Services, Selectors, and Permissions

- Keep transactional writes in services and visibility-filtered reads in selectors.
- Allow staff to manage all records and assigned users to view only their current vehicles.
- Derive deadline states from the latest record for every maintenance type using a 30-day warning window.

## Phase 4 - Routes and Forms

- Add fleet list, vehicle create/detail/edit/archive/restore, nested maintenance create/edit, and maintenance-type management routes.
- Use server-validated multipart forms and POST/CSRF for all state changes.

## Phase 5 - User Interface

- Implement the approved compact fleet table and vehicle detail concept in the shared TUVTK shell.
- Include summary counts, filters, pagination, core deadline columns, complete service history, and assignment history.
- Use minimal progressive enhancement only for deadline label refresh.

## Phase 6 - Tests and Verification

- Test persistence, validation, assignment history, permissions, filtering, due-state boundaries, archival, forms, and responsive rendering.
- Run the focused Django checks, Tailwind build, browser QA against the approved concept, and context regeneration.

## Deferred Scope

- Notifications, email, scheduled jobs, recurring intervals, document attachments, fuel tracking, expense reporting, and permanent deletion.

```

## `apps/flota/models.py`

Size: 7.5 KB

```python
import uuid
import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q
from django.db.models.functions import Lower
from django.utils import timezone

from .validators import (
    normalize_registration_number,
    normalize_vin,
    validate_emblem,
    validate_maintenance_dates,
    validate_manufacture_year,
    validate_registration_number,
    validate_vin,
)


class Vehicle(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Activ"
        MAINTENANCE = "maintenance", "În mentenanță"
        OUT_OF_SERVICE = "out_of_service", "Indisponibil"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    registration_number = models.CharField(max_length=20, validators=[validate_registration_number])
    vin = models.CharField(max_length=17, blank=True, validators=[validate_vin])
    brand = models.CharField(max_length=80)
    model = models.CharField(max_length=80)
    manufacture_year = models.PositiveSmallIntegerField(blank=True, null=True, validators=[validate_manufacture_year])
    current_mileage = models.PositiveIntegerField(default=0)
    emblem = models.ImageField(upload_to="flota/emblems/%Y/%m/", blank=True, validators=[validate_emblem])
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE, db_index=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_fleet_vehicles",
    )
    archived_at = models.DateTimeField(blank=True, null=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("brand", "model", "registration_number")
        constraints = [
            models.UniqueConstraint(
                Lower("registration_number"),
                name="flota_unique_registration_ci",
            ),
            models.UniqueConstraint(
                Lower("vin"),
                condition=~Q(vin=""),
                name="flota_unique_vin_ci",
            ),
        ]

    def clean(self):
        self.registration_number = normalize_registration_number(self.registration_number)
        self.vin = normalize_vin(self.vin)
        validate_registration_number(self.registration_number)
        validate_vin(self.vin)
        validate_manufacture_year(self.manufacture_year)

    def save(self, *args, **kwargs):
        self.registration_number = normalize_registration_number(self.registration_number)
        self.vin = normalize_vin(self.vin)
        super().save(*args, **kwargs)

    @property
    def is_archived(self):
        return self.archived_at is not None

    @property
    def registration_display(self):
        value = self.registration_number
        match = re.fullmatch(r"([A-Z]{1,2})(\d{2,3})([A-Z]{3})", value)
        return " ".join(match.groups()) if match else value

    def __str__(self):
        return f"{self.brand} {self.model} ({self.registration_display})"


class MaintenanceType(models.Model):
    code = models.SlugField(max_length=50, unique=True)
    name = models.CharField(max_length=80)
    display_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True, db_index=True)
    is_system = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("display_order", "name")
        constraints = [
            models.UniqueConstraint(Lower("name"), name="flota_unique_maintenance_name_ci"),
        ]

    def clean(self):
        self.code = self.code.strip().lower()
        self.name = " ".join(self.name.split())
        if self.is_system and not self.is_active:
            raise ValidationError({"is_active": "Tipurile de sistem nu pot fi dezactivate."})

    def save(self, *args, **kwargs):
        self.code = self.code.strip().lower()
        self.name = " ".join(self.name.split())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class VehicleAssignment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="assignments")
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="fleet_assignments",
    )
    starts_at = models.DateTimeField(default=timezone.now)
    ends_at = models.DateTimeField(blank=True, null=True, db_index=True)
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="fleet_assignments_created",
    )
    ended_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="fleet_assignments_ended",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-starts_at",)
        constraints = [
            models.UniqueConstraint(
                fields=("vehicle",),
                condition=Q(ends_at__isnull=True),
                name="flota_one_open_assignment",
            ),
            models.CheckConstraint(
                condition=Q(ends_at__isnull=True) | Q(ends_at__gte=F("starts_at")),
                name="flota_assignment_ends_after_start",
            ),
        ]

    def clean(self):
        if not self.assignee.is_active:
            raise ValidationError({"assignee": "Vehiculul poate fi atribuit doar unui utilizator activ."})
        if self.ends_at and self.ends_at < self.starts_at:
            raise ValidationError({"ends_at": "Data încheierii nu poate preceda atribuirea."})

    def __str__(self):
        return f"{self.vehicle} - {self.assignee}"


class MaintenanceRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="maintenance_records")
    maintenance_type = models.ForeignKey(
        MaintenanceType,
        on_delete=models.PROTECT,
        related_name="records",
    )
    completed_on = models.DateField()
    next_due_on = models.DateField(db_index=True)
    mileage = models.PositiveIntegerField(blank=True, null=True)
    provider = models.CharField(max_length=160, blank=True)
    cost = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_fleet_maintenance_records",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-completed_on", "-created_at")
        constraints = [
            models.CheckConstraint(
                condition=Q(next_due_on__gt=F("completed_on")),
                name="flota_due_after_completed",
            ),
        ]
        indexes = [
            models.Index(
                fields=("vehicle", "maintenance_type", "-completed_on"),
                name="flota_record_latest_idx",
            ),
        ]

    def clean(self):
        validate_maintenance_dates(self.completed_on, self.next_due_on)

    def __str__(self):
        return f"{self.vehicle} - {self.maintenance_type} - {self.completed_on}"
```

## `apps/flota/selectors.py`

Size: 7.2 KB

```python
from dataclasses import dataclass
from datetime import date

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import Http404
from django.utils import timezone

from .models import MaintenanceRecord, MaintenanceType, Vehicle, VehicleAssignment
from .validators import normalize_registration_number


CORE_MAINTENANCE_CODES = ("itp", "insurance", "oil_change", "service")


@dataclass(frozen=True)
class DeadlineState:
    code: str
    label: str
    tone: str
    days: int | None


def deadline_state(due_on, *, today=None) -> DeadlineState:
    if not due_on:
        return DeadlineState("missing", "Neînregistrat", "neutral", None)
    today = today or timezone.localdate()
    days = (due_on - today).days
    if days < 0:
        elapsed = abs(days)
        return DeadlineState("overdue", f"Expirat de {elapsed} {'zi' if elapsed == 1 else 'zile'}", "error", days)
    if days == 0:
        return DeadlineState("today", "Scadent astăzi", "error", 0)
    if days <= 30:
        return DeadlineState("due_soon", f"Scadent în {days} {'zi' if days == 1 else 'zile'}", "warning", days)
    return DeadlineState("valid", "Valabil", "success", days)


def visible_vehicles(*, user, include_archived=False):
    queryset = Vehicle.objects.select_related("created_by")
    if user.is_staff:
        return queryset.filter(archived_at__isnull=not include_archived)
    return queryset.filter(
        archived_at__isnull=True,
        assignments__assignee=user,
        assignments__ends_at__isnull=True,
    ).distinct()


def get_visible_vehicle(*, user, vehicle_id) -> Vehicle:
    try:
        if user.is_staff:
            return Vehicle.objects.get(pk=vehicle_id)
        return visible_vehicles(user=user).get(pk=vehicle_id)
    except Vehicle.DoesNotExist as exc:
        raise Http404 from exc


def get_staff_vehicle(*, vehicle_id) -> Vehicle:
    try:
        return Vehicle.objects.get(pk=vehicle_id)
    except Vehicle.DoesNotExist as exc:
        raise Http404 from exc


def active_users():
    return get_user_model().objects.filter(is_active=True).order_by("first_name", "last_name", "username")


def maintenance_types(*, include_inactive=False):
    queryset = MaintenanceType.objects.all()
    return queryset if include_inactive else queryset.filter(is_active=True)


def core_maintenance_types():
    types = {item.code: item for item in MaintenanceType.objects.filter(code__in=CORE_MAINTENANCE_CODES)}
    return [types[code] for code in CORE_MAINTENANCE_CODES if code in types]


def _latest_records(*, vehicle_ids, type_ids=None):
    queryset = MaintenanceRecord.objects.filter(vehicle_id__in=vehicle_ids).select_related("maintenance_type")
    if type_ids is not None:
        queryset = queryset.filter(maintenance_type_id__in=type_ids)
    latest = {}
    for record in queryset.order_by("vehicle_id", "maintenance_type_id", "-completed_on", "-created_at"):
        latest.setdefault((record.vehicle_id, record.maintenance_type_id), record)
    return latest


def decorate_vehicle_rows(vehicles, *, types=None):
    vehicles = list(vehicles)
    if not vehicles:
        return vehicles
    vehicle_ids = [vehicle.pk for vehicle in vehicles]
    assignments = {
        assignment.vehicle_id: assignment
        for assignment in VehicleAssignment.objects.filter(
            vehicle_id__in=vehicle_ids,
            ends_at__isnull=True,
        ).select_related("assignee")
    }
    types = list(types or core_maintenance_types())
    latest = _latest_records(vehicle_ids=vehicle_ids, type_ids=[item.pk for item in types])
    for vehicle in vehicles:
        vehicle.current_assignment = assignments.get(vehicle.pk)
        vehicle.deadline_cells = []
        for maintenance_type in types:
            record = latest.get((vehicle.pk, maintenance_type.pk))
            vehicle.deadline_cells.append(
                {
                    "type": maintenance_type,
                    "record": record,
                    "state": deadline_state(record.next_due_on if record else None),
                }
            )
    return vehicles


def vehicle_deadline_rows(vehicle: Vehicle):
    types = list(MaintenanceType.objects.filter(Q(is_active=True) | Q(records__vehicle=vehicle)).distinct())
    latest = _latest_records(vehicle_ids=[vehicle.pk], type_ids=[item.pk for item in types])
    return [
        {
            "type": maintenance_type,
            "record": latest.get((vehicle.pk, maintenance_type.pk)),
            "state": deadline_state(
                latest[(vehicle.pk, maintenance_type.pk)].next_due_on
                if (vehicle.pk, maintenance_type.pk) in latest
                else None
            ),
        }
        for maintenance_type in types
    ]


def fleet_summary(*, queryset=None):
    active_queryset = queryset if queryset is not None else Vehicle.objects.all()
    active_ids = list(active_queryset.filter(archived_at__isnull=True).values_list("pk", flat=True))
    active_type_ids = list(MaintenanceType.objects.filter(is_active=True).values_list("pk", flat=True))
    latest = _latest_records(vehicle_ids=active_ids, type_ids=active_type_ids)
    due_soon = set()
    overdue = set()
    for (vehicle_id, _), record in latest.items():
        state = deadline_state(record.next_due_on)
        if state.code == "due_soon":
            due_soon.add(vehicle_id)
        elif state.code in {"today", "overdue"}:
            overdue.add(vehicle_id)
    return {
        "total": len(active_ids),
        "due_soon": len(due_soon),
        "overdue": len(overdue),
        "archived": active_queryset.filter(archived_at__isnull=False).count(),
    }


def filter_vehicles(queryset, params):
    query = (params.get("q") or "").strip()
    if query:
        normalized = normalize_registration_number(query)
        criteria = Q(brand__icontains=query) | Q(model__icontains=query) | Q(vin__icontains=query)
        if normalized:
            criteria |= Q(registration_number__icontains=normalized)
        queryset = queryset.filter(criteria)
    status = params.get("status")
    if status in Vehicle.Status.values:
        queryset = queryset.filter(status=status)
    assignee = params.get("assignee")
    if assignee:
        queryset = queryset.filter(assignments__assignee_id=assignee, assignments__ends_at__isnull=True)
    deadline = params.get("deadline")
    if deadline in {"valid", "due_soon", "overdue", "missing"}:
        ids = list(queryset.values_list("pk", flat=True))
        active_type_ids = list(MaintenanceType.objects.filter(is_active=True).values_list("pk", flat=True))
        latest = _latest_records(vehicle_ids=ids, type_ids=active_type_ids)
        states_by_vehicle = {vehicle_id: [] for vehicle_id in ids}
        for (vehicle_id, _), record in latest.items():
            states_by_vehicle[vehicle_id].append(deadline_state(record.next_due_on).code)
        selected = []
        for vehicle_id, states in states_by_vehicle.items():
            if deadline == "overdue" and any(state in {"today", "overdue"} for state in states):
                selected.append(vehicle_id)
            elif deadline == "missing" and len(states) < len(active_type_ids):
                selected.append(vehicle_id)
            elif deadline in states:
                selected.append(vehicle_id)
        queryset = queryset.filter(pk__in=selected)
    return queryset.distinct()
```

## `apps/flota/services.py`

Size: 6.4 KB

```python
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.utils import timezone

from .models import MaintenanceRecord, MaintenanceType, Vehicle, VehicleAssignment


VEHICLE_FIELDS = (
    "registration_number",
    "vin",
    "brand",
    "model",
    "manufacture_year",
    "current_mileage",
    "emblem",
    "status",
)


def require_staff(actor) -> None:
    if not actor.is_authenticated or not actor.is_staff:
        raise PermissionDenied("Doar personalul autorizat poate modifica flota.")


def _vehicle_values(data) -> dict:
    values = {field: data.get(field) for field in VEHICLE_FIELDS}
    if values["emblem"] is False:
        values["emblem"] = None
    return values


@transaction.atomic
def set_vehicle_assignment(*, actor, vehicle: Vehicle, assignee) -> VehicleAssignment | None:
    require_staff(actor)
    locked_vehicle = Vehicle.objects.select_for_update().get(pk=vehicle.pk)
    current = (
        VehicleAssignment.objects.select_for_update()
        .filter(vehicle=locked_vehicle, ends_at__isnull=True)
        .select_related("assignee")
        .first()
    )
    if current and assignee and current.assignee_id == assignee.pk:
        return current
    now = timezone.now()
    if current:
        current.ends_at = now
        current.ended_by = actor
        current.full_clean()
        current.save(update_fields=("ends_at", "ended_by"))
    if assignee is None:
        return None
    if not assignee.is_active:
        raise ValidationError({"assignee": "Vehiculul poate fi atribuit doar unui utilizator activ."})
    assignment = VehicleAssignment(
        vehicle=locked_vehicle,
        assignee=assignee,
        assigned_by=actor,
        starts_at=now,
    )
    assignment.full_clean()
    assignment.save()
    return assignment


@transaction.atomic
def create_vehicle(*, actor, data) -> Vehicle:
    require_staff(actor)
    assignee = data.get("assignee")
    vehicle = Vehicle(created_by=actor, **_vehicle_values(data))
    vehicle.full_clean()
    vehicle.save()
    if assignee:
        set_vehicle_assignment(actor=actor, vehicle=vehicle, assignee=assignee)
    return vehicle


@transaction.atomic
def update_vehicle(*, actor, vehicle: Vehicle, data) -> Vehicle:
    require_staff(actor)
    vehicle = Vehicle.objects.select_for_update().get(pk=vehicle.pk)
    for field, value in _vehicle_values(data).items():
        setattr(vehicle, field, value)
    vehicle.full_clean()
    vehicle.save()
    set_vehicle_assignment(actor=actor, vehicle=vehicle, assignee=data.get("assignee"))
    return vehicle


@transaction.atomic
def set_vehicle_archived(*, actor, vehicle: Vehicle, archived: bool) -> Vehicle:
    require_staff(actor)
    vehicle = Vehicle.objects.select_for_update().get(pk=vehicle.pk)
    vehicle.archived_at = timezone.now() if archived else None
    vehicle.save(update_fields=("archived_at", "updated_at"))
    if archived:
        set_vehicle_assignment(actor=actor, vehicle=vehicle, assignee=None)
    return vehicle


def _record_values(data) -> dict:
    return {
        "maintenance_type": data["maintenance_type"],
        "completed_on": data["completed_on"],
        "next_due_on": data["next_due_on"],
        "mileage": data.get("mileage"),
        "provider": data.get("provider", "").strip(),
        "cost": data.get("cost"),
        "notes": data.get("notes", "").strip(),
    }


def _validate_record_target(*, vehicle: Vehicle, maintenance_type: MaintenanceType) -> None:
    if vehicle.archived_at:
        raise ValidationError("Nu poți adăuga mentenanță unui vehicul arhivat.")
    if not maintenance_type.is_active:
        raise ValidationError({"maintenance_type": "Alege un tip de mentenanță activ."})


def _raise_vehicle_mileage(vehicle: Vehicle, mileage: int | None) -> None:
    if mileage is not None and mileage > vehicle.current_mileage:
        Vehicle.objects.filter(pk=vehicle.pk).update(current_mileage=mileage, updated_at=timezone.now())


@transaction.atomic
def create_maintenance_record(*, actor, vehicle: Vehicle, data) -> MaintenanceRecord:
    require_staff(actor)
    vehicle = Vehicle.objects.select_for_update().get(pk=vehicle.pk)
    maintenance_type = data["maintenance_type"]
    _validate_record_target(vehicle=vehicle, maintenance_type=maintenance_type)
    record = MaintenanceRecord(vehicle=vehicle, created_by=actor, **_record_values(data))
    record.full_clean()
    record.save()
    _raise_vehicle_mileage(vehicle, record.mileage)
    return record


@transaction.atomic
def update_maintenance_record(*, actor, record: MaintenanceRecord, data) -> MaintenanceRecord:
    require_staff(actor)
    record = MaintenanceRecord.objects.select_for_update().select_related("vehicle").get(pk=record.pk)
    _validate_record_target(vehicle=record.vehicle, maintenance_type=data["maintenance_type"])
    for field, value in _record_values(data).items():
        setattr(record, field, value)
    record.full_clean()
    record.save()
    _raise_vehicle_mileage(record.vehicle, record.mileage)
    return record


@transaction.atomic
def create_maintenance_type(*, actor, data) -> MaintenanceType:
    require_staff(actor)
    maintenance_type = MaintenanceType(
        code=data["code"],
        name=data["name"],
        display_order=data["display_order"],
        is_active=data.get("is_active", True),
        is_system=False,
    )
    maintenance_type.full_clean()
    maintenance_type.save()
    return maintenance_type


@transaction.atomic
def update_maintenance_type(*, actor, maintenance_type: MaintenanceType, data) -> MaintenanceType:
    require_staff(actor)
    maintenance_type = MaintenanceType.objects.select_for_update().get(pk=maintenance_type.pk)
    maintenance_type.name = data["name"]
    maintenance_type.display_order = data["display_order"]
    if not maintenance_type.is_system:
        maintenance_type.code = data["code"]
        maintenance_type.is_active = data.get("is_active", True)
    maintenance_type.full_clean()
    maintenance_type.save()
    return maintenance_type


@transaction.atomic
def archive_maintenance_type(*, actor, maintenance_type: MaintenanceType) -> MaintenanceType:
    require_staff(actor)
    maintenance_type = MaintenanceType.objects.select_for_update().get(pk=maintenance_type.pk)
    if maintenance_type.is_system:
        raise ValidationError("Tipurile de mentenanță de sistem nu pot fi arhivate.")
    maintenance_type.is_active = False
    maintenance_type.save(update_fields=("is_active", "updated_at"))
    return maintenance_type

```

## `apps/flota/static/flota/flota.js`

Size: 3.0 KB

```javascript
(() => {
    const MS_PER_DAY = 24 * 60 * 60 * 1000;

    function startOfToday() {
        const now = new Date();
        return new Date(now.getFullYear(), now.getMonth(), now.getDate());
    }

    function pluralizedDays(value) {
        return `${value} ${value === 1 ? "zi" : "zile"}`;
    }

    function setTone(badge, tone) {
        badge.classList.remove("badge-success", "badge-warning", "badge-error", "badge-ghost");
        badge.classList.toggle("badge-outline", tone !== "neutral");
        badge.classList.add(tone === "neutral" ? "badge-ghost" : `badge-${tone}`);
    }

    function deadlineBadges(root) {
        const container = root || document;
        const badges = [];
        if (container.matches?.("[data-deadline][data-due-date]")) {
            badges.push(container);
        }
        container.querySelectorAll?.("[data-deadline][data-due-date]").forEach((badge) => {
            badges.push(badge);
        });
        return badges;
    }

    function refreshDeadlines(root) {
        const today = startOfToday();
        deadlineBadges(root).forEach((badge) => {
            const parts = badge.dataset.dueDate.split("-").map(Number);
            if (parts.length !== 3 || parts.some(Number.isNaN)) return;
            const due = new Date(parts[0], parts[1] - 1, parts[2]);
            const days = Math.round((due - today) / MS_PER_DAY);
            if (days < 0) {
                badge.textContent = `Expirat de ${pluralizedDays(Math.abs(days))}`;
                setTone(badge, "error");
            } else if (days === 0) {
                badge.textContent = "Scadent astăzi";
                setTone(badge, "error");
            } else if (days <= 30) {
                badge.textContent = `Scadent în ${pluralizedDays(days)}`;
                setTone(badge, "warning");
            } else {
                badge.textContent = "Valabil";
                setTone(badge, "success");
            }
        });
    }

    function fleetPanelFromEvent(event) {
        const element = event.target;
        if (!(element instanceof Element)) return null;
        return element.closest("#fleet-panel");
    }

    function setFleetBusy(panel, isBusy) {
        if (!panel) return;
        panel.querySelectorAll("[data-fleet-loading-region]").forEach((region) => {
            region.setAttribute("aria-busy", isBusy ? "true" : "false");
        });
    }

    refreshDeadlines();
    document.addEventListener("visibilitychange", () => {
        if (!document.hidden) refreshDeadlines();
    });
    document.body.addEventListener("htmx:beforeRequest", (event) => {
        setFleetBusy(fleetPanelFromEvent(event), true);
    });
    document.body.addEventListener("htmx:afterRequest", (event) => {
        setFleetBusy(fleetPanelFromEvent(event), false);
    });
    document.body.addEventListener("htmx:responseError", (event) => {
        setFleetBusy(fleetPanelFromEvent(event), false);
    });
    document.body.addEventListener("htmx:afterSwap", (event) => {
        refreshDeadlines(event.detail?.target || document);
    });
})();
```

## `apps/flota/templates/flota/includes/deadline_badge.html`

Size: 409 B

```html
<span
    class="badge badge-sm whitespace-nowrap
        {% if state.tone == 'success' %}badge-success badge-outline
        {% elif state.tone == 'warning' %}badge-warning badge-outline
        {% elif state.tone == 'error' %}badge-error badge-outline
        {% else %}badge-ghost{% endif %}"
    {% if due_on %}data-deadline data-due-date="{{ due_on|date:'Y-m-d' }}"{% endif %}
>{{ state.label }}</span>

```

## `apps/flota/templates/flota/includes/fleet_panel.html`

Size: 10.7 KB

```html
<div id="fleet-panel" class="space-y-5">
    <div class="grid grid-cols-2 border border-base-300 bg-base-100 lg:grid-cols-4" aria-label="Rezumat flotă">
        <div class="border-b border-r border-base-300 px-5 py-4 lg:border-b-0">
            <p class="text-xs font-medium text-muted">Total vehicule</p>
            <p class="mt-1 text-2xl font-semibold text-base-content">{{ summary.total }}</p>
        </div>
        <div class="border-b border-base-300 px-5 py-4 lg:border-b-0 lg:border-r">
            <p class="text-xs font-medium text-muted">Scadente în 30 zile</p>
            <p class="mt-1 text-2xl font-semibold text-warning">{{ summary.due_soon }}</p>
        </div>
        <div class="border-r border-base-300 px-5 py-4">
            <p class="text-xs font-medium text-muted">Expirate</p>
            <p class="mt-1 text-2xl font-semibold text-error">{{ summary.overdue }}</p>
        </div>
        <div class="px-5 py-4">
            <p class="text-xs font-medium text-muted">Arhivate</p>
            <p class="mt-1 text-2xl font-semibold text-base-content">{{ summary.archived }}</p>
        </div>
    </div>

    <form
        id="fleet-filters"
        method="get"
        action="{% url 'flota:index' %}"
        class="grid grid-cols-2 gap-3 border-b border-base-300 pb-4 lg:grid-cols-7"
        aria-busy="false"
        data-fleet-loading-region
        hx-get="{% url 'flota:index' %}"
        hx-target="#fleet-panel"
        hx-swap="outerHTML show:top"
        hx-push-url="true"
        hx-indicator="#fleet-table-loading"
        hx-trigger="submit, change delay:250ms, keyup changed delay:450ms from:input[name='q']"
        hx-sync="this:replace"
        hx-disabled-elt="find input, find select, find button"
    >
        <label class="fieldset col-span-2 lg:col-span-2">
            <span class="fieldset-legend">Caută</span>
            <input name="q" value="{{ filters.q|default:'' }}" class="input input-bordered input-sm w-full" placeholder="Vehicul, VIN, nr. înmatriculare...">
        </label>
        <label class="fieldset">
            <span class="fieldset-legend">Status</span>
            <select name="status" class="select select-bordered select-sm w-full">
                <option value="">Toate</option>
                {% for value,label in status_choices %}<option value="{{ value }}"{% if filters.status == value %} selected{% endif %}>{{ label }}</option>{% endfor %}
            </select>
        </label>
        {% if request.user.is_staff %}
        <label class="fieldset">
            <span class="fieldset-legend">Responsabil</span>
            <select name="assignee" class="select select-bordered select-sm w-full">
                <option value="">Toți</option>
                {% for person in users %}<option value="{{ person.pk }}"{% if filters.assignee == person.pk|stringformat:'s' %} selected{% endif %}>{{ person.get_full_name|default:person.username }}</option>{% endfor %}
            </select>
        </label>
        {% endif %}
        <label class="fieldset">
            <span class="fieldset-legend">Termen</span>
            <select name="deadline" class="select select-bordered select-sm w-full">
                <option value="">Toate</option>
                <option value="valid"{% if filters.deadline == 'valid' %} selected{% endif %}>Valabile</option>
                <option value="due_soon"{% if filters.deadline == 'due_soon' %} selected{% endif %}>Scadente în 30 zile</option>
                <option value="overdue"{% if filters.deadline == 'overdue' %} selected{% endif %}>Expirate</option>
                <option value="missing"{% if filters.deadline == 'missing' %} selected{% endif %}>Neînregistrate</option>
            </select>
        </label>
        {% if request.user.is_staff %}
        <label class="fieldset">
            <span class="fieldset-legend">Arhivă</span>
            <select name="archived" class="select select-bordered select-sm w-full">
                <option value="0">Active</option>
                <option value="1"{% if archived_only %} selected{% endif %}>Arhivate</option>
            </select>
        </label>
        {% endif %}
        <div class="col-span-2 flex items-end gap-2 lg:col-span-1">
            <button class="btn btn-primary btn-sm flex-1" type="submit">Filtrează</button>
            <a
                href="{% url 'flota:index' %}"
                class="btn btn-ghost btn-sm"
                hx-get="{% url 'flota:index' %}"
                hx-target="#fleet-panel"
                hx-swap="outerHTML show:top"
                hx-push-url="true"
                hx-indicator="#fleet-table-loading"
            >Resetează</a>
        </div>
    </form>

    <div class="relative overflow-x-auto border border-base-300 bg-base-100" aria-live="polite" aria-busy="false" data-fleet-loading-region>
        <div
            id="fleet-table-loading"
            class="htmx-indicator absolute inset-0 z-10 flex items-center justify-center bg-base-100/80"
            role="status"
            aria-live="polite"
        >
            <span class="inline-flex items-center gap-3 border border-base-300 bg-base-100 px-4 py-3 text-sm font-medium text-base-content shadow-sm">
                <span class="loading loading-spinner loading-md text-primary" aria-hidden="true"></span>
                Se actualizează lista de vehicule
            </span>
        </div>
        <table class="table table-xs min-w-[1000px]">
            <thead>
                <tr>
                    <th>Vehicul</th>
                    <th>Nr. înmatriculare</th>
                    <th>Responsabil</th>
                    <th>Kilometraj</th>
                    <th>ITP</th>
                    <th>Asigurare</th>
                    <th>Ulei</th>
                    <th>Service</th>
                    <th class="text-right">Acțiuni</th>
                </tr>
            </thead>
            <tbody>
                {% for vehicle in page %}
                <tr class="hover:bg-base-200/60">
                    <td>
                        <a href="{% url 'flota:vehicle_detail' vehicle.pk %}" class="flex min-w-48 items-center gap-3">
                            <span class="flex h-10 w-10 shrink-0 items-center justify-center border border-base-300 bg-base-100">
                                {% if vehicle.emblem %}
                                    <img src="{{ vehicle.emblem.url }}" alt="Emblema {{ vehicle.brand }}" class="h-8 w-8 object-contain">
                                {% else %}
                                    <span class="text-sm font-bold text-primary" aria-hidden="true">{{ vehicle.brand|slice:":1"|upper }}</span>
                                {% endif %}
                            </span>
                            <span>
                                <span class="block font-semibold text-base-content">{{ vehicle.brand }} {{ vehicle.model }}</span>
                                <span class="block text-xs text-muted">{{ vehicle.get_status_display }}{% if vehicle.manufacture_year %} · {{ vehicle.manufacture_year }}{% endif %}</span>
                            </span>
                        </a>
                    </td>
                    <td class="font-medium whitespace-nowrap">{{ vehicle.registration_display }}</td>
                    <td class="whitespace-nowrap">
                        {% if vehicle.current_assignment %}
                            {{ vehicle.current_assignment.assignee.get_full_name|default:vehicle.current_assignment.assignee.username }}
                        {% else %}
                            <span class="text-muted">Neatribuit</span>
                        {% endif %}
                    </td>
                    <td class="whitespace-nowrap">{{ vehicle.current_mileage }} km</td>
                    {% for cell in vehicle.deadline_cells %}
                    <td>{% include "flota/includes/deadline_badge.html" with state=cell.state due_on=cell.record.next_due_on %}</td>
                    {% endfor %}
                    <td>
                        <div class="flex justify-end gap-1">
                            <a href="{% url 'flota:vehicle_detail' vehicle.pk %}" class="btn btn-outline btn-primary btn-square btn-xs" aria-label="Deschide {{ vehicle }}" title="Deschide">
                                <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12s3.75-6.75 9.75-6.75S21.75 12 21.75 12 18 18.75 12 18.75 2.25 12 2.25 12Z"/><circle cx="12" cy="12" r="2.25"/></svg>
                            </a>
                            {% if request.user.is_staff %}<a href="{% url 'flota:vehicle_edit' vehicle.pk %}" class="btn btn-outline btn-primary btn-square btn-xs" aria-label="Editează {{ vehicle }}" title="Editează">
                                <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="m14.7 5.3 4 4M4 20l4.35-.85L19.4 8.1a1.9 1.9 0 0 0 0-2.7l-.8-.8a1.9 1.9 0 0 0-2.7 0L4.85 15.65 4 20Z"/></svg>
                            </a>{% endif %}
                        </div>
                    </td>
                </tr>
                {% empty %}
                <tr><td colspan="9" class="py-12 text-center text-muted">Nu există vehicule pentru filtrele selectate.</td></tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    {% if page.paginator.num_pages > 1 %}
    <div class="flex items-center justify-between text-sm text-muted">
        <span>Pagina {{ page.number }} din {{ page.paginator.num_pages }}</span>
        <div class="join">
            {% if page.has_previous %}
            <a
                class="btn btn-sm join-item"
                href="?{% if query_without_page %}{{ query_without_page }}&{% endif %}page={{ page.previous_page_number }}"
                hx-get="?{% if query_without_page %}{{ query_without_page }}&{% endif %}page={{ page.previous_page_number }}"
                hx-target="#fleet-panel"
                hx-swap="outerHTML show:top"
                hx-push-url="true"
                aria-label="Pagina precedentă"
            >&lsaquo;</a>
            {% endif %}
            {% if page.has_next %}
            <a
                class="btn btn-sm join-item"
                href="?{% if query_without_page %}{{ query_without_page }}&{% endif %}page={{ page.next_page_number }}"
                hx-get="?{% if query_without_page %}{{ query_without_page }}&{% endif %}page={{ page.next_page_number }}"
                hx-target="#fleet-panel"
                hx-swap="outerHTML show:top"
                hx-push-url="true"
                aria-label="Pagina următoare"
            >&rsaquo;</a>
            {% endif %}
        </div>
    </div>
    {% endif %}
</div>
```

## `apps/flota/templates/flota/includes/form_fields.html`

Size: 831 B

```html
{% if form.non_field_errors %}
    <div class="alert alert-error py-2 text-sm sm:col-span-2" role="alert">{{ form.non_field_errors|join:", " }}</div>
{% endif %}
{% for field in form %}
    <fieldset class="fieldset min-w-0 {% if field.name == 'notes' or field.name == 'emblem' %}sm:col-span-2{% endif %}">
        <label class="fieldset-legend" for="{{ field.id_for_label }}">
            {{ field.label }}{% if field.field.required %}<span class="text-error" aria-hidden="true"> *</span>{% endif %}
        </label>
        {{ field }}
        {% if field.help_text %}<p class="label whitespace-normal text-xs text-muted">{{ field.help_text }}</p>{% endif %}
        {% if field.errors %}<p class="label whitespace-normal text-xs text-error" role="alert">{{ field.errors|join:", " }}</p>{% endif %}
    </fieldset>
{% endfor %}

```

## `apps/flota/templates/flota/includes/maintenance_type_panel.html`

Size: 4.1 KB

```html
<div id="maintenance-type-panel" class="space-y-5">
    {% include "flota/includes/messages.html" %}
    <div class="overflow-x-auto border border-base-300 bg-base-100" aria-live="polite">
        <table class="table table-xs min-w-[680px]">
            <thead><tr><th>Denumire</th><th>Cod</th><th>Ordine</th><th>Tip</th><th>Status</th><th class="text-right">Acțiuni</th></tr></thead>
            <tbody>
            {% for item in maintenance_types %}
                <tr>
                    <td class="font-semibold">{{ item.name }}</td>
                    <td><code class="text-xs">{{ item.code }}</code></td>
                    <td>{{ item.display_order }}</td>
                    <td>{% if item.is_system %}Sistem{% else %}Personalizat{% endif %}</td>
                    <td><span class="badge badge-sm {% if item.is_active %}badge-success badge-outline{% else %}badge-ghost{% endif %}">{% if item.is_active %}Activ{% else %}Arhivat{% endif %}</span></td>
                    <td>
                        <div class="flex justify-end gap-1">
                            <a href="{% url 'flota:maintenance_type_edit' item.pk %}" class="btn btn-outline btn-primary btn-square btn-xs" aria-label="Editează {{ item.name }}" title="Editează">
                                <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="m14.7 5.3 4 4M4 20l4.35-.85L19.4 8.1a1.9 1.9 0 0 0 0-2.7l-.8-.8a1.9 1.9 0 0 0-2.7 0L4.85 15.65 4 20Z"/></svg>
                            </a>
                            {% if not item.is_system and item.is_active %}
                            <form
                                method="post"
                                action="{% url 'flota:maintenance_type_archive' item.pk %}"
                                class="flex gap-1"
                                hx-post="{% url 'flota:maintenance_type_archive' item.pk %}"
                                hx-target="#maintenance-type-panel"
                                hx-swap="outerHTML show:top"
                                x-data="{ confirming: false }"
                                @submit="if (!confirming) { $event.preventDefault(); confirming = true; }"
                                @keydown.escape.window="confirming = false"
                            >
                                {% csrf_token %}
                                <button class="btn btn-outline btn-error btn-square btn-xs" type="submit" aria-label="Arhivează {{ item.name }}" title="Arhivează" :title="confirming ? 'Confirmă' : 'Arhivează'">
                                    <svg class="h-4 w-4" x-show="!confirming" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M4.5 7.5h15M9 7.5V5.25A1.25 1.25 0 0 1 10.25 4h3.5A1.25 1.25 0 0 1 15 5.25V7.5m-8.5 0 1 12.25A1.5 1.5 0 0 0 9 21h6a1.5 1.5 0 0 0 1.5-1.25l1-12.25"/></svg>
                                    <svg class="h-4 w-4" style="display: none;" x-show="confirming" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="m5 12.5 4.5 4.5L19 7"/></svg>
                                </button>
                                <button class="btn btn-ghost btn-square btn-xs" type="button" style="display: none;" x-show="confirming" @click="confirming = false" aria-label="Anulează arhivarea" title="Anulează">
                                    <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="M6 6l12 12M18 6 6 18"/></svg>
                                </button>
                            </form>
                            {% endif %}
                        </div>
                    </td>
                </tr>
            {% empty %}<tr><td colspan="6" class="py-10 text-center text-muted">Nu există tipuri de mentenanță.</td></tr>{% endfor %}
            </tbody>
        </table>
    </div>
</div>
```

## `apps/flota/templates/flota/includes/messages.html`

Size: 338 B

```html
{% if messages %}
<div class="space-y-2" aria-live="polite">
    {% for message in messages %}
        <div class="alert py-2 text-sm {% if message.tags == 'error' %}alert-error{% elif message.tags == 'success' %}alert-success{% else %}alert-info{% endif %}">
            {{ message }}
        </div>
    {% endfor %}
</div>
{% endif %}

```

## `apps/flota/templates/flota/includes/vehicle_detail_panel.html`

Size: 11.4 KB

```html
<section id="vehicle-detail-panel" class="space-y-5">
    {% include "flota/includes/messages.html" %}
    <nav class="text-xs text-muted" aria-label="Breadcrumb">
        <a href="{% url 'flota:index' %}" class="hover:text-primary">Flota</a> / {{ vehicle.registration_display }}
    </nav>

    <header class="flex flex-col gap-4 border border-base-300 bg-base-100 p-4 lg:flex-row lg:items-center">
        <span class="flex h-16 w-16 shrink-0 items-center justify-center border border-base-300 bg-base-100">
            {% if vehicle.emblem %}
                <img src="{{ vehicle.emblem.url }}" alt="Emblema {{ vehicle.brand }}" class="h-12 w-12 object-contain">
            {% else %}
                <span class="text-xl font-bold text-primary" aria-hidden="true">{{ vehicle.brand|slice:":1"|upper }}</span>
            {% endif %}
        </span>
        <div class="min-w-0">
            <h1 class="ops-title text-2xl font-bold">{{ vehicle.brand }} {{ vehicle.model }}</h1>
            <div class="mt-1 flex flex-wrap items-center gap-2 text-sm">
                <span class="font-semibold text-base-content">{{ vehicle.registration_display }}</span>
                <span class="badge badge-sm {% if vehicle.is_archived %}badge-ghost{% elif vehicle.status == 'active' %}badge-success badge-outline{% else %}badge-warning badge-outline{% endif %}">
                    {% if vehicle.is_archived %}Arhivat{% else %}{{ vehicle.get_status_display }}{% endif %}
                </span>
            </div>
        </div>
        <div class="lg:ml-8 lg:border-l lg:border-base-300 lg:pl-8">
            <p class="text-xs text-muted">Responsabil</p>
            <p class="mt-1 text-sm font-medium text-base-content">
                {% if current_assignment %}{{ current_assignment.assignee.get_full_name|default:current_assignment.assignee.username }}{% else %}Neatribuit{% endif %}
            </p>
        </div>
        {% if request.user.is_staff %}
        <div class="flex flex-wrap gap-2 lg:ml-auto">
            <a href="{% url 'flota:vehicle_edit' vehicle.pk %}" class="btn btn-primary btn-sm">Editează</a>
            {% if vehicle.is_archived %}
            <form
                method="post"
                action="{% url 'flota:vehicle_restore' vehicle.pk %}"
                class="flex flex-wrap gap-2"
                hx-post="{% url 'flota:vehicle_restore' vehicle.pk %}"
                hx-target="#vehicle-detail-panel"
                hx-swap="outerHTML show:top"
                x-data="{ confirming: false }"
                @submit="if (!confirming) { $event.preventDefault(); confirming = true; }"
                @keydown.escape.window="confirming = false"
            >
                {% csrf_token %}
                <button class="btn btn-outline btn-success btn-sm" type="submit" x-text="confirming ? 'Confirmă' : 'Restaurează'">Restaurează</button>
                <button class="btn btn-ghost btn-sm" type="button" style="display: none;" x-show="confirming" @click="confirming = false">Anulează</button>
            </form>
            {% else %}
            <form
                method="post"
                action="{% url 'flota:vehicle_archive' vehicle.pk %}"
                class="flex flex-wrap gap-2"
                hx-post="{% url 'flota:vehicle_archive' vehicle.pk %}"
                hx-target="#vehicle-detail-panel"
                hx-swap="outerHTML show:top"
                x-data="{ confirming: false }"
                @submit="if (!confirming) { $event.preventDefault(); confirming = true; }"
                @keydown.escape.window="confirming = false"
            >
                {% csrf_token %}
                <button class="btn btn-outline btn-error btn-sm" type="submit" x-text="confirming ? 'Confirmă' : 'Arhivează'">Arhivează</button>
                <button class="btn btn-ghost btn-sm" type="button" style="display: none;" x-show="confirming" @click="confirming = false">Anulează</button>
            </form>
            {% endif %}
        </div>
        {% endif %}
    </header>

    <div class="grid gap-5 xl:grid-cols-[minmax(280px,0.8fr)_minmax(0,2fr)]">
        <div class="space-y-5">
            <section class="border border-base-300 bg-base-100">
                <h2 class="border-b border-base-300 px-4 py-3 text-sm font-semibold text-base-content">Date vehicul</h2>
                <dl class="divide-y divide-base-300 text-sm">
                    <div class="grid grid-cols-2 gap-3 px-4 py-3"><dt class="text-muted">VIN</dt><dd class="text-right font-medium">{{ vehicle.vin|default:"—" }}</dd></div>
                    <div class="grid grid-cols-2 gap-3 px-4 py-3"><dt class="text-muted">An fabricație</dt><dd class="text-right font-medium">{{ vehicle.manufacture_year|default:"—" }}</dd></div>
                    <div class="grid grid-cols-2 gap-3 px-4 py-3"><dt class="text-muted">Kilometraj</dt><dd class="text-right font-medium">{{ vehicle.current_mileage }} km</dd></div>
                    <div class="grid grid-cols-2 gap-3 px-4 py-3"><dt class="text-muted">Status</dt><dd class="text-right font-medium">{{ vehicle.get_status_display }}</dd></div>
                    <div class="grid grid-cols-2 gap-3 px-4 py-3"><dt class="text-muted">Responsabil</dt><dd class="text-right font-medium">{% if current_assignment %}{{ current_assignment.assignee.get_full_name|default:current_assignment.assignee.username }}{% else %}Neatribuit{% endif %}</dd></div>
                </dl>
            </section>

            <section class="border border-base-300 bg-base-100">
                <div class="flex items-center justify-between border-b border-base-300 px-4 py-3">
                    <h2 class="text-sm font-semibold text-base-content">Termene mentenanță</h2>
                    {% if request.user.is_staff and not vehicle.is_archived %}<a href="{% url 'flota:maintenance_create' vehicle.pk %}" class="btn btn-primary btn-xs">Înregistrează</a>{% endif %}
                </div>
                <div class="divide-y divide-base-300">
                    {% for row in deadline_rows %}
                    <div class="space-y-2 px-4 py-3">
                        <div class="flex items-center justify-between gap-3">
                            <h3 class="text-sm font-semibold text-base-content">{{ row.type.name }}</h3>
                            {% include "flota/includes/deadline_badge.html" with state=row.state due_on=row.record.next_due_on %}
                        </div>
                        <div class="grid grid-cols-2 gap-3 text-xs">
                            <div><span class="block text-muted">Ultima efectuare</span><span class="font-medium">{% if row.record %}{{ row.record.completed_on|date:"d.m.Y" }}{% else %}—{% endif %}</span></div>
                            <div><span class="block text-muted">Următorul termen</span><span class="font-medium">{% if row.record %}{{ row.record.next_due_on|date:"d.m.Y" }}{% else %}—{% endif %}</span></div>
                        </div>
                        {% if request.user.is_staff and not vehicle.is_archived %}<a href="{% url 'flota:maintenance_create' vehicle.pk %}?type={{ row.type.pk }}" class="text-xs font-medium text-primary hover:underline">Înregistrează {{ row.type.name|lower }}</a>{% endif %}
                    </div>
                    {% empty %}<p class="px-4 py-8 text-center text-sm text-muted">Nu există tipuri de mentenanță active.</p>{% endfor %}
                </div>
            </section>
        </div>

        <div class="space-y-5">
            <section class="border border-base-300 bg-base-100">
                <div class="flex items-center justify-between border-b border-base-300 px-4 py-3">
                    <h2 class="text-sm font-semibold text-base-content">Istoric servicii</h2>
                    {% if request.user.is_staff and not vehicle.is_archived %}<a href="{% url 'flota:maintenance_create' vehicle.pk %}" class="btn btn-primary btn-xs">Înregistrare nouă</a>{% endif %}
                </div>
                <div class="overflow-x-auto">
                    <table class="table table-sm min-w-[760px]">
                        <thead><tr><th>Tip</th><th>Efectuat la</th><th>Următorul termen</th><th>Kilometraj</th><th>Furnizor</th><th>Cost</th><th class="text-right">Acțiuni</th></tr></thead>
                        <tbody>
                        {% for record in maintenance_records %}
                            <tr>
                                <td class="font-medium">{{ record.maintenance_type.name }}</td>
                                <td class="whitespace-nowrap">{{ record.completed_on|date:"d.m.Y" }}</td>
                                <td class="whitespace-nowrap">{{ record.next_due_on|date:"d.m.Y" }}</td>
                                <td class="whitespace-nowrap">{% if record.mileage is not None %}{{ record.mileage }} km{% else %}—{% endif %}</td>
                                <td>{{ record.provider|default:"—" }}</td>
                                <td class="whitespace-nowrap">{% if record.cost is not None %}{{ record.cost }} lei{% else %}—{% endif %}</td>
                                <td class="text-right">
                                    {% if request.user.is_staff %}
                                    <a href="{% url 'flota:maintenance_edit' record.pk %}" class="btn btn-outline btn-primary btn-square btn-xs" aria-label="Editează {{ record.maintenance_type.name }}" title="Editează">
                                        <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" d="m14.7 5.3 4 4M4 20l4.35-.85L19.4 8.1a1.9 1.9 0 0 0 0-2.7l-.8-.8a1.9 1.9 0 0 0-2.7 0L4.85 15.65 4 20Z"/></svg>
                                    </a>
                                    {% else %}—{% endif %}
                                </td>
                            </tr>
                        {% empty %}<tr><td colspan="7" class="py-10 text-center text-muted">Nu există intervenții înregistrate.</td></tr>{% endfor %}
                        </tbody>
                    </table>
                </div>
            </section>

            <section class="border border-base-300 bg-base-100">
                <h2 class="border-b border-base-300 px-4 py-3 text-sm font-semibold text-base-content">Istoric atribuiri</h2>
                <div class="overflow-x-auto">
                    <table class="table table-sm min-w-[560px]">
                        <thead><tr><th>De la</th><th>Până la</th><th>Responsabil</th><th>Atribuit de</th></tr></thead>
                        <tbody>
                        {% for assignment in assignment_history %}
                            <tr>
                                <td class="whitespace-nowrap">{{ assignment.starts_at|date:"d.m.Y H:i" }}</td>
                                <td class="whitespace-nowrap">{% if assignment.ends_at %}{{ assignment.ends_at|date:"d.m.Y H:i" }}{% else %}Prezent{% endif %}</td>
                                <td>{{ assignment.assignee.get_full_name|default:assignment.assignee.username }}</td>
                                <td>{{ assignment.assigned_by.get_full_name|default:assignment.assigned_by.username }}</td>
                            </tr>
                        {% empty %}<tr><td colspan="4" class="py-8 text-center text-muted">Vehiculul nu a fost atribuit.</td></tr>{% endfor %}
                        </tbody>
                    </table>
                </div>
            </section>
        </div>
    </div>
</section>
```

## `apps/flota/templates/flota/index.html`

Size: 1.1 KB

```html
{% extends "layouts/base.html" %}
{% load static %}

{% block title %}Flota | Platforma TUVTK{% endblock %}

{% block content %}
<section class="space-y-5">
    {% include "flota/includes/messages.html" %}

    <div class="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
            <h1 class="ops-title text-2xl font-bold sm:text-[2rem]">Flota</h1>
            <p class="mt-1 text-sm text-muted">Administrarea vehiculelor și a termenelor de mentenanță.</p>
        </div>
        {% if request.user.is_staff %}
        <div class="flex flex-wrap gap-2">
            <a href="{% url 'flota:maintenance_type_list' %}" class="btn btn-outline btn-primary btn-sm">Tipuri mentenanță</a>
            <a href="{% url 'flota:vehicle_create' %}" class="btn btn-primary btn-sm">
                <i class="bi bi-plus-lg" aria-hidden="true"></i> Adaugă vehicul
            </a>
        </div>
        {% endif %}
    </div>

    {% include "flota/includes/fleet_panel.html" %}
</section>
{% endblock %}

{% block page_scripts %}<script src="{% static 'flota/flota.js' %}" defer></script>{% endblock %}
```

## `apps/flota/templates/flota/maintenance_form.html`

Size: 1.1 KB

```html
{% extends "layouts/base.html" %}

{% block title %}{% if record %}Editează mentenanța{% else %}Mentenanță nouă{% endif %} | Flota{% endblock %}

{% block content %}
<section class="mx-auto max-w-3xl space-y-5">
    <div>
        <p class="text-xs text-muted"><a href="{% url 'flota:vehicle_detail' vehicle.pk %}" class="hover:text-primary">{{ vehicle.brand }} {{ vehicle.model }}</a> / Mentenanță</p>
        <h1 class="ops-title mt-1 text-2xl font-bold">{% if record %}Editează înregistrarea{% else %}Înregistrează mentenanța{% endif %}</h1>
        <p class="mt-1 text-sm text-muted">{{ vehicle.registration_display }} · {{ vehicle.current_mileage }} km</p>
    </div>
    <form method="post" class="space-y-5 border border-base-300 bg-base-100 p-5">
        {% csrf_token %}
        <div class="grid gap-x-4 sm:grid-cols-2">{% include "flota/includes/form_fields.html" %}</div>
        <div class="flex justify-end gap-2">
            <a href="{% url 'flota:vehicle_detail' vehicle.pk %}" class="btn btn-ghost btn-sm">Anulează</a>
            <button class="btn btn-primary btn-sm">Salvează</button>
        </div>
    </form>
</section>
{% endblock %}

```

## `apps/flota/templates/flota/maintenance_type_form.html`

Size: 1013 B

```html
{% extends "layouts/base.html" %}

{% block title %}{% if maintenance_type %}Editează tipul{% else %}Tip nou{% endif %} | Flota{% endblock %}

{% block content %}
<section class="mx-auto max-w-2xl space-y-5">
    <div>
        <p class="text-xs text-muted"><a href="{% url 'flota:maintenance_type_list' %}" class="hover:text-primary">Tipuri mentenanță</a> / Formular</p>
        <h1 class="ops-title mt-1 text-2xl font-bold">{% if maintenance_type %}Editează tipul{% else %}Tip de mentenanță nou{% endif %}</h1>
    </div>
    <form method="post" class="space-y-5 border border-base-300 bg-base-100 p-5">
        {% csrf_token %}
        <div class="grid gap-x-4 sm:grid-cols-2">{% include "flota/includes/form_fields.html" %}</div>
        <div class="flex justify-end gap-2">
            <a href="{% url 'flota:maintenance_type_list' %}" class="btn btn-ghost btn-sm">Anulează</a>
            <button class="btn btn-primary btn-sm">Salvează</button>
        </div>
    </form>
</section>
{% endblock %}

```

## `apps/flota/templates/flota/maintenance_type_list.html`

Size: 803 B

```html
{% extends "layouts/base.html" %}

{% block title %}Tipuri mentenanță | Flota{% endblock %}

{% block content %}
<section class="space-y-5">
    <div class="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
            <p class="text-xs text-muted"><a href="{% url 'flota:index' %}" class="hover:text-primary">Flota</a> / Configurare</p>
            <h1 class="ops-title mt-1 text-2xl font-bold">Tipuri de mentenanță</h1>
            <p class="mt-1 text-sm text-muted">Tipurile de sistem sunt protejate; tipurile personalizate pot fi arhivate.</p>
        </div>
        <a href="{% url 'flota:maintenance_type_create' %}" class="btn btn-primary btn-sm">Tip nou</a>
    </div>

    {% include "flota/includes/maintenance_type_panel.html" %}
</section>
{% endblock %}
```

## `apps/flota/templates/flota/vehicle_detail.html`

Size: 324 B

```html
{% extends "layouts/base.html" %}
{% load static %}

{% block title %}{{ vehicle.brand }} {{ vehicle.model }} | Flota{% endblock %}

{% block content %}
{% include "flota/includes/vehicle_detail_panel.html" %}
{% endblock %}

{% block page_scripts %}<script src="{% static 'flota/flota.js' %}" defer></script>{% endblock %}
```

## `apps/flota/templates/flota/vehicle_form.html`

Size: 1.1 KB

```html
{% extends "layouts/base.html" %}

{% block title %}{% if vehicle %}Editează {{ vehicle }}{% else %}Vehicul nou{% endif %} | Flota{% endblock %}

{% block content %}
<section class="mx-auto max-w-3xl space-y-5">
    <div>
        <p class="text-xs text-muted"><a href="{% url 'flota:index' %}" class="hover:text-primary">Flota</a> / Vehicul</p>
        <h1 class="ops-title mt-1 text-2xl font-bold">{% if vehicle %}Editează vehiculul{% else %}Adaugă vehicul{% endif %}</h1>
        <p class="mt-1 text-sm text-muted">Datele vehiculului și responsabilul curent.</p>
    </div>
    <form method="post" enctype="multipart/form-data" class="space-y-5 border border-base-300 bg-base-100 p-5">
        {% csrf_token %}
        <div class="grid gap-x-4 sm:grid-cols-2">{% include "flota/includes/form_fields.html" %}</div>
        <div class="flex justify-end gap-2">
            <a href="{% if vehicle %}{% url 'flota:vehicle_detail' vehicle.pk %}{% else %}{% url 'flota:index' %}{% endif %}" class="btn btn-ghost btn-sm">Anulează</a>
            <button class="btn btn-primary btn-sm">Salvează</button>
        </div>
    </form>
</section>
{% endblock %}

```

## `apps/flota/tests.py`

Size: 14.1 KB

Redacted secret-like assignments: 2

```python
from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError, transaction
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from .models import MaintenanceRecord, MaintenanceType, Vehicle, VehicleAssignment
from .selectors import deadline_state, visible_vehicles
from .services import (
    archive_maintenance_type,
    create_maintenance_record,
    create_maintenance_type,
    create_vehicle,
    set_vehicle_archived,
    set_vehicle_assignment,
)
from .validators import validate_emblem


class FlotaAppTests(TestCase):
    def setUp(self):
        users = get_user_model().objects
        self.staff = users.create_user(
            username="fleet-admin",
            password=<redacted>
            first_name="Ana",
            last_name="Admin",
            is_staff=True,
        )
        self.driver = users.create_user(
            username="driver",
            password=<redacted>
            first_name="Dan",
            last_name="Ionescu",
        )
        self.other_driver = users.create_user(username="other-driver", password="test-password")
        self.outsider = users.create_user(username="outsider", password="test-password")
        self.vehicle = create_vehicle(
            actor=self.staff,
            data={
                "registration_number": "B 123 TUV",
                "vin": "UU1HSDACX50123456",
                "brand": "Dacia",
                "model": "Duster",
                "manufacture_year": 2022,
                "current_mileage": 42000,
                "emblem": None,
                "status": Vehicle.Status.ACTIVE,
                "assignee": self.driver,
            },
        )
        self.itp = MaintenanceType.objects.get(code="itp")
        self.client.force_login(self.staff)

    def maintenance_data(self, **overrides):
        data = {
            "maintenance_type": self.itp,
            "completed_on": date.today() - timedelta(days=30),
            "next_due_on": date.today() + timedelta(days=335),
            "mileage": 42500,
            "provider": "RAR București",
            "cost": Decimal("250.00"),
            "notes": "Verificare periodică",
        }
        data.update(overrides)
        return data

    def test_system_maintenance_types_are_seeded(self):
        self.assertEqual(
            list(MaintenanceType.objects.filter(is_system=True).values_list("code", flat=True)),
            ["itp", "insurance", "oil_change", "service"],
        )

    def test_vehicle_identifiers_are_normalized(self):
        self.assertEqual(self.vehicle.registration_number, "B123TUV")
        self.assertEqual(self.vehicle.registration_display, "B 123 TUV")
        self.assertEqual(self.vehicle.vin, "UU1HSDACX50123456")

    def test_vehicle_rejects_invalid_vin_and_year(self):
        self.vehicle.vin = "INVALID"
        self.vehicle.manufacture_year = date.today().year + 2
        with self.assertRaises(ValidationError) as context:
            self.vehicle.full_clean()
        self.assertIn("vin", context.exception.error_dict)
        self.assertIn("manufacture_year", context.exception.error_dict)

    def test_registration_number_is_case_insensitive_unique(self):
        duplicate = Vehicle(
            registration_number="b123tuv",
            brand="Dacia",
            model="Logan",
            created_by=self.staff,
        )
        with self.assertRaises(ValidationError):
            duplicate.full_clean()

    def test_emblem_rejects_unsupported_file(self):
        upload = SimpleUploadedFile("emblem.gif", b"GIF89a", content_type="image/gif")
        with self.assertRaises(ValidationError):
            validate_emblem(upload)

    def test_assignment_reassignment_and_unassignment_keep_history(self):
        first = self.vehicle.assignments.get(ends_at__isnull=True)
        set_vehicle_assignment(actor=self.staff, vehicle=self.vehicle, assignee=self.other_driver)
        first.refresh_from_db()
        self.assertIsNotNone(first.ends_at)
        current = self.vehicle.assignments.get(ends_at__isnull=True)
        self.assertEqual(current.assignee, self.other_driver)
        set_vehicle_assignment(actor=self.staff, vehicle=self.vehicle, assignee=None)
        self.assertFalse(self.vehicle.assignments.filter(ends_at__isnull=True).exists())
        self.assertEqual(self.vehicle.assignments.count(), 2)

    def test_database_prevents_two_open_assignments(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            VehicleAssignment.objects.create(
                vehicle=self.vehicle,
                assignee=self.other_driver,
                assigned_by=self.staff,
            )

    def test_non_staff_cannot_mutate_through_services(self):
        with self.assertRaises(PermissionDenied):
            set_vehicle_assignment(actor=self.driver, vehicle=self.vehicle, assignee=None)

    def test_maintenance_record_updates_vehicle_mileage(self):
        create_maintenance_record(
            actor=self.staff,
            vehicle=self.vehicle,
            data=self.maintenance_data(mileage=50000),
        )
        self.vehicle.refresh_from_db()
        self.assertEqual(self.vehicle.current_mileage, 50000)

    def test_maintenance_due_date_must_follow_completion(self):
        with self.assertRaises(ValidationError):
            create_maintenance_record(
                actor=self.staff,
                vehicle=self.vehicle,
                data=self.maintenance_data(
                    completed_on=date.today(),
                    next_due_on=date.today(),
                ),
            )

    def test_deadline_state_boundaries(self):
        today = date(2026, 7, 5)
        self.assertEqual(deadline_state(today + timedelta(days=31), today=today).code, "valid")
        self.assertEqual(deadline_state(today + timedelta(days=30), today=today).code, "due_soon")
        self.assertEqual(deadline_state(today, today=today).code, "today")
        self.assertEqual(deadline_state(today - timedelta(days=1), today=today).code, "overdue")
        self.assertEqual(deadline_state(None, today=today).code, "missing")

    def test_archiving_closes_assignment_and_restore_does_not_reassign(self):
        set_vehicle_archived(actor=self.staff, vehicle=self.vehicle, archived=True)
        self.vehicle.refresh_from_db()
        self.assertTrue(self.vehicle.is_archived)
        self.assertFalse(self.vehicle.assignments.filter(ends_at__isnull=True).exists())
        set_vehicle_archived(actor=self.staff, vehicle=self.vehicle, archived=False)
        self.vehicle.refresh_from_db()
        self.assertFalse(self.vehicle.is_archived)
        self.assertFalse(self.vehicle.assignments.filter(ends_at__isnull=True).exists())

    def test_assigned_user_visibility_is_owner_scoped(self):
        visible = visible_vehicles(user=self.driver)
        self.assertTrue(visible.filter(pk=self.vehicle.pk).exists())
        self.assertFalse(visible_vehicles(user=self.outsider).filter(pk=self.vehicle.pk).exists())

    def test_anonymous_user_is_redirected(self):
        self.client.logout()
        response = self.client.get(reverse("flota:index"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("login")))

    def test_staff_list_and_assigned_detail_render(self):
        response = self.client.get(reverse("flota:index"))
        self.assertContains(response, "Administrarea vehiculelor")
        self.assertContains(response, "Dacia Duster")
        self.client.force_login(self.driver)
        response = self.client.get(reverse("flota:vehicle_detail", args=[self.vehicle.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Istoric atribuiri")
        self.assertNotContains(response, "Arhivează")

    def test_outsider_receives_404_for_vehicle_detail(self):
        self.client.force_login(self.outsider)
        response = self.client.get(reverse("flota:vehicle_detail", args=[self.vehicle.pk]))
        self.assertEqual(response.status_code, 404)

    def test_non_staff_vehicle_create_is_forbidden(self):
        self.client.force_login(self.driver)
        response = self.client.get(reverse("flota:vehicle_create"))
        self.assertEqual(response.status_code, 403)

    def test_vehicle_create_form_persists_assignment(self):
        response = self.client.post(
            reverse("flota:vehicle_create"),
            {
                "registration_number": "CJ 12 ABC",
                "vin": "",
                "brand": "Volkswagen",
                "model": "Golf",
                "manufacture_year": 2020,
                "current_mileage": 75000,
                "status": Vehicle.Status.ACTIVE,
                "assignee": self.other_driver.pk,
            },
        )
        created = Vehicle.objects.get(registration_number="CJ12ABC")
        self.assertRedirects(response, reverse("flota:vehicle_detail", args=[created.pk]))
        self.assertEqual(created.assignments.get(ends_at__isnull=True).assignee, self.other_driver)

    def test_list_filters_by_assignee_and_deadline(self):
        create_maintenance_record(
            actor=self.staff,
            vehicle=self.vehicle,
            data=self.maintenance_data(next_due_on=date.today() + timedelta(days=10)),
        )
        response = self.client.get(
            reverse("flota:index"),
            {"assignee": self.driver.pk, "deadline": "due_soon"},
        )
        self.assertContains(response, "Dacia Duster")
        response = self.client.get(reverse("flota:index"), {"deadline": "overdue"})
        self.assertNotContains(response, "Dacia Duster")

    def test_htmx_list_filters_render_fleet_panel_only(self):
        response = self.client.get(
            reverse("flota:index"),
            {"q": "Dacia"},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "flota/includes/fleet_panel.html")
        self.assertContains(response, 'id="fleet-panel"')
        self.assertContains(response, "Dacia Duster")
        self.assertNotContains(response, "<html")

    def test_fleet_filter_partial_renders_loading_and_sync_hooks(self):
        response = self.client.get(reverse("flota:index"), HTTP_HX_REQUEST="true")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'hx-sync="this:replace"')
        self.assertContains(response, 'hx-disabled-elt="find input, find select, find button"')
        self.assertContains(response, 'hx-indicator="#fleet-table-loading"', count=2)
        self.assertNotContains(response, "fleet-filter-indicator")
        self.assertContains(response, 'id="fleet-table-loading"')
        self.assertContains(response, "data-fleet-loading-region", count=2)
        self.assertContains(response, 'aria-busy="false"', count=2)

    def test_htmx_vehicle_archive_refreshes_detail_panel(self):
        response = self.client.post(
            reverse("flota:vehicle_archive", args=[self.vehicle.pk]),
            HTTP_HX_REQUEST="true",
        )
        self.vehicle.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "flota/includes/vehicle_detail_panel.html")
        self.assertTrue(self.vehicle.is_archived)
        self.assertContains(response, 'id="vehicle-detail-panel"')
        self.assertContains(response, "Restaurează")
        self.assertNotContains(response, "<html")

    def test_htmx_vehicle_restore_refreshes_detail_panel(self):
        set_vehicle_archived(actor=self.staff, vehicle=self.vehicle, archived=True)
        response = self.client.post(
            reverse("flota:vehicle_restore", args=[self.vehicle.pk]),
            HTTP_HX_REQUEST="true",
        )
        self.vehicle.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "flota/includes/vehicle_detail_panel.html")
        self.assertFalse(self.vehicle.is_archived)
        self.assertContains(response, "Arhivează")
        self.assertNotContains(response, "<html")

    def test_htmx_maintenance_type_archive_refreshes_list_panel(self):
        custom = create_maintenance_type(
            actor=self.staff,
            data={"name": "Rovinietă", "code": "rovinieta", "display_order": 50, "is_active": True},
        )
        response = self.client.post(
            reverse("flota:maintenance_type_archive", args=[custom.pk]),
            HTTP_HX_REQUEST="true",
        )
        custom.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "flota/includes/maintenance_type_panel.html")
        self.assertFalse(custom.is_active)
        self.assertContains(response, 'id="maintenance-type-panel"')
        self.assertContains(response, "Arhivat")
        self.assertNotContains(response, "<html")

    def test_maintenance_history_renders_on_detail(self):
        create_maintenance_record(
            actor=self.staff,
            vehicle=self.vehicle,
            data=self.maintenance_data(),
        )
        response = self.client.get(reverse("flota:vehicle_detail", args=[self.vehicle.pk]))
        self.assertContains(response, "RAR București")
        self.assertContains(response, "250.00")

    def test_custom_type_can_be_archived_but_system_type_cannot(self):
        custom = create_maintenance_type(
            actor=self.staff,
            data={"name": "Rovinietă", "code": "rovinieta", "display_order": 50, "is_active": True},
        )
        archive_maintenance_type(actor=self.staff, maintenance_type=custom)
        custom.refresh_from_db()
        self.assertFalse(custom.is_active)
        with self.assertRaises(ValidationError):
            archive_maintenance_type(actor=self.staff, maintenance_type=self.itp)

    def test_archive_action_requires_csrf(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.staff)
        response = client.post(reverse("flota:vehicle_archive", args=[self.vehicle.pk]))
        self.assertEqual(response.status_code, 403)
```

## `apps/flota/urls.py`

Size: 1.5 KB

```python
from django.urls import path

from . import views


app_name = "flota"

urlpatterns = [
    path("", views.FleetIndexView.as_view(), name="index"),
    path("vehicule/noi/", views.VehicleCreateView.as_view(), name="vehicle_create"),
    path("vehicule/<uuid:vehicle_id>/", views.VehicleDetailView.as_view(), name="vehicle_detail"),
    path("vehicule/<uuid:vehicle_id>/editare/", views.VehicleEditView.as_view(), name="vehicle_edit"),
    path("vehicule/<uuid:vehicle_id>/arhivare/", views.VehicleArchiveView.as_view(), name="vehicle_archive"),
    path("vehicule/<uuid:vehicle_id>/restaurare/", views.VehicleRestoreView.as_view(), name="vehicle_restore"),
    path(
        "vehicule/<uuid:vehicle_id>/mentenanta/noua/",
        views.MaintenanceCreateView.as_view(),
        name="maintenance_create",
    ),
    path("mentenanta/<uuid:record_id>/editare/", views.MaintenanceEditView.as_view(), name="maintenance_edit"),
    path("tipuri-mentenanta/", views.MaintenanceTypeListView.as_view(), name="maintenance_type_list"),
    path(
        "tipuri-mentenanta/noi/",
        views.MaintenanceTypeCreateView.as_view(),
        name="maintenance_type_create",
    ),
    path(
        "tipuri-mentenanta/<int:type_id>/editare/",
        views.MaintenanceTypeEditView.as_view(),
        name="maintenance_type_edit",
    ),
    path(
        "tipuri-mentenanta/<int:type_id>/arhivare/",
        views.MaintenanceTypeArchiveView.as_view(),
        name="maintenance_type_archive",
    ),
]

```

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

## `apps/flota/views.py`

Size: 13.1 KB

```python
from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .forms import MaintenanceRecordForm, MaintenanceTypeForm, VehicleForm
from .models import MaintenanceRecord, MaintenanceType, Vehicle, VehicleAssignment
from .selectors import (
    active_users,
    core_maintenance_types,
    decorate_vehicle_rows,
    filter_vehicles,
    fleet_summary,
    get_staff_vehicle,
    get_visible_vehicle,
    vehicle_deadline_rows,
    visible_vehicles,
)
from .services import (
    archive_maintenance_type,
    create_maintenance_record,
    create_maintenance_type,
    create_vehicle,
    set_vehicle_archived,
    update_maintenance_record,
    update_maintenance_type,
    update_vehicle,
)


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        return self.request.user.is_staff


def _current_assignment(vehicle):
    return vehicle.assignments.filter(ends_at__isnull=True).select_related("assignee").first()


def _apply_validation_error(form, error):
    if hasattr(error, "error_dict"):
        for field, errors in error.error_dict.items():
            target = field if field in form.fields else None
            for item in errors:
                form.add_error(target, item)
    else:
        for message in error.messages:
            form.add_error(None, message)


def _is_htmx(request):
    return request.headers.get("HX-Request") == "true"


def _fleet_index_context(request):
    archived_only = request.user.is_staff and request.GET.get("archived") == "1"
    base_queryset = visible_vehicles(user=request.user, include_archived=archived_only)
    filtered = filter_vehicles(base_queryset, request.GET)
    paginator = Paginator(filtered, 20)
    page = paginator.get_page(request.GET.get("page"))
    page.object_list = decorate_vehicle_rows(page.object_list)
    query = request.GET.copy()
    query.pop("page", None)
    summary_queryset = Vehicle.objects.all() if request.user.is_staff else visible_vehicles(user=request.user)
    return {
        "page": page,
        "summary": fleet_summary(queryset=summary_queryset),
        "filters": request.GET,
        "status_choices": Vehicle.Status.choices,
        "users": active_users() if request.user.is_staff else [],
        "archived_only": archived_only,
        "query_without_page": urlencode(query, doseq=True),
    }


def _vehicle_detail_context(vehicle):
    return {
        "vehicle": vehicle,
        "current_assignment": _current_assignment(vehicle),
        "deadline_rows": vehicle_deadline_rows(vehicle),
        "maintenance_records": vehicle.maintenance_records.select_related(
            "maintenance_type", "created_by"
        ),
        "assignment_history": vehicle.assignments.select_related(
            "assignee", "assigned_by", "ended_by"
        ),
    }


def _maintenance_type_context():
    return {"maintenance_types": MaintenanceType.objects.all()}


class FleetIndexView(LoginRequiredMixin, View):
    template_name = "flota/index.html"
    partial_template_name = "flota/includes/fleet_panel.html"

    def get(self, request):
        template_name = self.partial_template_name if _is_htmx(request) else self.template_name
        return render(request, template_name, _fleet_index_context(request))


class VehicleDetailView(LoginRequiredMixin, View):
    template_name = "flota/vehicle_detail.html"
    partial_template_name = "flota/includes/vehicle_detail_panel.html"

    def get(self, request, vehicle_id):
        vehicle = get_visible_vehicle(user=request.user, vehicle_id=vehicle_id)
        template_name = self.partial_template_name if _is_htmx(request) else self.template_name
        return render(request, template_name, _vehicle_detail_context(vehicle))


class VehicleCreateView(StaffRequiredMixin, View):
    template_name = "flota/vehicle_form.html"

    def get(self, request):
        return render(request, self.template_name, {"form": VehicleForm(), "vehicle": None})

    def post(self, request):
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                vehicle = create_vehicle(actor=request.user, data=form.cleaned_data)
            except ValidationError as error:
                _apply_validation_error(form, error)
            else:
                messages.success(request, "Vehiculul a fost adăugat în flotă.")
                return redirect("flota:vehicle_detail", vehicle_id=vehicle.pk)
        return render(request, self.template_name, {"form": form, "vehicle": None}, status=400)


class VehicleEditView(StaffRequiredMixin, View):
    template_name = "flota/vehicle_form.html"

    def get_vehicle(self, vehicle_id):
        return get_staff_vehicle(vehicle_id=vehicle_id)

    def get(self, request, vehicle_id):
        vehicle = self.get_vehicle(vehicle_id)
        form = VehicleForm(instance=vehicle, current_assignment=_current_assignment(vehicle))
        return render(request, self.template_name, {"form": form, "vehicle": vehicle})

    def post(self, request, vehicle_id):
        vehicle = self.get_vehicle(vehicle_id)
        form = VehicleForm(
            request.POST,
            request.FILES,
            instance=vehicle,
            current_assignment=_current_assignment(vehicle),
        )
        if form.is_valid():
            try:
                vehicle = update_vehicle(actor=request.user, vehicle=vehicle, data=form.cleaned_data)
            except ValidationError as error:
                _apply_validation_error(form, error)
            else:
                messages.success(request, "Datele vehiculului au fost actualizate.")
                return redirect("flota:vehicle_detail", vehicle_id=vehicle.pk)
        return render(request, self.template_name, {"form": form, "vehicle": vehicle}, status=400)


class VehicleArchiveView(StaffRequiredMixin, View):
    def post(self, request, vehicle_id):
        vehicle = get_staff_vehicle(vehicle_id=vehicle_id)
        vehicle = set_vehicle_archived(actor=request.user, vehicle=vehicle, archived=True)
        messages.success(request, "Vehiculul a fost arhivat, iar atribuirea curentă a fost încheiată.")
        if _is_htmx(request):
            return render(
                request,
                VehicleDetailView.partial_template_name,
                _vehicle_detail_context(vehicle),
            )
        return redirect("flota:vehicle_detail", vehicle_id=vehicle.pk)


class VehicleRestoreView(StaffRequiredMixin, View):
    def post(self, request, vehicle_id):
        vehicle = get_staff_vehicle(vehicle_id=vehicle_id)
        vehicle = set_vehicle_archived(actor=request.user, vehicle=vehicle, archived=False)
        messages.success(request, "Vehiculul a fost restaurat și este neatribuit.")
        if _is_htmx(request):
            return render(
                request,
                VehicleDetailView.partial_template_name,
                _vehicle_detail_context(vehicle),
            )
        return redirect("flota:vehicle_detail", vehicle_id=vehicle.pk)


class MaintenanceCreateView(StaffRequiredMixin, View):
    template_name = "flota/maintenance_form.html"

    def get(self, request, vehicle_id):
        vehicle = get_staff_vehicle(vehicle_id=vehicle_id)
        if vehicle.is_archived:
            raise Http404
        initial = {"mileage": vehicle.current_mileage}
        type_id = request.GET.get("type")
        if type_id:
            initial["maintenance_type"] = type_id
        return render(
            request,
            self.template_name,
            {"form": MaintenanceRecordForm(initial=initial), "vehicle": vehicle, "record": None},
        )

    def post(self, request, vehicle_id):
        vehicle = get_staff_vehicle(vehicle_id=vehicle_id)
        form = MaintenanceRecordForm(request.POST)
        if form.is_valid():
            try:
                record = create_maintenance_record(actor=request.user, vehicle=vehicle, data=form.cleaned_data)
            except ValidationError as error:
                _apply_validation_error(form, error)
            else:
                messages.success(request, "Intervenția de mentenanță a fost înregistrată.")
                return redirect("flota:vehicle_detail", vehicle_id=record.vehicle_id)
        return render(
            request,
            self.template_name,
            {"form": form, "vehicle": vehicle, "record": None},
            status=400,
        )


class MaintenanceEditView(StaffRequiredMixin, View):
    template_name = "flota/maintenance_form.html"

    def get_record(self, record_id):
        return get_object_or_404(MaintenanceRecord.objects.select_related("vehicle", "maintenance_type"), pk=record_id)

    def get(self, request, record_id):
        record = self.get_record(record_id)
        return render(
            request,
            self.template_name,
            {"form": MaintenanceRecordForm(instance=record), "vehicle": record.vehicle, "record": record},
        )

    def post(self, request, record_id):
        record = self.get_record(record_id)
        form = MaintenanceRecordForm(request.POST, instance=record)
        if form.is_valid():
            try:
                record = update_maintenance_record(actor=request.user, record=record, data=form.cleaned_data)
            except ValidationError as error:
                _apply_validation_error(form, error)
            else:
                messages.success(request, "Înregistrarea de mentenanță a fost actualizată.")
                return redirect("flota:vehicle_detail", vehicle_id=record.vehicle_id)
        return render(
            request,
            self.template_name,
            {"form": form, "vehicle": record.vehicle, "record": record},
            status=400,
        )


class MaintenanceTypeListView(StaffRequiredMixin, View):
    template_name = "flota/maintenance_type_list.html"
    partial_template_name = "flota/includes/maintenance_type_panel.html"

    def get(self, request):
        template_name = self.partial_template_name if _is_htmx(request) else self.template_name
        return render(request, template_name, _maintenance_type_context())


class MaintenanceTypeCreateView(StaffRequiredMixin, View):
    template_name = "flota/maintenance_type_form.html"

    def get(self, request):
        return render(request, self.template_name, {"form": MaintenanceTypeForm(), "maintenance_type": None})

    def post(self, request):
        form = MaintenanceTypeForm(request.POST)
        if form.is_valid():
            try:
                maintenance_type = create_maintenance_type(actor=request.user, data=form.cleaned_data)
            except ValidationError as error:
                _apply_validation_error(form, error)
            else:
                messages.success(request, "Tipul de mentenanță a fost creat.")
                return redirect("flota:maintenance_type_list")
        return render(
            request,
            self.template_name,
            {"form": form, "maintenance_type": None},
            status=400,
        )


class MaintenanceTypeEditView(StaffRequiredMixin, View):
    template_name = "flota/maintenance_type_form.html"

    def get_type(self, type_id):
        return get_object_or_404(MaintenanceType, pk=type_id)

    def get(self, request, type_id):
        maintenance_type = self.get_type(type_id)
        return render(
            request,
            self.template_name,
            {"form": MaintenanceTypeForm(instance=maintenance_type), "maintenance_type": maintenance_type},
        )

    def post(self, request, type_id):
        maintenance_type = self.get_type(type_id)
        form = MaintenanceTypeForm(request.POST, instance=maintenance_type)
        if form.is_valid():
            try:
                update_maintenance_type(actor=request.user, maintenance_type=maintenance_type, data=form.cleaned_data)
            except ValidationError as error:
                _apply_validation_error(form, error)
            else:
                messages.success(request, "Tipul de mentenanță a fost actualizat.")
                return redirect("flota:maintenance_type_list")
        return render(
            request,
            self.template_name,
            {"form": form, "maintenance_type": maintenance_type},
            status=400,
        )


class MaintenanceTypeArchiveView(StaffRequiredMixin, View):
    def post(self, request, type_id):
        maintenance_type = get_object_or_404(MaintenanceType, pk=type_id)
        try:
            archive_maintenance_type(actor=request.user, maintenance_type=maintenance_type)
        except ValidationError as error:
            messages.error(request, error.messages[0])
        else:
            messages.success(request, "Tipul de mentenanță a fost arhivat.")
        if _is_htmx(request):
            return render(
                request,
                MaintenanceTypeListView.partial_template_name,
                _maintenance_type_context(),
            )
        return redirect("flota:maintenance_type_list")
```

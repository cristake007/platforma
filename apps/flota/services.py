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


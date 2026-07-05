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

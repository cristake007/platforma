# Source snapshot

## `apps/flota/views.py`

Size: 12.0 KB

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


class FleetIndexView(LoginRequiredMixin, View):
    template_name = "flota/index.html"

    def get(self, request):
        archived_only = request.user.is_staff and request.GET.get("archived") == "1"
        base_queryset = visible_vehicles(user=request.user, include_archived=archived_only)
        filtered = filter_vehicles(base_queryset, request.GET)
        paginator = Paginator(filtered, 20)
        page = paginator.get_page(request.GET.get("page"))
        page.object_list = decorate_vehicle_rows(page.object_list)
        query = request.GET.copy()
        query.pop("page", None)
        summary_queryset = Vehicle.objects.all() if request.user.is_staff else visible_vehicles(user=request.user)
        return render(
            request,
            self.template_name,
            {
                "page": page,
                "summary": fleet_summary(queryset=summary_queryset),
                "filters": request.GET,
                "status_choices": Vehicle.Status.choices,
                "users": active_users() if request.user.is_staff else [],
                "archived_only": archived_only,
                "query_without_page": urlencode(query, doseq=True),
            },
        )


class VehicleDetailView(LoginRequiredMixin, View):
    template_name = "flota/vehicle_detail.html"

    def get(self, request, vehicle_id):
        vehicle = get_visible_vehicle(user=request.user, vehicle_id=vehicle_id)
        return render(
            request,
            self.template_name,
            {
                "vehicle": vehicle,
                "current_assignment": _current_assignment(vehicle),
                "deadline_rows": vehicle_deadline_rows(vehicle),
                "maintenance_records": vehicle.maintenance_records.select_related(
                    "maintenance_type", "created_by"
                ),
                "assignment_history": vehicle.assignments.select_related(
                    "assignee", "assigned_by", "ended_by"
                ),
            },
        )


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
        set_vehicle_archived(actor=request.user, vehicle=vehicle, archived=True)
        messages.success(request, "Vehiculul a fost arhivat, iar atribuirea curentă a fost încheiată.")
        return redirect("flota:vehicle_detail", vehicle_id=vehicle.pk)


class VehicleRestoreView(StaffRequiredMixin, View):
    def post(self, request, vehicle_id):
        vehicle = get_staff_vehicle(vehicle_id=vehicle_id)
        set_vehicle_archived(actor=request.user, vehicle=vehicle, archived=False)
        messages.success(request, "Vehiculul a fost restaurat și este neatribuit.")
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

    def get(self, request):
        return render(request, self.template_name, {"maintenance_types": MaintenanceType.objects.all()})


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
        return redirect("flota:maintenance_type_list")

```

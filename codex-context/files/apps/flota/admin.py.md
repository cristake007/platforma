# apps/flota/admin.py

Generated: `2026-07-05T21:21:12`

## Scope

- Real source file: `apps/flota/admin.py`
- App: `flota`
- App guide: `codex-context/apps/flota.md`
- Role: `backend`
- Size: 2287 bytes
- Source SHA-256: `bd0f66329685956957a66051a0708147374730733c73869fcbc1764a54db2cee`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

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

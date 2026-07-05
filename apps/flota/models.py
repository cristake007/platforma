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

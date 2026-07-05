# Source snapshot

## `apps/flota/tests.py`

Size: 10.9 KB

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

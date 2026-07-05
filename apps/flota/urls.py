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


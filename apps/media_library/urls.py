from django.urls import path

from .views import (
    MediaAssetContentView,
    MediaAssetDeleteView,
    MediaAssetListApiView,
    MediaAssetUploadApiView,
    MediaLibraryView,
)


app_name = "media_library"

urlpatterns = [
    path("", MediaLibraryView.as_view(), name="index"),
    path("api/assets/", MediaAssetListApiView.as_view(), name="api_assets"),
    path("api/assets/upload/", MediaAssetUploadApiView.as_view(), name="api_upload"),
    path("<uuid:asset_id>/continut/", MediaAssetContentView.as_view(), name="content"),
    path("<uuid:asset_id>/sterge/", MediaAssetDeleteView.as_view(), name="delete"),
]

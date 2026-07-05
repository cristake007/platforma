from django.contrib import admin

from .models import MediaAsset


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "kind", "mime_type", "size_bytes", "created_at")
    list_filter = ("kind", "mime_type")
    search_fields = ("name", "original_filename", "owner__username")
    readonly_fields = ("id", "sha256", "size_bytes", "width_px", "height_px", "created_at", "updated_at")


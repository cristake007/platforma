from django.apps import AppConfig


class MediaLibraryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.media_library"

    def ready(self):
        from . import signals  # noqa: F401


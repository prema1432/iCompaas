from django.apps import AppConfig


class SanitizedConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sanitized"

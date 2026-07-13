from django.apps import AppConfig


class NotificationAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "notification_app"

    # noinspection PyUnresolvedReferences

    def ready(self):
        pass     # Ensures signals are registered

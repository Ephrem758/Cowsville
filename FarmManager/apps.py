from django.apps import AppConfig
import os


class FarmManagerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "FarmManager"

    def ready(self):
        if os.environ.get("RUN_MAIN", None) != "true":  # Avoid duplicate schedulers
            from AlertSystem import updater

            updater.start()

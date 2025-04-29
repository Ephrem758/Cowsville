from django.apps import AppConfig
import os
import sys


class FarmManagerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "FarmManager"

    def ready(self):
        # Check if running a management command like migrate or makemigrations
        is_management_command = any(
            cmd in sys.argv for cmd in ['makemigrations', 'migrate', 'showmigrations']
        )
        
        if os.environ.get("RUN_MAIN", None) != "true" and not is_management_command:
            try:
                from AlertSystem import updater
                updater.start()
            except Exception as e:
                # Handle potential errors during updater start, e.g., missing dependencies
                print(f"Warning: Could not start AlertSystem updater: {e}")

from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError


class EduvaultConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eduvault'

    def ready(self):
        from django.contrib.auth import get_user_model

        try:
            User = get_user_model()

            ADMIN_USERNAME = "mohan"
            ADMIN_PASSWORD = "admin123"
            ADMIN_EMAIL = "mohanrgbl6629@gmail.com"

            if not User.objects.filter(username=ADMIN_USERNAME).exists():
                User.objects.create_superuser(
                    username=ADMIN_USERNAME,
                    email=ADMIN_EMAIL,
                    password=ADMIN_PASSWORD
                )

        except (OperationalError, ProgrammingError):
            # Database tables not ready yet (during migrate)
            pass
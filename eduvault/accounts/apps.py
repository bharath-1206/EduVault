from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        from django.contrib.auth import get_user_model
        from django.db.utils import OperationalError, ProgrammingError

        try:
            User = get_user_model()

            if not User.objects.filter(username="admin").exists():
                User.objects.create_superuser(
                    username="mohan",
                    email="mohanrgbl6629@gmail.com",
                    password="admin123"
                )
        except (OperationalError, ProgrammingError):
            # Database might not be ready during migration
            pass
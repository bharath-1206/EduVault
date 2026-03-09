from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'

from django.contrib.auth import get_user_model
from django.db.utils import OperationalError

try:
    User = get_user_model()

    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(
            username="mohan",
            email="mohanrgbl6629@gmail.com",
            password="mohang@1307"
        )
except OperationalError:
    pass
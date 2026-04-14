from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import Staff


@receiver(post_save, sender=Staff)
def create_user_for_staff(sender, instance, created, **kwargs):

    if created:
        if not User.objects.filter(username=instance.staff_id).exists():

            User.objects.create_user(
                username=instance.staff_id,
                password="1234"   # default password
            )
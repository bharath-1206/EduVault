from django.db import models


class Staff(models.Model):

    name = models.CharField(max_length=100)

    staff_id = models.CharField(max_length=20, unique=True)

    # ✅ NEW PASSWORD FIELD
    password = models.CharField(max_length=100)

    branch = models.ForeignKey(
        "academics.Branche",
        on_delete=models.CASCADE
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
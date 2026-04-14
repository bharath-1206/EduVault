from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Staff(models.Model):

    ROLE_CHOICES = [
        ("cycle", "Cycle Staff"),
        ("branch", "Branch Staff"),
        ("hod", "HOD"),
    ]

    CYCLE_CHOICES = [
        ("P", "P Cycle"),
        ("C", "C Cycle"),
    ]

    name = models.CharField(max_length=100)
    staff_id = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=255)

    role_type = models.CharField(max_length=10, choices=ROLE_CHOICES)

    cycle = models.CharField(max_length=1, choices=CYCLE_CHOICES, blank=True, null=True)

    branch = models.ForeignKey(
        "academics.Branche",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    # ✅ PASSWORD CHECK METHOD (NEW)
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def save(self, *args, **kwargs):

        # 🔐 HASH ONLY IF NOT HASHED
        if not self.password.startswith("pbkdf2_"):
            self.password = make_password(self.password)

        if self.role_type == "hod":
            existing_hod = Staff.objects.filter(
                role_type="hod",
                branch=self.branch
            ).exclude(pk=self.pk)

            if existing_hod.exists():
                raise ValueError("HOD already exists for this branch.")

        super().save(*args, **kwargs)
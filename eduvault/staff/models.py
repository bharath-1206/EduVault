from django.db import models


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
    password = models.CharField(max_length=100)

    role_type = models.CharField(max_length=10, choices=ROLE_CHOICES)

    # ✅ For cycle staff
    cycle = models.CharField(
        max_length=1,
        choices=CYCLE_CHOICES,
        blank=True,
        null=True
    )

    # ✅ For branch staff
    branch = models.ForeignKey(
        "academics.Branche",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        if self.role_type == "hod":
            existing_hod = Staff.objects.filter(
                role_type="hod",
                branch=self.branch
            ).exclude(pk=self.pk)

            if existing_hod.exists():
                raise ValueError("HOD already exists for this branch.")

        super().save(*args, **kwargs)
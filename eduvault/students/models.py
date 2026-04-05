from django.db import models
from academics.models import Branche, Scheme
from accounts.models import ActivityLog


class Student(models.Model):

    name = models.CharField(max_length=100)
    usn = models.CharField(max_length=20, unique=True)

    semester = models.IntegerField(default=1)  # ✅ NEW

    branche = models.ForeignKey(
        Branche,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    scheme = models.ForeignKey(
        Scheme,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    section = models.ForeignKey(
        "academics.Section",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):

        is_new = self.pk is None

        # Detect scheme
        try:
            scheme_digits = self.usn[3:5]
            scheme_year = int("20" + scheme_digits)
            self.scheme = Scheme.objects.get(year=scheme_year)
        except:
            pass

        # Detect branch
        try:
            branch_code = self.usn[5:7]
            self.branche = Branche.objects.get(code=branch_code)
        except:
            pass

        super().save(*args, **kwargs)

        if is_new:
            ActivityLog.objects.create(
                user_type="admin",
                user_id="admin",
                action=f"Added student: {self.usn}"
            )

    def __str__(self):
        return f"{self.name} ({self.usn})"

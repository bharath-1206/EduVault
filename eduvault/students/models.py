from django.db import models
from academics.models import Branche, Scheme
from accounts.models import ActivityLog   # ✅ ADD THIS


class Student(models.Model):

    name = models.CharField(max_length=100)
    usn = models.CharField(max_length=20, unique=True)

    branche = models.ForeignKey(
        Branche,
        on_delete=models.CASCADE,
        verbose_name="Branch",
        blank=True,
        null=True
    )

    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):

        # ✅ Detect if new student
        is_new = self.pk is None

        # Detect scheme from USN
        try:
            scheme_digits = self.usn[3:5]
            self.scheme = int("20" + scheme_digits)
        except:
            pass

        # Detect branch from USN
        try:
            branch_code = self.usn[5:7]
            branch = Branche.objects.get(code=branch_code)
            self.branche = branch
        except Branche.DoesNotExist:
            pass

        # Save first
        super().save(*args, **kwargs)

        # ✅ LOG ONLY IF NEW STUDENT
        if is_new:
            ActivityLog.objects.create(
                user_type="admin",
                user_id="admin",
                action=f"Added student: {self.usn}"
            )

    def __str__(self):
        return f"{self.name} ({self.usn})"
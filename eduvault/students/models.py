from django.db import models
from academics.models import Branche, Scheme
from accounts.models import ActivityLog


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

    scheme = models.ForeignKey(
        Scheme,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):

        # ✅ Check if new student
        is_new = self.pk is None

        # 🔹 Detect scheme from USN
        try:
            scheme_digits = self.usn[3:5]   # Example: "25"
            scheme_year = int("20" + scheme_digits)  # 2025

            scheme_obj = Scheme.objects.get(year=scheme_year)
            self.scheme = scheme_obj

        except Scheme.DoesNotExist:
            print(f"Scheme {scheme_year} not found in DB")
        except Exception as e:
            print("Scheme detection error:", e)

        # 🔹 Detect branch from USN
        try:
            branch_code = self.usn[5:7]   # Example: "IC"
            branch_obj = Branche.objects.get(code=branch_code)
            self.branche = branch_obj

        except Branche.DoesNotExist:
            print(f"Branch {branch_code} not found in DB")
        except Exception as e:
            print("Branch detection error:", e)

        # ✅ Save student
        super().save(*args, **kwargs)

        # ✅ Log only when new student is added
        if is_new:
            ActivityLog.objects.create(
                user_type="admin",
                user_id="admin",
                action=f"Added student: {self.usn}"
            )

    def __str__(self):
        return f"{self.name} ({self.usn})"
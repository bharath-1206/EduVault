from django.db import models
from academics.models import Branche, Scheme
from accounts.models import ActivityLog


class Student(models.Model):
    is_diploma = models.BooleanField(default=False)
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

        # =========================
        # DETECT SCHEME (FINAL)
        # =========================
        try:
            # 🔥 DO NOT override if already set (important for year-back)
            if not self.scheme:

                scheme_digits = self.usn[3:5]
                scheme_year = int("20" + scheme_digits)

                # ✅ Diploma → previous year
                if self.is_diploma:
                    scheme_year = scheme_year - 1

                scheme_obj = Scheme.objects.filter(year=scheme_year).first()

                if scheme_obj:
                    self.scheme = scheme_obj
                else:
                    print(f"⚠️ Scheme {scheme_year} not found for USN {self.usn}")

        except Exception as e:
            print(f"❌ Scheme error for {self.usn}: {e}")

        # =========================
        # DETECT BRANCH
        # =========================
        try:
            branch_code = self.usn[5:7]

            branch_obj = Branche.objects.filter(code=branch_code).first()

            if branch_obj:
                self.branche = branch_obj
            else:
                print(f"⚠️ Branch {branch_code} not found for USN {self.usn}")

        except Exception as e:
            print(f"❌ Branch detection error for {self.usn}: {e}")

        super().save(*args, **kwargs)

        if is_new:
            ActivityLog.objects.create(
                user_type="admin",
                user_id="admin",
                action=f"Added student: {self.usn}"
            )

    def __str__(self):
        return f"{self.name} ({self.usn})"
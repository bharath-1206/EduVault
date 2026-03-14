from django.db import models
from academics.models import Branche,Scheme


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

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.usn})"
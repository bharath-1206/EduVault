from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=100)
    usn = models.CharField(max_length=20, unique=True)
    branche = models.ForeignKey("academics.Branche", on_delete=models.CASCADE,  verbose_name="Branch",blank=True, null=True)

    def save(self, *args, **kwargs):
        branche_code = self.usn[5:7]

        from academics.models import Branche
        try:
            branche = Branche.objects.get(code=branche_code)
            self.branche = branche
        except Branche.DoesNotExist:
            pass

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.usn})"

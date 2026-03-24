from django.db import models
from cloudinary.models import CloudinaryField
from academics.models import Subject, Branche


class Material(models.Model):

    CYCLE_CHOICES = [
        ("P", "P Cycle"),
        ("C", "C Cycle"),
    ]

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

    file = CloudinaryField(resource_type="raw")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # ✅ NEW
    cycle = models.CharField(max_length=1, choices=CYCLE_CHOICES, null=True, blank=True)
    branch = models.ForeignKey(Branche, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

class CycleAssignment(models.Model):
    branch = models.ForeignKey("academics.Branche", on_delete=models.CASCADE)
    scheme = models.ForeignKey("academics.Scheme", on_delete=models.CASCADE)  # ✅ NEW
    cycle = models.CharField(max_length=1, choices=[("P", "P"), ("C", "C")])

    def __str__(self):
        return f"{self.branch.name} ({self.scheme.year}) → {self.cycle}"
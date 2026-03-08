from django.db import models
from cloudinary.models import CloudinaryField

class Material(models.Model):

    title = models.CharField(max_length=200)

    branche = models.ForeignKey(
        "academics.Branche",
        on_delete=models.CASCADE,
    verbose_name = "Branch"
    )

    semester = models.ForeignKey(
        "academics.Semester",
        on_delete=models.CASCADE
    )

    subject = models.ForeignKey(
        "academics.Subject",
        on_delete=models.CASCADE
    )

    file = CloudinaryField('file', resource_type='raw')

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
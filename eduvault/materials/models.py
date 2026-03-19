from django.db import models
from cloudinary.models import CloudinaryField

from django.db import models
from academics.models import Subject

from cloudinary.models import CloudinaryField



class Material(models.Model):



    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)



    file = CloudinaryField(resource_type="raw")

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
from django.db import models
class ActivityLog(models.Model):

    user_type = models.CharField(max_length=20)   # staff / admin
    user_id = models.CharField(max_length=50)

    action = models.CharField(max_length=255)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_type} - {self.user_id} - {self.action}"
# Create your models here.

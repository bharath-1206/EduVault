from django.db import models


class Staff(models.Model):

    name = models.CharField(max_length=100)

    staff_id = models.CharField(max_length=20, unique=True)

    branch = models.ForeignKey(
        "academics.Branche",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
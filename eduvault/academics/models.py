from django.db import models

class Branche(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Branch"
        verbose_name_plural = "Branches"

    def __str__(self):
        return self.name


class Semester(models.Model):
    number = models.IntegerField()

    def __str__(self):
        return f"Semester {self.number}"

class Subject(models.Model):
    name = models.CharField(max_length=200)
    branch = models.ForeignKey(Branche, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
# Create your models here.

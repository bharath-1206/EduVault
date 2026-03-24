from django.db import models

class Branche(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Branch"
        verbose_name_plural = "Branches"

    def __str__(self):
        return self.name

class Scheme(models.Model):

    year = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.year)

class Semester(models.Model):
    number = models.IntegerField()

    def __str__(self):
        return f"Semester {self.number}"

class Subject(models.Model):
    name = models.CharField(max_length=200)
    branch = models.ForeignKey(Branche, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE)

    def __str__(self):
        branch_code = self.branch.code if self.branch else "N/A"
        semester_number = self.semester.number if self.semester else "?"

        return f"{self.name} (Sem {semester_number} - {branch_code})"
# Create your models here.
from django.db import models



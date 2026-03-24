from django.contrib import admin
from .models import Student
from accounts.admin_logger import LoggableAdminMixin


@admin.register(Student)
class StudentAdmin(LoggableAdminMixin, admin.ModelAdmin):
    list_display = ("name", "usn", "branche", "semester")
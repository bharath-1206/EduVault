from django.contrib import admin
from .models import Staff
from accounts.admin_logger import LoggableAdminMixin


@admin.register(Staff)
class StaffAdmin(LoggableAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'staff_id', 'role_type', 'cycle', 'branch', 'is_active')
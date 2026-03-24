from django.contrib import admin
from .models import Material, CycleAssignment
from accounts.admin_logger import LoggableAdminMixin


@admin.register(Material)
class MaterialAdmin(LoggableAdminMixin, admin.ModelAdmin):
    list_display = ("title", "subject", "uploaded_at")


@admin.register(CycleAssignment)
class CycleAssignmentAdmin(LoggableAdminMixin, admin.ModelAdmin):
    pass
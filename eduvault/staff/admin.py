from django.contrib import admin
from .models import Staff


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'staff_id', 'role_type', 'cycle', 'branch', 'is_active')
    list_editable = ('is_active',)
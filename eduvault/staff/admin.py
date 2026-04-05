from django.contrib import admin
from .models import Staff
from accounts.admin_logger import LoggableAdminMixin


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):

    list_display = ('name', 'staff_id', 'role_type', 'branch', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('role_type', 'branch')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        # 🔥 Hide branch for cycle staff
        if obj and obj.role_type == "cycle":
            form.base_fields['branch'].required = False

        return form
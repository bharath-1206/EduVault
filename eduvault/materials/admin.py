from django.contrib import admin
from .models import Material,Subject
from accounts.admin_logger import LoggableAdminMixin


@admin.register(Material)
class MaterialAdmin(LoggableAdminMixin, admin.ModelAdmin):
    list_display = ("title", "subject", "section", "uploaded_at")

    fields = ("title", "subject", "section", "file")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "subject":
            kwargs["queryset"] = Subject.objects.select_related("scheme", "semester", "branch")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)




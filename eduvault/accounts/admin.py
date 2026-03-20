from django.contrib import admin
from django.contrib import admin
from .models import ActivityLog


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):

    list_display = ("user_type", "user_id", "action", "timestamp")

    list_filter = ("user_type", "timestamp")

    search_fields = ("user_id", "action")

    ordering = ("-timestamp",)

    # prevent manual editing
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
# Register your models here.

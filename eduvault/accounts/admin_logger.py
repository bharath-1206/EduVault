from accounts.models import ActivityLog


class LoggableAdminMixin:

    def save_model(self, request, obj, form, change):
        action = "updated" if change else "added"

        super().save_model(request, obj, form, change)

        ActivityLog.objects.create(
            user_type="admin",
            user_id=request.user.username,
            action=f"Admin {action} {obj._meta.model_name}: {obj}"
        )

    def delete_model(self, request, obj):
        ActivityLog.objects.create(
            user_type="admin",
            user_id=request.user.username,
            action=f"Admin deleted {obj._meta.model_name}: {obj}"
        )

        super().delete_model(request, obj)
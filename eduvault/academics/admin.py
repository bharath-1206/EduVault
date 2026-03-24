from django.contrib import admin
from .models import Branche, Semester, Subject, Scheme


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "get_branch_code", "semester", "scheme")

    def get_branch_code(self, obj):
        return obj.branch.code if obj.branch else "-"

    get_branch_code.short_description = "Branch"


admin.site.register(Branche)
admin.site.register(Semester)
admin.site.register(Scheme)
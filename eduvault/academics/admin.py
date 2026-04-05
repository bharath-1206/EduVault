from django.contrib import admin
from .models import Branche, Semester, Subject, Scheme,Section
from accounts.admin_logger import LoggableAdminMixin


@admin.register(Branche)
class BrancheAdmin(LoggableAdminMixin, admin.ModelAdmin):
    pass


@admin.register(Semester)
class SemesterAdmin(LoggableAdminMixin, admin.ModelAdmin):
    pass


@admin.register(Subject)
class SubjectAdmin(LoggableAdminMixin, admin.ModelAdmin):

    list_display = ("name", "semester", "branch", "scheme")

    fields = ("name", "scheme", "semester", "branch")  # 👈 ADD THIS


@admin.register(Scheme)
class SchemeAdmin(LoggableAdminMixin, admin.ModelAdmin):
    pass

@admin.register(Section)
class SectionAdmin(LoggableAdminMixin, admin.ModelAdmin):
    list_display = ("name", "branch", "scheme")
    list_filter = ("branch", "scheme")
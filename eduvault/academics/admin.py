from django.contrib import admin
from .models import Branche, Semester, Subject, Scheme
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


@admin.register(Scheme)
class SchemeAdmin(LoggableAdminMixin, admin.ModelAdmin):
    pass
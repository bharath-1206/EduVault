from django.contrib import admin
from .models import Student


class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "usn", "branche")
    list_filter = ("branche",)
    search_fields = ("name", "usn")


admin.site.register(Student, StudentAdmin)
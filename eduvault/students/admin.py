from django.contrib import admin
from .models import Student


@admin.action(description="Promote students to next semester")
def promote_students(modeladmin, request, queryset):
    for student in queryset:
        if student.semester < 8:
            student.semester += 1
            student.save()


class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "usn", "branche", "semester")
    actions = [promote_students]


admin.site.register(Student, StudentAdmin)
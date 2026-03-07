from django.urls import path
from .views import semester_subjects, subject_materials

urlpatterns = [

    path(
        "semester/<int:semester_number>/<int:branch_id>/",
        semester_subjects,
        name="semester_subjects"
    ),

    path(
        "subject/<int:subject_id>/",
        subject_materials,
        name="subject_materials"
    ),

]
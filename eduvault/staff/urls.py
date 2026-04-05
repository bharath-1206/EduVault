from django.urls import path
from . import views


urlpatterns = [

    # -----------------------------------
    # AUTH / ENTRY
    # -----------------------------------
    path('', views.staff_login, name='staff_login'),

    # -----------------------------------
    # STAFF DASHBOARD
    # -----------------------------------
    path('dashboard/', views.staff_dashboard, name='staff_dashboard'),

    # -----------------------------------
    # MATERIALS (COMMON)
    # -----------------------------------
    path('upload/', views.upload_material, name='upload_material'),
    path('delete/<int:material_id>/', views.delete_material, name='delete_material'),

    # -----------------------------------
    # AJAX FILTERS
    # -----------------------------------
    path('get-subjects/', views.get_subjects, name='get_subjects'),
    path('get-sections/', views.get_sections, name='get_sections'),

    # -----------------------------------
    # HOD DASHBOARD
    # -----------------------------------
    path('hod/', views.hod_dashboard, name='hod_dashboard'),

    # -----------------------------------
    # HOD → STUDENTS
    # -----------------------------------
    path('hod/students/', views.hod_students, name='hod_students'),
    path('hod/add-student/', views.add_student, name='add_student'),
    path('hod/edit-student/<int:student_id>/', views.edit_student, name='edit_student'),
    path('hod/delete-student/<int:student_id>/', views.delete_student, name='delete_student'),

    # -----------------------------------
    # HOD → STAFF
    # -----------------------------------
    path('hod/staff/', views.hod_staff_list, name='hod_staff_list'),
    path('hod/add-staff/', views.add_staff, name='add_staff'),
    path('hod/edit-staff/<int:id>/', views.edit_staff, name='edit_staff'),
    path('hod/delete-staff/<int:id>/', views.delete_staff, name='delete_staff'),

    # -----------------------------------
    # HOD → BULK CSV
    # -----------------------------------
    path('hod/upload-students/', views.upload_students_csv, name='upload_students_csv'),

    # -----------------------------------
    # HOD → ACADEMICS
    # -----------------------------------
    path('hod/add-section/', views.add_section, name='add_section'),
    path('hod/add-subject/', views.add_subject, name='add_subject'),
]
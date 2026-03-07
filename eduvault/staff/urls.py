from django.urls import path
from .views import staff_login, upload_material, get_subjects,delete_material

urlpatterns = [

    path('', staff_login, name='staff_login'),

    path('upload/', upload_material, name='upload_material'),

    path('get-subjects/', get_subjects, name='get_subjects'),
    path('delete/<int:material_id>/', delete_material, name='delete_material'),

]
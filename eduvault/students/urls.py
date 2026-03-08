from django.urls import path
from .views import student_dashboard

urlpatterns = [
    path('', student_dashboard, name="student_dashboard"),
]
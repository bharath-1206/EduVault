from django.shortcuts import render, redirect
from .models import Student

def student_dashboard(request):

    usn = request.session.get("student_id")

    if not usn:
        return redirect("/")   # not logged in

    try:
        student = Student.objects.get(usn=usn)
    except Student.DoesNotExist:
        return redirect("/")

    return render(request, "dashboard.html", {"student": student})
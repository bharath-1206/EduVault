from django.shortcuts import render, redirect

from .models import Student
from academics.models import Semester
from materials.models import Material


# -----------------------------------
# STUDENT DASHBOARD
# -----------------------------------
def student_dashboard(request):

    usn = request.session.get("student_id")

    if not usn:
        return redirect("/")

    student = Student.objects.get(usn=usn)
    semesters = Semester.objects.all()

    # -----------------------------------
    # ✅ STRICT SECTION FILTER
    # -----------------------------------
    materials = Material.objects.filter(
        section=student.section
    )

    context = {
        "student": student,
        "semesters": semesters,
        "materials": materials,
    }

    return render(request, "dashboard.html", context)
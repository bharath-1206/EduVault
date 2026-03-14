from django.shortcuts import render, redirect
from .models import Student
from academics.models import Semester


def student_dashboard(request):

    usn = request.session.get("student_id")

    if not usn:
        return redirect("/")

    student = Student.objects.get(usn=usn)

    semesters = Semester.objects.all()

    branch_id = None
    if student.branche:
        branch_id = student.branche.id

    # Store scheme in session
    request.session["scheme"] = student.scheme.year

    context = {
        "student": student,
        "semesters": semesters,
        "branch_id": branch_id,
        "scheme": student.scheme
    }

    return render(request, "dashboard.html", context)
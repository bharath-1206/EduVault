from django.shortcuts import render, redirect
from django.db.models import Q

from .models import Student
from academics.models import Semester
from materials.models import Material, CycleAssignment


# -----------------------------------
# GET CURRENT CYCLE
# -----------------------------------
def get_cycle(student):

    try:
        assignment = CycleAssignment.objects.get(
            branch=student.branche,
            scheme=student.scheme
        )

        if student.semester == 1:
            return assignment.cycle

        elif student.semester == 2:
            return "C" if assignment.cycle == "P" else "P"

        else:
            return None

    except:
        return None


# -----------------------------------
# STUDENT DASHBOARD
# -----------------------------------
def student_dashboard(request):

    usn = request.session.get("student_id")

    if not usn:
        return redirect("/")

    student = Student.objects.get(usn=usn)
    semesters = Semester.objects.all()

    cycle = get_cycle(student)

    # -----------------------------------
    # MATERIAL FILTER LOGIC (UPDATED 🔥)
    # -----------------------------------

    if student.semester == 1:
        # Only current cycle
        materials = Material.objects.filter(cycle=cycle)

    elif student.semester == 2:
        # Both P and C cycles
        materials = Material.objects.filter(cycle__in=["P", "C"])

    else:
        # P + C + Branch materials
        materials = Material.objects.filter(
            Q(cycle__in=["P", "C"]) |
            Q(branch=student.branche)
        )

    context = {
        "student": student,
        "semesters": semesters,
        "materials": materials,
        "cycle": cycle,  # optional (useful in UI if needed)
    }

    return render(request, "dashboard.html", context)
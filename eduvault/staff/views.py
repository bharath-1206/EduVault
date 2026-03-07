from django.shortcuts import render, redirect
from django.http import JsonResponse

from .models import Staff
from materials.models import Material
from academics.models import Branche, Semester, Subject


def staff_login(request):

    if request.method == "POST":

        staff_id = request.POST.get("staff_id")

        try:
            staff = Staff.objects.get(staff_id=staff_id)

            # store staff session
            request.session["staff_id"] = staff.staff_id

            semesters = Semester.objects.all()
            subjects = Subject.objects.filter(branch=staff.branch)

            # fetch uploaded materials of this branch
            materials = Material.objects.filter(branche_id=staff.branch.id)

            return render(
                request,
                "staff_dashboard.html",
                {
                    "staff": staff,
                    "semesters": semesters,
                    "subjects": subjects,
                    "materials": materials
                }
            )

        except Staff.DoesNotExist:
            return render(request, "staff_login.html", {"error": "Invalid Staff ID"})

    return render(request, "staff_login.html")


def upload_material(request):

    if request.method == "POST":

        title = request.POST.get("title")
        semester_id = request.POST.get("semester")
        subject_id = request.POST.get("subject")
        file = request.FILES.get("file")

        staff = Staff.objects.get(
            staff_id=request.session.get("staff_id")
        )

        Material.objects.create(
            title=title,
            branche=staff.branch,
            semester_id=semester_id,
            subject_id=subject_id,
            file=file
        )

        return redirect("/staff/")

    return redirect("/staff/")


def get_subjects(request):

    semester_id = request.GET.get("semester")
    branch_id = request.GET.get("branch")

    subjects = Subject.objects.filter(
        semester_id=semester_id,
        branch_id=branch_id
    )

    data = []

    for subject in subjects:
        data.append({
            "id": subject.id,
            "name": subject.name
        })

    return JsonResponse(data, safe=False)


def delete_material(request, material_id):

    material = Material.objects.get(id=material_id)
    material.delete()

    return redirect("/staff/")
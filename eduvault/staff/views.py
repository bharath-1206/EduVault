from django.shortcuts import render, redirect
from django.http import JsonResponse

from .models import Staff
from materials.models import Material
from academics.models import Branche, Semester, Subject


def staff_login(request):

    # Check if staff session exists
    if "staff_id" not in request.session:
        return redirect("/")

    staff_id = request.session.get("staff_id")

    staff = Staff.objects.get(staff_id=staff_id)

    semesters = Semester.objects.all()

    subjects = Subject.objects.filter(branch=staff.branch)

    materials = Material.objects.filter(branche=staff.branch)

    return render(
        request,
        "staff_dashboard.html",
        {
            "staff": staff,
            "semesters": semesters,
            "subjects": subjects,
            "materials": materials,
        },
    )
import cloudinary.uploader
from django.shortcuts import redirect
from materials.models import Material


from django.contrib import messages

from django.contrib import messages
from django.shortcuts import redirect
from materials.models import Material
from .models import Staff


def upload_material(request):
    if "staff_id" not in request.session:
        return redirect("/")
    if request.method == "POST":

        title = request.POST.get("title")
        semester_id = request.POST.get("semester")
        subject_id = request.POST.get("subject")
        file = request.FILES.get("file")

        # Allowed file types
        allowed_types = ["pdf", "ppt", "pptx", "doc", "docx"]

        file_extension = file.name.split(".")[-1].lower()

        if file_extension not in allowed_types:
            messages.error(request, "Only PDF, PPT, DOC files are allowed.")
            return redirect("/staff/")

        # File size limit (20MB)
        if file.size > 20 * 1024 * 1024:
            messages.error(request, "File size must be less than 20MB.")
            return redirect("/staff/")

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

        messages.success(request, "Material uploaded successfully.")

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


import cloudinary.uploader
from django.shortcuts import redirect
from materials.models import Material


def delete_material(request, material_id):

    material = Material.objects.get(id=material_id)

    # Delete file from Cloudinary
    if material.file:
        cloudinary.uploader.destroy(material.file.public_id)

    # Delete record from database
    material.delete()

    return redirect("/staff/")
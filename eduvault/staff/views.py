from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages

from .models import Staff
from materials.models import Material
from academics.models import Scheme, Semester, Subject

import cloudinary.uploader


# -----------------------------------
# STAFF DASHBOARD
# -----------------------------------
def staff_login(request):

    staff_id = request.session.get("staff_id")

    # ❌ Not logged in
    if not staff_id:
        return redirect("/")

    staff = Staff.objects.get(staff_id=staff_id)

    # ❌ BLOCK INACTIVE STAFF
    if not staff.is_active:
        request.session.flush()
        messages.error(request, "Your account is inactive.")
        return redirect("/")

    semesters = Semester.objects.all()
    schemes = Scheme.objects.all()

    materials = Material.objects.filter(subject__branch=staff.branch)

    return render(
        request,
        "staff_dashboard.html",
        {
            "staff": staff,
            "semesters": semesters,
            "schemes": schemes,
            "materials": materials,
        },
    )


# -----------------------------------
# UPLOAD MATERIAL
# -----------------------------------
def upload_material(request):

    staff_id = request.session.get("staff_id")

    if not staff_id:
        return redirect("/")

    staff = Staff.objects.get(staff_id=staff_id)

    # ❌ BLOCK INACTIVE STAFF
    if not staff.is_active:
        request.session.flush()
        messages.error(request, "Your account is inactive.")
        return redirect("/")

    if request.method == "POST":

        title = request.POST.get("title")
        subject_id = request.POST.get("subject")
        file = request.FILES.get("file")

        if not file:
            messages.error(request, "No file selected.")
            return redirect("/staff/")

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

        Material.objects.create(
            title=title,
            subject_id=subject_id,
            file=file
        )

        messages.success(request, "Material uploaded successfully.")
        return redirect("/staff/")


# -----------------------------------
# GET SUBJECTS (AJAX)
# -----------------------------------
def get_subjects(request):

    scheme_id = request.GET.get("scheme")

    subjects = Subject.objects.filter(scheme_id=scheme_id)

    data = []

    for subject in subjects:
        data.append({
            "id": subject.id,
            "name": subject.name
        })

    return JsonResponse(data, safe=False)


# -----------------------------------
# DELETE MATERIAL
# -----------------------------------
def delete_material(request, material_id):

    staff_id = request.session.get("staff_id")

    if not staff_id:
        return redirect("/")

    staff = Staff.objects.get(staff_id=staff_id)

    # ❌ BLOCK INACTIVE STAFF
    if not staff.is_active:
        request.session.flush()
        messages.error(request, "Your account is inactive.")
        return redirect("/")

    material = Material.objects.get(id=material_id)

    if material.file:
        cloudinary.uploader.destroy(material.file.public_id)

    material.delete()

    return redirect("/staff/")
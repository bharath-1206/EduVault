from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages

from .models import Staff
from materials.models import Material
from academics.models import Scheme, Semester, Subject
from accounts.models import ActivityLog
from django.db.models import Q
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

    if staff.role_type == "cycle":
        materials = Material.objects.filter(cycle=staff.cycle)
    else:
        materials = Material.objects.filter(branch=staff.branch)

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

        material = Material.objects.create(
            title=title,
            subject_id=subject_id,
            file=file
        )

        if staff.role_type == "cycle":
            material.cycle = staff.cycle
        else:
            material.branch = staff.branch

        material.save()
        ActivityLog.objects.create(
            user_type="staff",
            user_id=staff.staff_id,
            action=f"Uploaded material: {title}"
        )
        messages.success(request, "Material uploaded successfully.")
        return redirect("/staff/")


# -----------------------------------
# GET SUBJECTS (AJAX)
# -----------------------------------


def get_subjects(request):

    scheme_id = request.GET.get("scheme")
    staff_id = request.session.get("staff_id")

    if not staff_id:
        return JsonResponse([], safe=False)

    staff = Staff.objects.get(staff_id=staff_id)

    # -----------------------------------
    # FILTER SUBJECTS BASED ON ROLE
    # -----------------------------------

    if staff.role_type == "cycle":
        # Only sem 1 & 2 subjects
        subjects = Subject.objects.filter(
            scheme_id=scheme_id,
            semester__number__in=[1, 2]
        )

    else:
        # Only branch subjects (sem 3+)
        subjects = Subject.objects.filter(
            scheme_id=scheme_id,
            branch=staff.branch,
            semester__number__gte=3
        )

    data = []

    for subject in subjects:
        data.append({
            "id": subject.id,
            "name": f"{subject.name} (Sem {subject.semester.number})"
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

    ActivityLog.objects.create(
        user_type="staff",
        user_id=staff.staff_id,
        action=f"Deleted material: {material.title}"
    )
    material.delete()

    return redirect("/staff/")
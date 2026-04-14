from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Staff
from materials.models import Material
from academics.models import Scheme, Semester, Subject, Section
from students.models import Student
from accounts.models import ActivityLog

import cloudinary.uploader
import csv
from io import TextIOWrapper


# -----------------------------------
# AUTH HELPER
# -----------------------------------
def get_staff(request):
    if not request.user.is_authenticated:
        return None
    return Staff.objects.filter(staff_id=request.user.username).first()


# -----------------------------------
# LOGIN
# -----------------------------------
def staff_login(request):

    if request.user.is_authenticated:
        return redirect("/staff/dashboard/")

    if request.method == "POST":
        staff_id = request.POST.get("usn")
        password = request.POST.get("password")

        user = authenticate(request, username=staff_id, password=password)

        if user:
            login(request, user)

            staff = Staff.objects.filter(staff_id=staff_id).first()

            if not staff or not staff.is_active:
                logout(request)
                messages.error(request, "Inactive account")
                return redirect("/")

            if staff.role_type == "hod":
                return redirect("/staff/hod/")
            return redirect("/staff/dashboard/")

        messages.error(request, "Invalid credentials")

    return render(request, "login.html")


def staff_logout(request):
    logout(request)
    return redirect("/")


# -----------------------------------
# DASHBOARD
# -----------------------------------
@login_required
def staff_dashboard(request):

    staff = get_staff(request)

    if not staff:
        return redirect("/")

    if staff.role_type == "hod":
        return redirect("/staff/hod/")

    schemes = Scheme.objects.all()

    if staff.role_type == "cycle":
        materials = Material.objects.filter(subject__semester__number__in=[1, 2])
        sections = Section.objects.all()
    else:
        materials = Material.objects.filter(
            section__branch=staff.branch,
            subject__semester__number__gt=2
        )
        sections = Section.objects.filter(branch=staff.branch)

    return render(request, "staff_dashboard.html", {
        "staff": staff,
        "schemes": schemes,
        "materials": materials,
        "sections": sections
    })


# -----------------------------------
# HOD DASHBOARD
# -----------------------------------
@login_required
def hod_dashboard(request):

    staff = get_staff(request)

    if not staff or staff.role_type != "hod":
        return redirect("/staff/dashboard/")

    return render(request, "hod_dashboard.html", {
        "staff": staff,
        "schemes": Scheme.objects.all(),
        "semesters": Semester.objects.all(),
        "materials": Material.objects.filter(section__branch=staff.branch)
    })


# -----------------------------------
# MATERIALS
# -----------------------------------
@login_required
def view_materials(request):

    staff = get_staff(request)

    if staff.role_type == "cycle":
        materials = Material.objects.filter(subject__semester__number__in=[1, 2])
    else:
        materials = Material.objects.filter(
            section__branch=staff.branch,
            subject__semester__number__gt=2
        )

    return render(request, "view_materials.html", {
        "materials": materials,
        "staff": staff
    })


@login_required
def upload_material(request):

    staff = get_staff(request)

    if request.method == "POST":

        title = request.POST.get("title")
        subject_id = request.POST.get("subject")
        section_id = request.POST.get("section")
        file = request.FILES.get("file")

        try:
            subject = Subject.objects.get(id=subject_id)

            if staff.role_type != "cycle":
                if subject.branch != staff.branch:
                    raise Exception("Invalid subject")

                if subject.semester.number <= 2:
                    raise Exception("Branch cannot upload cycle")

            section = Section.objects.get(id=section_id)

            Material.objects.create(
                title=title,
                subject=subject,
                section=section,
                file=file
            )

            messages.success(request, "Uploaded")

        except Exception as e:
            messages.error(request, str(e))

    return redirect("/staff/dashboard/")


@login_required
def delete_material(request, material_id):

    try:
        material = Material.objects.get(id=material_id)

        if material.file:
            cloudinary.uploader.destroy(material.file.public_id)

        material.delete()

    except:
        pass

    return redirect("/staff/dashboard/")


# -----------------------------------
# FILTER APIs
# -----------------------------------
@login_required
def get_subjects(request):

    staff = get_staff(request)
    scheme_id = request.GET.get("scheme")

    if staff.role_type == "cycle":
        subjects = Subject.objects.filter(scheme_id=scheme_id)
    else:
        subjects = Subject.objects.filter(
            scheme_id=scheme_id,
            branch=staff.branch
        )

    return JsonResponse(
        [{"id": s.id, "name": str(s)} for s in subjects],
        safe=False
    )


@login_required
def get_sections(request):

    staff = get_staff(request)
    scheme_id = request.GET.get("scheme")

    if staff.role_type == "cycle":
        sections = Section.objects.filter(scheme_id=scheme_id)
    else:
        sections = Section.objects.filter(
            scheme_id=scheme_id,
            branch=staff.branch
        )

    return JsonResponse(
        [{"id": s.id, "name": str(s)} for s in sections],
        safe=False
    )


# -----------------------------------
# STUDENTS
# -----------------------------------
@login_required
def hod_students(request):

    staff = get_staff(request)
    students = Student.objects.filter(section__branch=staff.branch)

    return render(request, "hod_students.html", {"students": students})


@login_required
def add_student(request):

    staff = get_staff(request)
    sections = Section.objects.filter(branch=staff.branch)

    if request.method == "POST":

        if Student.objects.filter(usn=request.POST.get("usn")).exists():
            messages.error(request, "Student exists")
            return redirect("/staff/hod/students/")

        Student.objects.create(
            name=request.POST.get("name"),
            usn=request.POST.get("usn"),
            section_id=request.POST.get("section"),
            is_diploma=request.POST.get("is_diploma") == "on"
        )

        return redirect("/staff/hod/students/")

    return render(request, "add_student.html", {"sections": sections})


@login_required
def edit_student(request, student_id):

    student = Student.objects.get(id=student_id)

    if request.method == "POST":

        student.name = request.POST.get("name")
        student.usn = request.POST.get("usn")
        student.section_id = request.POST.get("section")
        student.is_diploma = request.POST.get("is_diploma") == "on"

        student.save()

        return redirect("/staff/hod/students/")

    return render(request, "edit_student.html", {"student": student})


@login_required
def delete_student(request, student_id):

    Student.objects.filter(id=student_id).delete()
    return redirect("/staff/hod/students/")


# -----------------------------------
# STAFF MANAGEMENT
# -----------------------------------
@login_required
def hod_staff_list(request):

    staff = get_staff(request)
    staff_list = Staff.objects.filter(branch=staff.branch)

    return render(request, "hod_staff_list.html", {"staff_list": staff_list})


@login_required
def add_staff(request):

    staff = get_staff(request)

    if request.method == "POST":

        staff_id = request.POST.get("staff_id")
        name = request.POST.get("name")
        password = request.POST.get("password")

        if Staff.objects.filter(staff_id=staff_id).exists():
            messages.error(request, "Staff exists")
            return redirect("/staff/hod/add-staff/")

        # 🔐 Create User
        User.objects.create_user(
            username=staff_id,
            password=password
        )

        # ✅ Force role_type (don't depend on form)
        Staff.objects.create(
            name=name,
            staff_id=staff_id,
            role_type="branch",
            branch=staff.branch
        )

        return redirect("/staff/hod/staff/")

    return render(request, "add_staff.html")


@login_required
def edit_staff(request, id):

    target = Staff.objects.get(id=id)

    if request.method == "POST":

        new_password = request.POST.get("password")

        if new_password:
            user = User.objects.get(username=target.staff_id)
            user.set_password(new_password)
            user.save()

        target.name = request.POST.get("name")
        target.save()

        return redirect("/staff/hod/staff/")

    return render(request, "edit_staff.html", {"staff": target})


@login_required
def delete_staff(request, id):

    target = Staff.objects.get(id=id)

    try:
        User.objects.get(username=target.staff_id).delete()
    except:
        pass

    target.delete()

    return redirect("/staff/hod/staff/")



# -----------------------------------
# BULK STUDENT UPLOAD (CSV)
# -----------------------------------
@login_required
def upload_students_csv(request):

    staff = get_staff(request)

    if not staff or staff.role_type != "hod":
        return redirect("/staff/dashboard/")

    if request.method == "POST":

        file = request.FILES.get("file")

        if not file:
            messages.error(request, "No file uploaded")
            return redirect("/staff/hod/")

        try:
            decoded_file = TextIOWrapper(file.file, encoding='utf-8')
            reader = csv.DictReader(decoded_file)

            for row in reader:

                usn = row.get("usn")

                if not usn:
                    continue

                if Student.objects.filter(usn=usn).exists():
                    continue

                Student.objects.create(
                    name=row.get("name"),
                    usn=usn,
                    section_id=row.get("section"),
                    is_diploma=row.get("is_diploma") == "True"
                )

            messages.success(request, "Students uploaded successfully")

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

        return redirect("/staff/hod/students/")

    return redirect("/staff/hod/")


# -----------------------------------
# ADD SECTION
# -----------------------------------
@login_required
def add_section(request):

    staff = get_staff(request)

    if not staff or staff.role_type != "hod":
        return redirect("/staff/dashboard/")

    if request.method == "POST":
        Section.objects.create(
            name=request.POST.get("name"),
            scheme_id=request.POST.get("scheme"),
            branch=staff.branch
        )

    return redirect("/staff/hod/")


# -----------------------------------
# ADD SUBJECT
# -----------------------------------
@login_required
def add_subject(request):

    staff = get_staff(request)

    if not staff or staff.role_type != "hod":
        return redirect("/staff/dashboard/")

    if request.method == "POST":
        Subject.objects.create(
            name=request.POST.get("name"),
            semester_id=request.POST.get("semester"),
            scheme_id=request.POST.get("scheme"),
            branch=staff.branch
        )

    return redirect("/staff/hod/")
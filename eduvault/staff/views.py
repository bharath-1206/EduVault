from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib import messages

from .models import Staff
from materials.models import Material
from academics.models import Scheme, Semester, Subject, Section
from students.models import Student
from accounts.models import ActivityLog

import cloudinary.uploader
import csv
from io import TextIOWrapper


# -----------------------------------
# HELPER (FIXED)
# -----------------------------------
def get_staff(request):
    staff_id = request.session.get("staff_id")

    if not staff_id:
        return None

    try:
        return Staff.objects.get(staff_id=staff_id)
    except Staff.DoesNotExist:
        return None


# -----------------------------------
# LOGIN
# -----------------------------------
def staff_login(request):
    staff = get_staff(request)

    if not staff:
        return redirect("/")

    if not staff.is_active:
        request.session.flush()
        messages.error(request, "Your account is inactive.")
        return redirect("/")

    return redirect("/staff/hod/" if staff.role_type == "hod" else "/staff/dashboard/")


# -----------------------------------
# STAFF DASHBOARD
# -----------------------------------
def staff_dashboard(request):

    staff = get_staff(request)
    if not staff:
        return redirect("/")

    if staff.role_type == "hod":
        return redirect("/staff/hod/")

    schemes = Scheme.objects.all()

    if staff.role_type == "cycle":
        materials = Material.objects.all()
        sections = Section.objects.all()
    else:
        materials = Material.objects.filter(section__branch=staff.branch)
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
# HOD STUDENTS
# -----------------------------------
def hod_students(request):

    staff = get_staff(request)
    if not staff or staff.role_type != "hod":
        return redirect("/staff/dashboard/")

    students = Student.objects.filter(section__branch=staff.branch)

    return render(request, "hod_students.html", {
        "students": students
    })


# -----------------------------------
# MATERIAL UPLOAD
# -----------------------------------
def upload_material(request):

    staff = get_staff(request)
    if not staff:
        return redirect("/")

    if request.method == "POST":

        title = request.POST.get("title")
        subject_id = request.POST.get("subject")
        section_id = request.POST.get("section")
        file = request.FILES.get("file")

        if not all([title, subject_id, section_id, file]):
            messages.error(request, "All fields required")
        else:
            try:
                subject = Subject.objects.get(id=subject_id)

                # 🔥 Branch restriction ONLY for non-cycle
                if staff.role_type != "cycle":
                    if subject.branch != staff.branch:
                        raise Exception("Invalid subject for your branch")

                # 🔥 Cycle staff → only Sem 1 & 2
                if staff.role_type == "cycle":
                    if subject.semester.number not in [1, 2]:
                        messages.error(request, "Cycle staff can upload only for Sem 1 & 2")
                        return redirect("/staff/dashboard/")

                # 🔥 Section restriction
                if staff.role_type == "cycle":
                    section = Section.objects.get(id=section_id)
                else:
                    section = Section.objects.get(id=section_id, branch=staff.branch)

                Material.objects.create(
                    title=title,
                    subject=subject,
                    section=section,
                    file=file
                )

                ActivityLog.objects.create(
                    user_type=staff.role_type,
                    user_id=staff.staff_id,
                    action=f"Uploaded material: {title}"
                )

                messages.success(request, "Material uploaded successfully")

            except Exception as e:
                messages.error(request, f"Error: {str(e)}")

        return redirect("/staff/hod/" if staff.role_type == "hod" else "/staff/dashboard/")

    return redirect("/")


# -----------------------------------
# DELETE MATERIAL
# -----------------------------------
def delete_material(request, material_id):

    staff = get_staff(request)
    if not staff:
        return redirect("/")

    try:
        material = Material.objects.get(id=material_id)

        if material.file:
            cloudinary.uploader.destroy(material.file.public_id)

        material.delete()

    except Exception as e:
        messages.error(request, f"Error deleting material: {str(e)}")

    return redirect("/staff/hod/" if staff.role_type == "hod" else "/staff/dashboard/")


# -----------------------------------
# FILTER APIs
# -----------------------------------
def get_subjects(request):

    staff = get_staff(request)
    if not staff:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    scheme_id = request.GET.get("scheme")

    if staff.role_type == "cycle":
        subjects = Subject.objects.filter(
            scheme_id=scheme_id,
            semester__number__in=[1, 2]   # 🔥 restriction
        )
    else:
        subjects = Subject.objects.filter(
            scheme_id=scheme_id,
            branch=staff.branch
        )

    return JsonResponse(
        [
            {
                "id": s.id,
                "name": str(s)
            }
            for s in subjects
        ],
        safe=False
    )


def get_sections(request):

    staff = get_staff(request)
    if not staff:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    scheme_id = request.GET.get("scheme")

    if staff.role_type == "cycle":
        sections = Section.objects.filter(scheme_id=scheme_id)
    else:
        sections = Section.objects.filter(scheme_id=scheme_id, branch=staff.branch)

    return JsonResponse(
        [{"id": s.id, "name": str(s)} for s in sections],
        safe=False
    )


# -----------------------------------
# ADD STUDENT
# -----------------------------------
def add_student(request):

    staff = get_staff(request)
    if not staff or staff.role_type != "hod":
        return redirect("/staff/dashboard/")

    sections = Section.objects.filter(branch=staff.branch)

    if request.method == "POST":

        section_id = request.POST.get("section")

        if not Section.objects.filter(id=section_id, branch=staff.branch).exists():
            messages.error(request, "Invalid section")
            return redirect("/staff/hod/students/")

        usn = request.POST.get("usn")

        # 🚫 Prevent duplicate
        if Student.objects.filter(usn=usn).exists():
            messages.error(request, "Student with this USN already exists")
            return redirect("/staff/hod/students/")

        # ✅ Safe insert
        is_diploma = request.POST.get("is_diploma") == "on"

        Student.objects.create(
            name=request.POST.get("name"),
            usn=usn,
            section_id=section_id,
            is_diploma=is_diploma
        )

        return redirect("/staff/hod/students/")

    return render(request, "add_student.html", {"sections": sections})


# -----------------------------------
# EDIT STUDENT
# -----------------------------------
def edit_student(request, student_id):

    staff = get_staff(request)
    if not staff:
        return redirect("/")

    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return redirect("/staff/hod/students/")

    if request.method == "POST":

        section_id = request.POST.get("section")

        if not Section.objects.filter(id=section_id, branch=staff.branch).exists():
            messages.error(request, "Invalid section")
            return redirect("/staff/hod/students/")

        # ✅ Update basic fields
        student.name = request.POST.get("name")
        student.usn = request.POST.get("usn").strip().upper()
        student.section_id = section_id

        # ✅ Handle diploma checkbox
        student.is_diploma = request.POST.get("is_diploma") == "on"

        # ✅ Handle manual scheme (year-back support)
        scheme_year = request.POST.get("scheme_year")

        if scheme_year:
            scheme_obj = Scheme.objects.filter(year=int(scheme_year)).first()
            if scheme_obj:
                student.scheme = scheme_obj
        else:
            # 🔥 Important: clear scheme so save() recalculates
            student.scheme = None

        student.save()

        return redirect("/staff/hod/students/")

    return render(request, "edit_student.html", {
        "student": student,
        "sections": Section.objects.filter(branch=staff.branch)
    })


# -----------------------------------
# DELETE STUDENT
# -----------------------------------
def delete_student(request, student_id):

    staff = get_staff(request)
    if not staff:
        return redirect("/")

    try:
        Student.objects.get(id=student_id).delete()
    except:
        pass

    return redirect("/staff/hod/students/")


# -----------------------------------
# CSV UPLOAD (FIXED)
# -----------------------------------
from io import TextIOWrapper
import csv
from django.shortcuts import redirect
from django.contrib import messages

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

            created_count = 0
            skipped_count = 0

            for row in reader:
                try:
                    # ✅ Clean input
                    name = row.get("name", "").strip()
                    usn = row.get("usn", "").strip().upper()
                    section_name = row.get("section", "").strip()
                    is_diploma = row.get("is_diploma", "").strip().lower() == "yes"
                    scheme_year = row.get("scheme_year", "").strip()  # 🔥 NEW

                    # ✅ Validate
                    if not name or not usn or not section_name:
                        print("❌ Missing data:", row)
                        skipped_count += 1
                        continue

                    # ✅ Get section
                    section = Section.objects.filter(
                        name=section_name,
                        branch=staff.branch
                    ).first()

                    if not section:
                        print("❌ Section not found:", section_name)
                        skipped_count += 1
                        continue

                    # ✅ Skip duplicates
                    if Student.objects.filter(usn=usn).exists():
                        skipped_count += 1
                        print("⚠️ Duplicate skipped:", usn)
                        continue

                    # ✅ Create student
                    student = Student(
                        name=name,
                        usn=usn,
                        section=section,
                        is_diploma=is_diploma
                    )

                    # 🔥 Year-back handling (manual scheme override)
                    if scheme_year:
                        scheme_obj = Scheme.objects.filter(year=int(scheme_year)).first()
                        if scheme_obj:
                            student.scheme = scheme_obj

                    # ✅ Save (will auto-apply logic if scheme not set)
                    student.save()

                    created_count += 1
                    print("✅ Created:", usn)

                except Exception as e:
                    print("❌ Row error:", row, e)
                    skipped_count += 1
                    continue

            messages.success(
                request,
                f"{created_count} students added, {skipped_count} skipped"
            )

        except Exception as e:
            messages.error(request, f"Error processing file: {str(e)}")

    return redirect("/staff/hod/")
# -----------------------------------
# ADD SECTION
# -----------------------------------
def add_section(request):

    staff = get_staff(request)
    if not staff:
        return redirect("/")

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
def add_subject(request):

    staff = get_staff(request)
    if not staff:
        return redirect("/")

    if request.method == "POST":
        Subject.objects.create(
            name=request.POST.get("name"),
            semester_id=request.POST.get("semester"),
            scheme_id=request.POST.get("scheme"),
            branch=staff.branch
        )

    return redirect("/staff/hod/")


# -----------------------------------
# HOD STAFF LIST
# -----------------------------------
def hod_staff_list(request):

    staff = get_staff(request)
    if not staff or staff.role_type != "hod":
        return redirect("/staff/dashboard/")

    staff_list = Staff.objects.filter(branch=staff.branch)

    return render(request, "hod_staff_list.html", {
        "staff_list": staff_list
    })


# -----------------------------------
# ADD STAFF
# -----------------------------------
def add_staff(request):

    staff = get_staff(request)
    if not staff or staff.role_type != "hod":
        return redirect("/staff/dashboard/")

    if request.method == "POST":

        name = request.POST.get("name")
        staff_id = request.POST.get("staff_id")
        password = request.POST.get("password")
        role_type = request.POST.get("role_type")

        if not all([name, staff_id, password, role_type]):
            messages.error(request, "All fields required")
            return redirect("/staff/hod/add-staff/")

        # 🔥 HOD cannot create cycle staff
        if role_type == "cycle":
            messages.error(request, "HOD cannot create cycle staff")
            return redirect("/staff/hod/add-staff/")

        if Staff.objects.filter(staff_id=staff_id).exists():
            messages.error(request, "Staff ID already exists")
            return redirect("/staff/hod/add-staff/")

        Staff.objects.create(
            name=name,
            staff_id=staff_id,
            password=password,
            role_type=role_type,
            branch=staff.branch  # only branch staff
        )

        messages.success(request, "Staff created successfully")

        return redirect("/staff/hod/staff/")

    return render(request, "add_staff.html")


# -----------------------------------
# EDIT STAFF
# -----------------------------------
def edit_staff(request, id):

    staff = get_staff(request)
    if not staff or staff.role_type != "hod":
        return redirect("/staff/dashboard/")

    target = Staff.objects.get(id=id)

    if target.branch != staff.branch:
        messages.error(request, "Unauthorized access")
        return redirect("/staff/hod/staff/")

    if request.method == "POST":
        target.name = request.POST.get("name")
        target.password = request.POST.get("password")
        target.save()

        messages.success(request, "Staff updated successfully")

        return redirect("/staff/hod/staff/")

    return render(request, "edit_staff.html", {"staff": target})


# -----------------------------------
# DELETE STAFF
# -----------------------------------
def delete_staff(request, id):

    staff = get_staff(request)
    if not staff or staff.role_type != "hod":
        return redirect("/staff/dashboard/")

    target = Staff.objects.get(id=id)

    if target.branch != staff.branch:
        messages.error(request, "Unauthorized action")
        return redirect("/staff/hod/staff/")

    target.delete()

    messages.success(request, "Staff deleted successfully")

    return redirect("/staff/hod/staff/")
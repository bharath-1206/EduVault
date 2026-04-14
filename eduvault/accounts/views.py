from django.shortcuts import render, redirect
from django.contrib import messages
from students.models import Student
from staff.models import Staff


from django.shortcuts import render, redirect
from django.contrib import messages
from students.models import Student
from staff.models import Staff


def login_view(request):

    # ✅ Clear session ONLY if already logged in (safer)
    if request.method == "GET":
        if "staff_id" in request.session or "student_id" in request.session:
            request.session.flush()

    if request.method == "POST":

        user_id = request.POST.get("usn")
        password = request.POST.get("password")

        if not user_id:
            messages.error(request, "Please enter USN or Staff ID")
            return render(request, "login.html")

        user_id = user_id.strip()

        # 🔥 Clear session ONLY once before login
        if "staff_id" in request.session or "student_id" in request.session:
            request.session.flush()

        # -------------------------------
        # STUDENT LOGIN (NO PASSWORD)
        # -------------------------------
        student = Student.objects.filter(usn=user_id).first()

        if student:

            request.session["student_id"] = student.usn

            if student.scheme:
                request.session["scheme"] = student.scheme.year

            return redirect("/student/")

        # -------------------------------
        # STAFF LOGIN (PASSWORD REQUIRED)
        # -------------------------------
        staff = Staff.objects.filter(staff_id=user_id).first()

        if staff:

            # Step 1: Ask password
            if not password:
                return render(request, "login.html", {
                    "ask_password": True,
                    "staff_id": user_id
                })

            # Step 2: Check password
            if not staff.check_password(password):
                messages.error(request, "Invalid password")
                return render(request, "login.html", {
                    "ask_password": True,
                    "staff_id": user_id
                })

            # Step 3: Check active
            if not staff.is_active:
                messages.error(request, "Your account is inactive. Contact admin.")
                return render(request, "login.html")

            request.session["staff_id"] = staff.staff_id
            return redirect("/staff/")

        # -------------------------------
        # Invalid Login
        # -------------------------------
        messages.error(request, "Invalid USN or Staff ID")

    return render(request, "login.html")


def logout_user(request):

    request.session.flush()

    return redirect("/")

def logout_user(request):

    request.session.flush()

    return redirect("/")
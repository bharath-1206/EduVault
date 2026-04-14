
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect

from students.models import Student
from staff.models import Staff


def login_view(request):

    if request.method == "GET":
        return render(request, "login.html")

    if request.method == "POST":

        user_id = request.POST.get("usn")
        password = request.POST.get("password")

        if not user_id:
            messages.error(request, "Enter ID")
            return render(request, "login.html")

        user_id = user_id.strip()

        # -------------------------------
        # STEP 1 → CHECK STUDENT
        # -------------------------------
        student = Student.objects.filter(usn=user_id).first()

        if student:
            request.session["student_id"] = student.usn

            if student.scheme:
                request.session["scheme"] = student.scheme.year

            return redirect("/student/")

        # -------------------------------
        # STEP 2 → CHECK STAFF
        # -------------------------------
        staff = Staff.objects.filter(staff_id=user_id).first()

        if staff:

            # STEP 2A → ask password
            if not password:
                return render(request, "login.html", {
                    "ask_password": True,
                    "staff_id": user_id
                })

            # STEP 2B → authenticate via Django
            user = authenticate(request, username=user_id, password=password)

            if not user:
                messages.error(request, "Invalid password")
                return render(request, "login.html", {
                    "ask_password": True,
                    "staff_id": user_id
                })

            if not staff.is_active:
                messages.error(request, "Inactive account")
                return render(request, "login.html")

            # ✅ LOGIN (Django session)
            login(request, user)

            return redirect("/staff/")

        # -------------------------------
        # INVALID
        # -------------------------------
        messages.error(request, "Invalid ID")

    return render(request, "login.html")


def logout_user(request):

    request.session.flush()

    return redirect("/")

def logout_user(request):

    request.session.flush()

    return redirect("/")
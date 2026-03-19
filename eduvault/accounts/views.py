


from django.shortcuts import render, redirect
from django.contrib import messages
from students.models import Student
from staff.models import Staff


def login_view(request):

    # If already logged in
    if "student_id" in request.session:
        return redirect("/student/")

    if "staff_id" in request.session:
        return redirect("/staff/")

    if request.method == "POST":

        user_id = request.POST.get("usn")

        if not user_id:
            messages.error(request, "Please enter USN or Staff ID")
            return render(request, "login.html")

        user_id = user_id.strip()

        # Clear any previous session
        request.session.flush()

        # -------------------------------
        # Check Student Login
        # -------------------------------
        student = Student.objects.filter(usn=user_id).first()

        if student:

            request.session["student_id"] = student.usn

            # Store scheme if available
            if student.scheme:
                request.session["scheme"] = student.scheme.year

            return redirect("/student/")

        # -------------------------------
        # Check Staff Login
        # -------------------------------
        staff = Staff.objects.filter(staff_id=user_id).first()

        if staff:

            # ✅ NEW: CHECK ACTIVE STATUS
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
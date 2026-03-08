from django.shortcuts import render, redirect
from django.contrib import messages

from students.models import Student
from staff.models import Staff


def login_view(request):

    if request.method == "POST":

        user_id = request.POST.get("usn")

        # Check Student
        try:
            student = Student.objects.get(usn=user_id)

            request.session["student_id"] = student.usn

            return redirect("/student/")

        except Student.DoesNotExist:
            pass

        # Check Staff
        try:
            staff = Staff.objects.get(staff_id=user_id)

            request.session["staff_id"] = staff.staff_id

            return redirect("/staff/")

        except Staff.DoesNotExist:
            pass

        messages.error(request, "Invalid USN or Staff ID")

        return redirect("/")

    return render(request, "login.html")


def logout_user(request):

    request.session.flush()

    return redirect("/")
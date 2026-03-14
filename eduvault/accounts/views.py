from django.shortcuts import render, redirect
from django.contrib import messages
from students.models import Student
from staff.models import Staff




def login_view(request):

    if request.method == "POST":

        user_id = request.POST.get("usn")

        # Check Student
        student = Student.objects.filter(usn=user_id).first()

        if student:

            request.session["student_id"] = student.usn
            request.session["scheme"] = student.scheme.year

            return redirect("/student/")

        # Check Staff
        staff = Staff.objects.filter(staff_id=user_id).first()

        if staff:

            request.session["staff_id"] = staff.staff_id

            return redirect("/staff/")

        messages.error(request, "Invalid USN or Staff ID")

    return render(request, "login.html")
def logout_user(request):

    request.session.flush()

    return redirect("/")
from django.shortcuts import render
from students.models import Student


def login_view(request):
    if request.method == "POST":
        usn = request.POST.get("usn")

        try:
            student = Student.objects.get(usn=usn)
            return render(request, "dashboard.html", {"student": student})
        except Student.DoesNotExist:
            return render(request, "login.html", {"error": "Invalid USN"})

    return render(request, "login.html")
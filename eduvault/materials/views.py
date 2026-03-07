from django.shortcuts import render
from .models import Material

def subject_materials(request, subject_id):

    materials = Material.objects.filter(

        subject_id=subject_id
    )

    context = {
        "materials": materials,

    }

    return render(request, "materials.html", context)
from academics.models import Subject

def semester_subjects(request, semester_number, branch_id):

    subjects = Subject.objects.filter(
        semester__number=semester_number,
        branch_id=branch_id
    )

    context = {
        "subjects": subjects,
        "semester": semester_number
    }

    return render(request, "subjects.html", context)
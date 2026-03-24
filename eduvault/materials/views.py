from django.shortcuts import render
from .models import Material,Subject

def semester_subjects(request, semester_number, branch_id):

    scheme_year = request.session.get("scheme")

    subjects = Subject.objects.filter(
        semester__number=semester_number,
        branch_id=branch_id,
        scheme__year=scheme_year
    )

    context = {
        "subjects": subjects,
        "semester": semester_number
    }

    return render(request, "subjects.html", context)



def subject_materials(request, subject_id):

    materials = Material.objects.filter(

        subject_id=subject_id
    )

    context = {
        "materials": materials,

    }

    return render(request, "materials.html", context)
from academics.models import Subject


def student_subjects(request):

    scheme_year = request.session.get("scheme")

    subjects = Subject.objects.filter(
        scheme__year=scheme_year
    )

    return render(request, "subjects.html", {"subjects": subjects})


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Material
from .serializers import MaterialSerializer

@api_view(['GET'])
def get_materials(request):
    materials = Material.objects.all()
    serializer = MaterialSerializer(materials, many=True, context={'request': request})
    return Response(serializer.data)
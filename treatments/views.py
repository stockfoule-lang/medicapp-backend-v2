from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from .models import Treatment

User = get_user_model()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_treatments(request, patient_id):

    treatments = Treatment.objects.filter(patient_id=patient_id)

    data = []

    for t in treatments:
        data.append({
            "id": t.id,
            "medicament_name": t.medicament_name,
            "forme": t.forme,
            "dosage": t.dosage,
            "matin": t.matin,
            "midi": t.midi,
            "soir": t.soir,
            "semaine": t.semaine,
            "duree": t.duree,
            "notes": t.notes,
        })

    return Response(data)


@api_view(['POST'])
def add_treatment(request):

    patient_id = request.data.get("patient_id")

    if not patient_id:
        return Response(
            {"error": "patient_id manquant"},
            status=status.HTTP_400_BAD_REQUEST
        )

    patient = User.objects.filter(id=patient_id).first()

    if not patient:
        return Response(
            {"error": "patient introuvable"},
            status=status.HTTP_404_NOT_FOUND
        )

    Treatment.objects.create(
        patient=patient,
        medicament_name=request.data.get("medicament_name"),
        forme=request.data.get("forme"),
        dosage=request.data.get("dosage"),
        matin=request.data.get("matin"),
        midi=request.data.get("midi"),
        soir=request.data.get("soir"),
        semaine=request.data.get("semaine"),
        duree=request.data.get("duree"),
        notes=request.data.get("notes"),
    )

    return Response(
        {"message": "Traitement ajouté"},
        status=status.HTTP_201_CREATED
    )


@api_view(['PUT'])
def update_treatment(request, id):

    treatment = Treatment.objects.filter(id=id).first()

    if not treatment:
        return Response(
            {"error": "Traitement introuvable"},
            status=status.HTTP_404_NOT_FOUND
        )

    treatment.medicament_name = request.data.get("medicament_name")
    treatment.forme = request.data.get("forme")
    treatment.dosage = request.data.get("dosage")
    treatment.matin = request.data.get("matin")
    treatment.midi = request.data.get("midi")
    treatment.soir = request.data.get("soir")
    treatment.semaine = request.data.get("semaine")
    treatment.duree = request.data.get("duree")
    treatment.notes = request.data.get("notes")

    treatment.save()

    return Response({
        "message": "Traitement modifié"
    })


@api_view(['DELETE'])
def delete_treatment(request, id):

    treatment = Treatment.objects.filter(id=id).first()

    if not treatment:
        return Response(
            {"error": "Traitement introuvable"},
            status=status.HTTP_404_NOT_FOUND
        )

    treatment.delete()

    return Response({
        "message": "Traitement supprimé"
    })
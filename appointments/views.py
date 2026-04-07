from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from .models import Appointment

User = get_user_model()


# =========================
# GET APPOINTMENTS
# =========================
@api_view(['GET'])
def get_appointments(request, patient_id):

    try:
        appointments = Appointment.objects.filter(patient_id=patient_id)

        data = []

        for a in appointments:
            data.append({
                "id": a.id,
                "title": a.title or "",
                "date": str(a.date) if a.date else "",
                "time": str(a.time) if a.time else "",
                "instructions": a.instructions or ""
            })

        return Response(data)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# =========================
# CREATE APPOINTMENT
# =========================
@api_view(['POST'])
def create_appointment(request):

    try:
        patient_id = request.data.get("patient_id")

        if not patient_id:
            return Response(
                {"error": "patient_id requis"},
                status=status.HTTP_400_BAD_REQUEST
            )

        patient = User.objects.filter(id=patient_id).first()

        if not patient:
            return Response(
                {"error": "patient introuvable"},
                status=status.HTTP_404_NOT_FOUND
            )

        appointment = Appointment.objects.create(
            patient=patient,
            title=request.data.get("title", ""),
            date=request.data.get("date"),
            time=request.data.get("time"),
            instructions=request.data.get("instructions", "")
        )

        return Response({
            "message": "Rendez-vous créé",
            "id": appointment.id
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# =========================
# DELETE APPOINTMENT
# =========================
@api_view(['DELETE'])
def delete_appointment(request, id):

    try:
        appt = Appointment.objects.filter(id=id).first()

        if not appt:
            return Response(
                {"error": "Rendez-vous introuvable"},
                status=status.HTTP_404_NOT_FOUND
            )

        appt.delete()

        return Response({"message": "Rendez-vous supprimé"})

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
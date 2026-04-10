from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from config.firebase import send_push
from .models import Appointment
import json

User = get_user_model()


# =========================
# GET APPOINTMENTS
# =========================
@api_view(['GET'])
def get_appointments(request, patient_id):
    try:
        appointments = Appointment.objects.filter(patient_id=patient_id)

        data = [
            {
                "id": a.id,
                "title": a.title or "",
                "date": str(a.date) if a.date else "",
                "time": str(a.time) if a.time else "",
                "instructions": a.instructions or ""
            }
            for a in appointments
        ]

        return Response(data)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# =========================
# CREATE APPOINTMENT + NOTIF 🔥
# =========================
@api_view(['POST'])
def create_appointment(request):

    # 🔥 Parsing JSON fiable (Render)
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return Response(
            {"error": "JSON invalide"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        patient_id = data.get("patient_id")

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

        # 🔥 Création du RDV
        appointment = Appointment.objects.create(
            patient=patient,
            title=data.get("title", ""),
            date=data.get("date"),
            time=data.get("time"),
            instructions=data.get("instructions", "")
        )

        # =========================
        # 🔔 ENVOI NOTIFICATION
        # =========================
        if hasattr(patient, "fcm_token") and patient.fcm_token:
            try:
                send_push(
                    patient.fcm_token,
                    "Nouveau rendez-vous",
                    f"{data.get('title')} le {data.get('date')} à {data.get('time')}"
                )
                print("🔥 Notification envoyée au patient")
            except Exception as e:
                print("❌ Erreur envoi notification :", e)
        else:
            print("⚠️ Aucun fcm_token pour ce patient")

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
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Appointment
import json
from notifications.push import send_push_notification

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
# CREATE APPOINTMENT + NOTIFICATION RÉELLE
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
        # 🔔 NOTIFICATION RÉELLE FIREBASE
        # =========================
        try:
            token = getattr(patient, "fcm_token", None)

            if token:
                send_push_notification(token, appointment)
                print("✅ Notification envoyée à :", token)
            else:
                print("⚠️ Aucun fcm_token pour ce patient")

        except Exception as notif_error:
            # 👉 ne JAMAIS casser la création du RDV
            print("❌ Erreur notification :", notif_error)

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
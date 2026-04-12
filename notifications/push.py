from firebase_admin import messaging
from .firebase import initialize_firebase

def send_push_notification(token, appointment):
    try:
        initialize_firebase()

        message = messaging.Message(
            notification=messaging.Notification(
                title="Nouveau rendez-vous",
                body=f"RDV le {appointment.date}"
            ),
            token=token,
        )

        messaging.send(message)

    except Exception as e:
        print("Erreur envoi notification :", e)
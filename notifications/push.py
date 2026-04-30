import firebase_admin
from firebase_admin import credentials, messaging
import os
import json


# =========================
# 🔥 INITIALISATION FIREBASE (SAFE POUR RENDER)
# =========================

def initialize_firebase():
    if not firebase_admin._apps:

        # 🔐 Récupération depuis variable d'environnement (RENDER)
        firebase_creds = os.environ.get("FIREBASE_CREDENTIALS")

        if firebase_creds:
            cred_dict = json.loads(firebase_creds)
            cred = credentials.Certificate(cred_dict)
        else:
            # fallback local (si tu testes en local)
            cred = credentials.Certificate("firebase.json")

        firebase_admin.initialize_app(cred)


# =========================
# 🔔 ENVOI NOTIFICATION (VERSION PRO)
# =========================

def send_push_notification(token, title, body):

    try:
        initialize_firebase()

        message = messaging.Message(
            # 🔔 NOTIFICATION STANDARD (OBLIGATOIRE POUR BACKGROUND / KILLED)
            notification=messaging.Notification(
                title=title,
                body=body,
            ),

            # 🔥 CONFIG ANDROID (CRITIQUE)
            android=messaging.AndroidConfig(
                priority="high",
                notification=messaging.AndroidNotification(
                    sound="default",
                    channel_id="medicapp_channel_v2",
                ),
            ),

            # 🔥 CONFIG iOS (SAFE / FUTUR)
            apns=messaging.APNSConfig(
                payload=messaging.APNSPayload(
                    aps=messaging.Aps(
                        sound="default"
                    )
                )
            ),

            # 🎯 TOKEN CIBLE
            token=token,
        )

        response = messaging.send(message)

        print("✅ Firebase OK :", response)

    except Exception as e:
        print("❌ Firebase ERROR :", str(e))
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
# 🔔 ENVOI NOTIFICATION
# =========================

def send_push_notification(token, title, body):

    try:
        initialize_firebase()

        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=token,
        )

        response = messaging.send(message)

        print("✅ Firebase OK :", response)

    except Exception as e:
        print("❌ Firebase ERROR :", str(e))
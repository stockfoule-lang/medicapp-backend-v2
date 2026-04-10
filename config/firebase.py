import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate("firebase_key.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)


def send_push(token, title, body):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,
    )

    response = messaging.send(message)
    print("🔥 Notification envoyée :", response)
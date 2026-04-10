import firebase_admin
from firebase_admin import credentials, messaging

def send_push(token, title, body):
    try:
        if not firebase_admin._apps:
            try:
                cred = credentials.Certificate("firebase_key.json")
                firebase_admin.initialize_app(cred)
            except Exception:
                print("Firebase not initialized (no key)")
                return

        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            token=token,
        )

        messaging.send(message)

    except Exception as e:
        print("Firebase error:", e)
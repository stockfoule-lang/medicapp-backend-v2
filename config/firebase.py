try:
    import firebase_admin
    from firebase_admin import credentials, messaging

    # 🔥 Essaye de charger la clé
    try:
        cred = credentials.Certificate("firebase_key.json")
        firebase_admin.initialize_app(cred)
        FIREBASE_READY = True
        print("🔥 Firebase READY")
    except Exception as e:
        FIREBASE_READY = False
        print("🔥 Firebase INIT FAIL :", e)

    def send_push(token, title, body):
        if not FIREBASE_READY:
            print("⚠️ Firebase OFF → push ignoré")
            return

        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=token,
        )
        messaging.send(message)

except Exception as e:
    print("🔥 Firebase module KO :", e)

    def send_push(token, title, body):
        print("⚠️ Firebase non dispo")
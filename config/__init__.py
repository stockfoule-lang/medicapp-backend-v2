import os
import json
import firebase_admin
from firebase_admin import credentials

FIREBASE_CREDENTIALS = os.environ.get("FIREBASE_CREDENTIALS")

if FIREBASE_CREDENTIALS:
    try:
        cred_dict = json.loads(FIREBASE_CREDENTIALS)
        cred = credentials.Certificate(cred_dict)

        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
            print("🔥 Firebase initialized (INIT.PY)")

    except Exception as e:
        print("❌ Firebase init error:", e)
else:
    print("⚠️ FIREBASE_CREDENTIALS manquant")
import os
import firebase_admin
from firebase_admin import credentials

def initialize_firebase():
    if not firebase_admin._apps:
        firebase_json = os.environ.get("FIREBASE_CREDENTIALS")

        if firebase_json:
            cred = credentials.Certificate(eval(firebase_json))
            firebase_admin.initialize_app(cred)
        else:
            raise Exception("FIREBASE_CREDENTIALS not set")
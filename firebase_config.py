import firebase_admin
from firebase_admin import credentials, firestore

def iniciar_firebase():
    cred = credentials.Certificate("clima-19bf4-firebase-adminsdk-fbsvc-2c9dd49d62.json")
    firebase_admin.initialize_app(cred)
    return firestore.client()

db = iniciar_firebase()

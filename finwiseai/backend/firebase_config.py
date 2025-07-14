import firebase_admin
from firebase_admin import credentials, auth
import os

cred = credentials.Certificate("finwiseai-firebase-adminsdk.json")
firebase_app = firebase_admin.initialize_app(cred)
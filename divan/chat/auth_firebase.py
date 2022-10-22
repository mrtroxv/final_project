import pyrebase
from .config import firebaseConfig

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()


def refresh_token(refresh_token):
    refresh = auth.refresh(refresh_token)
    return refresh


def login(email, password):
    token = {}
    login = auth.sign_in_with_email_and_password(email, password)
    token['token_id'] = login['idToken']
    token['refresh_token'] = login['refreshToken']
    return token


def signup(email, password):
    token = {}
    auth.create_user_with_email_and_password(email, password)
    token = login(email, password)
    return token

import pyrebase
firebaseConfig = {
    "apiKey": "AIzaSyBYiKRs-fIsA_-YmwWpSd7jRy9gVeUbbL0",
    "authDomain": "divan-2e324.firebaseapp.com",
    "projectId": "divan-2e324",
    "storageBucket": "divan-2e324.appspot.com",
    "messagingSenderId": "996229135049",
    "appId": "1:996229135049:web:4419780bf7d9193b94ab18",
    "measurementId": "G-EYEC03X8LF",
    "databaseURL": ""
}

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

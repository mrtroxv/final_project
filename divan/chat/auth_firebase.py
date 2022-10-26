import pyrebase
from .config import firebaseConfig
import jwt


class FirebaseAuth:
    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()

    def refresh_token(self, refresh_token):
        new_token = self.auth.refresh(refresh_token)
        return new_token

    def login(self, email, password):
        token = {}
        login = self.auth.sign_in_with_email_and_password(email, password)
        token['token_id'] = login['idToken']
        token['refresh_token'] = login['refreshToken']
        return token

    def signup(self, email, password):
        self.auth.create_user_with_email_and_password(email, password)
        token = self.login(email, password)
        return token

    def get_user_id_by_token(self, token_id):
        decode = jwt.decode(token_id, options={"verify_signature": False})
        uid = decode.get('user_id')
        return uid

from firebase_admin import credentials, auth
import firebase_admin
import os


class TokenProcess():
    def initialize(self):
        file_path = ("../divan.json")
        cred = credentials.Certificate(
            file_path)
        firebase_admin.initialize_app(cred)

    def delete_app(self):
        firebase_admin.delete_app(firebase_admin.get_app(name='[DEFAULT]'))

    def __init__(self):
        self.initialize()

    def __del__(self):
        self.delete_app()

    def is_valid_token(self, token_id):
        try:
            auth.verify_id_token(token_id)
        except:
            return False

        return True

    def revoke_token(self, uid):
        auth.revoke_refresh_tokens(uid)

    def get_user_id(self, email):
        user = auth.get_user_by_email(email)
        uid = user.uid
        return uid

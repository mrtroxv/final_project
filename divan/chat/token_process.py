from firebase_admin import credentials, auth
import firebase_admin


def initialize():
    cred = credentials.Certificate(
        "C:/Users/AHmad/Desktop/final_project/divan.json")
    firebase_admin.initialize_app(cred)


def delete_app():
    firebase_admin.delete_app(firebase_admin.get_app(name='[DEFAULT]'))


def is_valid_token(token_id):
    initialize()
    try:
        auth.verify_id_token(token_id)
    except:
        delete_app()
        return False

    delete_app()
    return True


def revoke_token(uid):
    initialize()
    auth.revoke_refresh_tokens(uid)
    delete_app()


def get_user_id(email):
    initialize()
    user = auth.get_user_by_email(email)
    uid = user.uid
    delete_app()
    return uid

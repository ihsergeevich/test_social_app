import hashlib

from app.settings import SECRET_KEY


def get_password_hash(password):
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), SECRET_KEY.encode('utf-8'), 100000).hex()

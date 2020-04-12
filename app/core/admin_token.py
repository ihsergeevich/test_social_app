from datetime import datetime, timedelta
import jwt

from app.settings import SECRET_KEY, REFRESH_EXP_DELTA_SECONDS


def get_admin_token(admin_id):
    payload_jwt = {
        'user_id': admin_id,
        'exp': datetime.utcnow() + timedelta(seconds=REFRESH_EXP_DELTA_SECONDS)
    }
    return jwt.encode(payload_jwt, SECRET_KEY, 'HS256')

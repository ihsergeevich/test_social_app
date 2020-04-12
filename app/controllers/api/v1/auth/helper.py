from datetime import datetime, timedelta


async def generate_payload(user_id, time_exp):
    payload_jwt = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(seconds=time_exp)
        }

    return payload_jwt


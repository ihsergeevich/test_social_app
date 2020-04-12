from marshmallow import ValidationError
from aiohttp import web
import jwt

from app.controllers.api.v1.auth.helper import generate_payload
from app.controllers.api.v1.auth.queries import get_user
from app.controllers.api.v1.auth.serialization import AuthParameters, RefreshParameters
from app.core.password_hash import get_password_hash
from app.settings import (
    JWT_EXP_DELTA_SECONDS, JWT_SECRET_KEY, JWT_ALGORITHM, REFRESH_TOKEN_KEY, REFRESH_EXP_DELTA_SECONDS
)


async def users_auth_post(request):
    try:
        data = AuthParameters().load(await request.json())
    except ValidationError as error:
        return web.json_response(error.messages)

    async with request.app['db'].acquire() as conn:
        user = await get_user(conn, data['login'])
        if user and user['password_hash'] == get_password_hash(data['password']):
            payload_jwt = await generate_payload(user['id'], JWT_EXP_DELTA_SECONDS)
            access_jwt_token = jwt.encode(payload_jwt, JWT_SECRET_KEY, JWT_ALGORITHM)

            payload_refresh = await generate_payload(data['id'], REFRESH_EXP_DELTA_SECONDS)
            refresh_jwt_token = jwt.encode(payload_refresh, REFRESH_TOKEN_KEY, JWT_ALGORITHM)

            return web.json_response({'jwt_token': access_jwt_token.decode('utf-8'),
                                      'refresh_token': refresh_jwt_token.decode('utf-8')})
        else:
            return web.json_response({'message': 'Invalid user'})


async def refresh_token(request):
    try:
        data = RefreshParameters().load(await request.json())
    except ValidationError as error:
        return web.json_response(error.messages)

    if data['refresh_token']:
        data = jwt.decode(data, REFRESH_TOKEN_KEY, algorithms=JWT_ALGORITHM)

        payload_jwt = await generate_payload(data['user_id'], JWT_EXP_DELTA_SECONDS)
        access_jwt_token = jwt.encode(payload_jwt, JWT_SECRET_KEY, JWT_ALGORITHM)

        payload_refresh = await generate_payload(data['user_id'], REFRESH_EXP_DELTA_SECONDS)
        refresh_jwt_token = jwt.encode(payload_refresh, REFRESH_TOKEN_KEY, JWT_ALGORITHM)

        return web.json_response({'jwt_token': access_jwt_token.decode('utf-8'),
                                  'refresh_token': refresh_jwt_token.decode('utf-8')})


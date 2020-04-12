import jwt
from aiohttp import web

from app.settings import JWT_SECRET_KEY, JWT_ALGORITHM, SECRET_KEY


async def auth_middleware(app, handler):
    async def middleware(request):
        request.user_id = None
        jwt_token = request.headers.get('jwt_token', None)

        if jwt_token:
            try:
                payload = jwt.decode(jwt_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            except (jwt.DecodeError, jwt.ExpiredSignatureError):
                return web.json_response({'message': 'Token is invalid'}, status=400)

            request.user_id = payload['user_id']
        return await handler(request)
    return middleware


async def auth_admin_middleware(app, handler):
    async def middleware(request):
        request.user_id = None
        token = request.cookies.get('token')

        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
            except (jwt.DecodeError, jwt.ExpiredSignatureError):
                return web.json_response({'message': 'Token is invalid'}, status=400)

            request.user_id = payload['user_id']
            request.user_role = 'ADMIN'
        return await handler(request)
    return middleware


def login_required(func):
    async def wrapper(request):
        if not request.user_id:
            return web.json_response(
                {'code': 0, 'message': 'Auth required'}, status=401)
        return await func(request)
    return wrapper


def admin_required(func):
    async def wrapper(request):
        if request.user_role != 'ADMIN':
            return web.json_response(
                {'code': 0, 'message': 'Permission denied'},
                status=403
            )
        return await func(request)
    return wrapper

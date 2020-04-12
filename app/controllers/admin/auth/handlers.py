from aiohttp_jinja2 import template
from aiohttp import web

from app.controllers.admin.auth.queries import get_admin
from app.core.admin_token import get_admin_token
from app.core.password_hash import get_password_hash


@template('/admin/auth/login.html')
async def admin_auth_get(request):
    return {}


async def admin_auth_post(request):
    data = await request.post()
    async with request.app['db'].acquire() as connection:
        if data['password'] and data['login']:
            admin = await get_admin(connection, data['login'])

            if admin and admin['role'] == 'ADMIN' and admin['password_hash'] == get_password_hash(data['password']):
                location = request.app.router['users'].url_for()
                response = web.HTTPSeeOther(location=location)
                token = get_admin_token((admin['id'])).decode('utf-8')
                response.cookies['token'] = token

                return response


from aiohttp_jinja2 import template
from aiohttp import web

from app.controllers.admin.users.queries import get_all_users, get_user, edit_user
from app.core.middleware import admin_required


@admin_required
@template('/admin/users/users.html')
async def admin_users_get(request):
    async with request.app['db'].acquire() as connection:
        users = await get_all_users(connection)
        return {'users': users}


@template('/admin/users/user_profile.html')
async def admin_user_profile_get(request):
    user_id = request.match_info['user_id']
    if user_id:
        async with request.app['db'].acquire() as connection:
            user = await get_user(connection, user_id)
            return {'user': user}


async def admin_user_edit_post(request):
    data = await request.post()
    user_id = request.match_info['user_id']

    if data and user_id:
        async with request.app['db'].acquire() as connection:
            await edit_user(connection, user_id, data['email'], data['firstname'], data['lastname'])
            location = request.app.router['users'].url_for()
            response = web.HTTPSeeOther(location=location)
            return response

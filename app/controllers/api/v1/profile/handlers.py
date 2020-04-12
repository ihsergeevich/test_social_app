from aiohttp import web
from marshmallow import ValidationError

from app.controllers.api.v1.profile.queries import get_all_users, get_user
from app.controllers.api.v1.profile.serialization import UserProfileParameters


async def users_all_profiles_get(request):
    async with request.app['db'].acquire() as connection:
        users = await get_all_users(connection, request.user_id)
        return web.json_response({"data": users})


async def users_one_profile_get(request):
    try:
        data = UserProfileParameters().load(await request.json())
    except ValidationError as error:
        return web.json_response(error.messages)
    async with request.app['db'].acquire() as connection:
        user = await get_user(connection, data['request_user_id'])
        return web.json_response({"data": user})

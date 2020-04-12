from marshmallow import ValidationError
from aiohttp import web

from app.controllers.api.v1.registration.queries import create_user, check_user, create_profile, check_user_by_id
from app.controllers.api.v1.registration.serialization import RegisterParameters, ProfileParameters
from app.core.middleware import login_required
from app.core.password_hash import get_password_hash


async def users_registration_post(request):
    try:
        data = RegisterParameters().load(await request.json())
    except ValidationError as error:
        return web.json_response(error.messages)

    async with request.app['db'].acquire() as cursor:
        if await check_user(cursor, data['email']):
            return web.json_response({"message": "User already exists"})

        await create_user(cursor, data['email'], get_password_hash(data['password']))

    return web.json_response({'message': 'User created!'})


@login_required
async def users_create_profile_post(request):
    try:
        data = ProfileParameters().load(await request.json())
    except ValidationError as error:
        return web.json_response(error.messages)

    async with request.app['db'].acquire() as cursor:
        if await check_user_by_id(cursor, request.user_id):
            await create_profile(cursor, data['firstname'], data['lastname'], data['about_me'], request.user_id)
            return web.json_response({'message': 'Profile created'})

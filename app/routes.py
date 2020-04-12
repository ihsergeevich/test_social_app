from app.controllers.admin.auth import handlers
from app.controllers.admin.users import users
from app.controllers.api.v1.auth import handlers as auth_handler
from app.controllers.api.v1.registration import handlers as registration_handler
from app.controllers.api.v1.profile import handlers as profiles_handler


def setup_routes(app):
    # ADMIN
    app.router.add_route('GET', '/', handlers.admin_auth_get)
    app.router.add_route('POST', '/', handlers.admin_auth_post)
    app.router.add_route('GET', '/login', handlers.admin_auth_get)
    app.router.add_route('POST', '/login', handlers.admin_auth_post)

    app.router.add_route('GET', '/users', users.admin_users_get, name="users")
    app.router.add_route('GET', '/user/edit/{user_id}', users.admin_user_profile_get)
    app.router.add_route('POST', '/user/edit/{user_id}', users.admin_user_edit_post)

    # API V1
    app.router.add_route('POST', '/api/v1/login', auth_handler.users_auth_post)
    app.router.add_route('POST', '/api/v1/refresh', auth_handler.refresh_token)

    app.router.add_route('POST', '/api/v1/registration', registration_handler.users_registration_post)
    app.router.add_route('POST', '/api/v1/profile', registration_handler.users_create_profile_post)

    app.router.add_route('GET', '/api/v1/profile/user', profiles_handler.users_one_profile_get)
    app.router.add_route('GET', '/api/v1/profiles', profiles_handler.users_all_profiles_get)

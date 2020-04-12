from aiohttp import web
import jinja2
import aiohttp_jinja2

from app.core.middleware import auth_middleware, auth_admin_middleware
from app.core.postgres import connect_postgres, close_postgres
from app.routes import setup_routes


async def create_app():
    app = web.Application(middlewares=[auth_middleware, auth_admin_middleware])
    app.router.add_static('/static/', path='app/static/')
    aiohttp_jinja2.setup(app, loader=jinja2.PackageLoader('app', 'templates'))
    setup_routes(app)
    app.on_startup.append(connect_postgres)
    app.on_cleanup.append(close_postgres)

    return app



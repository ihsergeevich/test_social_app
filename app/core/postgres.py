import asyncpg

from app.settings import POSTGRES_NAME, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT


async def connect_postgres(app):
    app['db'] = await asyncpg.create_pool(
        database=POSTGRES_NAME,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
    )


async def close_postgres(app):
    await app['db'].close()

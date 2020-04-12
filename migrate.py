import os

from migrations.database import Database
from migrations.migration import Migration
from app.settings import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_NAME, POSTGRES_HOST, POSTGRES_PORT


def main():
    """ Migration run."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'migrations', 'versions')

    db = Database(
        database=POSTGRES_NAME,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
    ).connect()

    migration = Migration(path=path, db=db)
    migrations = migration.get_migrations()
    migration.migrate(migrations=migrations)


if __name__ == '__main__':
    main()

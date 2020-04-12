import os
from datetime import datetime
from typing import Optional, NoReturn, List

from psycopg2 import connect
from psycopg2.errors import UndefinedTable


class Migration:
    """ Run migration sql scripts."""

    def __init__(self, path: str, db: connect):
        """ Init constructor."""
        self.path = path
        self.db = db

    def migrate(self, migrations: List) -> NoReturn:
        """ Run migration scripts."""
        for migration in migrations:
            print(f'Run migration: {migration}')

            with open(os.path.join(self.path, migration)) as migration_file:
                with self.db.cursor() as cursor:
                    print('Execute migration.')
                    cursor.execute(migration_file.read())

                    print('Save migration in table migrations.')
                    cursor.execute("INSERT INTO migrations (migration_name, created) VALUES (%s, %s);",
                                   (migration, datetime.now()))

                    print('Commit.')
                    self.db.commit()

        print('Successfully exit.')

    def old_migrations(self) -> List:
        """ Get completed migrations."""
        with self.db.cursor() as cursor:
            try:
                cursor.execute("SELECT migration_name FROM migrations;")
            except UndefinedTable as e:
                self.db.rollback()
                sql = """
                    CREATE TABLE migrations(
                        id serial NOT NULL,
                        migration_name varchar(255) NOT NULL,
                        created timestamptz NOT NULL,
                        CONSTRAINT migration_migration_name_key UNIQUE (migration_name),
                        CONSTRAINT migration_pkey PRIMARY KEY (id)
                    );
                """
                cursor.execute(sql)
                return []

            return cursor.fetchall()

    def get_migrations(self) -> Optional[List]:
        """ Get new migrations."""
        print('Search new migrations...')
        new_migration = os.listdir(self.path)

        if not new_migration:
            print('Migration folder sql is empty, exit.')
            return

        old_migrations = self.old_migrations()

        if not old_migrations:
            print('Not old migration, start new migration.')
            new_migration.sort()
            return new_migration

        old_migrations = [m[0] for m in old_migrations]
        intersection_migrations = list(set(new_migration) - set(old_migrations))

        intersection_migrations.sort()
        print(f'Migrations to be performed: => {intersection_migrations}')

        return intersection_migrations

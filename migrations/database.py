from psycopg2 import connect


class Database:
    """ Connection db."""

    def __init__(self, user, password, database, host, port):
        """ Init settings."""
        self.user = user
        self.password = password
        self.database = database
        self.host = host
        self.port = port

    def connect(self):
        """ Connection db."""
        conn = connect(
            user=self.user,
            port=self.port,
            database=self.database,
            password=self.password,
            host=self.host,
        )

        return conn

    def __new__(cls, *args, **kwargs):
        """ There is only one database connection."""
        if not hasattr(cls, 'instance'):
            cls.instance = super(Database, cls).__new__(cls)

        return cls.instance

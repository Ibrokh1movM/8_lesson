import psycopg2

class DatabaseConnect:
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.connection = None

    def __enter__(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            return self.connection
        except psycopg2.DatabaseError as e:
            print(f"Database connection error: {e}")
            return None

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.connection and not self.connection.closed:
            self.connection.close()

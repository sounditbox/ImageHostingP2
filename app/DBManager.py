import psycopg
from loguru import logger


class DBManager:
    def __init__(self, dbname: str, user: str,
                 password: str, host: str, port: int):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None

    def connect(self) -> psycopg.Connection:
        try:
            self.conn = psycopg.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            return self.conn
        except psycopg.Error as e:
            logger.error(f"DB connection error: {e}")

    def close(self):
        self.conn.close()

    def execute(self, query: str):
        with self.connect().cursor() as cursor:
            cursor.execute(query)

    def execute_file(self, filename: str):
        try:
            self.execute(open(f'./{filename}').read())
        except FileNotFoundError:
            logger.error(f"File {filename} not found")

    def init_tables(self):
        self.execute_file('init_tables.sql')

    def get_images(self):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM images")
            return cursor.fetchall()

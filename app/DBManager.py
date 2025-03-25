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
        with self.conn.cursor() as cursor:
            cursor.execute(query)

    def execute_file(self, filename: str):
        try:
            self.execute(open(f'./{filename}').read())
        except FileNotFoundError:
            logger.error(f"File {filename} not found")

    def init_tables(self):
        self.execute_file('init_tables.sql')
        logger.info('Tables initialized')
        self.conn.commit()

    def get_images(self):
        with self.connect().cursor() as cursor:
            cursor.execute("SELECT * FROM images")
            return cursor.fetchall()

    def add_image(self, filename, original_name, length, ext, upload_date=None):
        logger.info(f'Try to add image {filename}')
        with self.conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO images "
                "(filename, original_name, size, file_type, upload_time) "
                "VALUES (%s, %s, %s, %s, %s)",
                (filename, original_name, length, ext, upload_date)
            )
        self.conn.commit()

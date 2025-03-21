import os
from http.server import HTTPServer

from dotenv import load_dotenv
from loguru import logger

from DBManager import DBManager
from ImageHostingHandler import ImageHostingHttpRequestHandler
from settings import LOG_PATH, LOG_FILE
from settings import SERVER_ADDRESS

logger.add(LOG_PATH + LOG_FILE,
           format='[{time:YYYY-MM-DD HH:mm:ss}] {level}: {message}',
           level='INFO')
def run(server_class=HTTPServer, handler_class=ImageHostingHttpRequestHandler):
    load_dotenv()
    db = DBManager(os.getenv('POSTGRES_DB'),
                   os.getenv('POSTGRES_USER'),
                   os.getenv('POSTGRES_PASSWORD'),
                   os.getenv('POSTGRES_HOST'),
                   os.getenv('POSTGRES_PORT'))
    db.init_tables()
    logger.info(db.get_images())
    db.execute("DROP TABLE IF EXISTS images")
    httpd = server_class(SERVER_ADDRESS, handler_class)
    logger.info(f'Serving on http://{SERVER_ADDRESS[0]}:{SERVER_ADDRESS[1]}')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.warning('Keyboard interrupt received, exiting.')
        httpd.server_close()
    finally:
        logger.info('Server stopped.')


if __name__ == '__main__':
    run()

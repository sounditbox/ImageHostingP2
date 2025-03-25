import os
from uuid import uuid4

from loguru import logger

from AdvancedHandler import AdvancedHTTPRequestHandler
from DBManager import DBManager
from settings import IMAGES_PATH, \
    ALLOWED_EXTENSIONS, MAX_FILE_SIZE, ERROR_FILE


class ImageHostingHttpRequestHandler(AdvancedHTTPRequestHandler):
    server_version = 'Image Hosting Server v0.1'

    def __init__(self, request, client_address, server):

        self.get_routes = {
            '/api/images/': self.get_images
        }
        self.post_routes = {
            '/upload/': self.post_upload
        }
        self.delete_routes = {
            '/api/delete/': self.delete_image
        }
        self.db = DBManager(os.getenv('POSTGRES_DB'),
                            os.getenv('POSTGRES_USER'),
                            os.getenv('POSTGRES_PASSWORD'),
                            os.getenv('POSTGRES_HOST'),
                            os.getenv('POSTGRES_PORT'))
        self.db.connect()
        # self.db.init_tables()
        super().__init__(request, client_address, server)

    def get_images(self):
        images = self.db.get_images()
        logger.info(f'Got {len(images)} images')
        images_json = \
            [
                dict(zip(['id', 'filename', 'original_name', 'size',
                          'upload_time',
                          'file_type'], image)
                     )
                for image in images
            ]
        logger.info(images_json)
        self.send_json({
            'images': images_json
        })

    def post_upload(self):
        length = int(self.headers.get('Content-Length'))
        if length > MAX_FILE_SIZE:
            logger.warning('File too large')
            self.send_html(ERROR_FILE, 413)
            return

        data = self.rfile.read(length)
        orig_name, ext = os.path.splitext(self.headers.get('Filename'))
        filename = uuid4()
        if ext not in ALLOWED_EXTENSIONS:
            logger.warning('File type not allowed')
            self.send_html(ERROR_FILE, 400)
            return
        self.db.add_image(filename, orig_name, length, ext)
        logger.info(f'File {filename}{ext} uploaded')
        with open(IMAGES_PATH + f'{filename}{ext}', 'wb') as file:
            file.write(data)
        self.send_html('upload_success.html', headers={
            'Location': f'http://localhost/{IMAGES_PATH}{filename}{ext}'})

    def delete_image(self):
        image_id = self.headers.get('Filename')
        if not image_id:
            logger.warning('Filename header not found')
            self.send_html(ERROR_FILE, 404)
            return

        image_path = IMAGES_PATH + image_id
        if not os.path.exists(image_path):
            logger.warning('Image not found')
            self.send_html(ERROR_FILE, 404)
            return os.remove(image_path)

        self.send_json({'Success': 'Image deleted'})

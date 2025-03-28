import json
from http.server import BaseHTTPRequestHandler

from loguru import logger

from Router import Router
from settings import STATIC_PATH


class AdvancedHTTPRequestHandler(BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server):
        self.default_response = lambda: self.send_html('404.html', 404)
        self.router = Router()
        super().__init__(request, client_address, server)

    def send_html(self, file, code=200, headers=None, file_path=STATIC_PATH):
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        if headers:
            for header, value in headers.items():
                self.send_header(header, value)
        self.end_headers()
        with open(file_path + file, 'rb') as file:
            self.wfile.write(file.read())

    def send_json(self, response: dict, code=200, headers=None):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        if headers:
            for header, value in headers.items():
                self.send_header(header, value)
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_GET(self):
        logger.info(f'GET {self.path}')
        handler = self.router.resolve('GET', self.path)
        if handler:
            handler(self)
        else:
            logger.warning(f'No handler for GET {self.path}')
            self.default_response()

    def do_POST(self):
        logger.info(f'POST {self.path}')
        handler = self.router.resolve('POST', self.path)
        if handler:
            handler(self)
        else:
            logger.warning(f'No handler for POST {self.path}')
            self.default_response()

    def do_DELETE(self):
        logger.info(f'DELETE {self.path}')
        handler = self.router.resolve('DELETE', self.path)
        if handler:
            handler(self)
        else:
            logger.warning(f'No handler for DELETE {self.path}')
            self.default_response()

import re

from loguru import logger

from utils import SingletonMeta

logger.add('logs/router.log',
           format='[{time:YYYY-MM-DD HH:mm:ss}] {level}: {message}',
           level='INFO')


class Router(metaclass=SingletonMeta):
    def __init__(self):
        self.routes = {
            'GET': {},
            'POST': {},
            'DELETE': {}
        }

    def add_route(self, method, path, handler):
        pattern = re.compile(path)

        self.routes[method][pattern] = handler
        logger.info(f'Added route: {method} {path} -> {handler.__name__}')

    def resolve(self, method, path):
        logger.info(f'Resolving route: {method} {path}')
        logger.info(f'Available routes of this method: {self.routes[method]}')
        for pattern in self.routes[method]:
            logger.info(f'Checking route: {method} {path} -> {pattern}')
            match = re.match(pattern, path)
            if match:
                return self.routes[method][pattern]

        return None

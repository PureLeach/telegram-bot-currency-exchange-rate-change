from aiogram.contrib.middlewares.logging import LoggingMiddleware

from settings.core import logger


class LoggerMiddleware(LoggingMiddleware):
    def __init__(self, logger=logger):
        self.logger = logger
        super(LoggingMiddleware, self).__init__()

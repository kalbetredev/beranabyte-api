import logging
import logging.handlers
from api.utils.logging.logger import Logger


class DefaultLogger(Logger):
    def __init__(self) -> None:
        level = logging.ERROR
        self.logger = logging.getLogger("default-logger")
        self.logger.setLevel(level)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        formatter = logging.Formatter(
            '%(levelname)s : %(asctime)s : %(name)s : %(message)s')
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def debug(self, source: str, message: str):
        self.logger.debug(f'{source} : {message}')

    def info(self, source: str, message: str):
        self.logger.info(f'{source} : {message}')

    def warning(self, source: str, message: str):
        self.logger.warning(f'{source} : {message}')

    def error(self, source: str, message: str):
        self.logger.error(f'{source} : {message}')

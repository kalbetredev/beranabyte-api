import logging
import logging.handlers
from api.utils.logging.logger import Logger


class DefaultLogger(Logger):
    def __init__(self) -> None:
        level = logging.ERROR
        self.logger = logging.getLogger("default-logger")
        self.logger.setLevel(level)
        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(level)
        formatter = logging.Formatter(
            '%(levelname)s : %(asctime)s : %(name)s : %(message)s')
        consoleHandler.setFormatter(formatter)
        self.logger.addHandler(consoleHandler)

    def debug(self, source: str, message: str):
        self.logger.debug(f'{source} : {message}')

    def info(self, source: str, message: str):
        self.logger.info(f'{source} : {message}')

    def warning(self, source: str, message: str):
        self.logger.warning(f'{source} : {message}')

    def error(self, source: str, message: str):
        self.logger.error(f'{source} : {message}')

import logging
import logging.handlers
from api.utils.logging.logger import Logger


class DefaultLogger(Logger):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            level = logging.ERROR
            cls._instance.logger = logging.getLogger("default-logger")
            cls._instance.logger.setLevel(level)
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)
            formatter = logging.Formatter(
                '%(levelname)s : %(asctime)s : %(name)s : %(message)s')
            console_handler.setFormatter(formatter)
            cls._instance.logger.addHandler(console_handler)

        return cls._instance

    def debug(self, source: str, message: str):
        self._instance.logger.debug(
            f'{source} : {message}'.replace('\n', ' - '))

    def info(self, source: str, message: str):
        self._instance.logger.info(
            f'{source} : {message}'.replace('\n', ' - '))

    def warning(self, source: str, message: str):
        self._instance.logger.warning(
            f'{source} : {message}'.replace('\n', ' - '))

    def error(self, source: str, message: str):
        self._instance.logger.error(
            f'{source} : {message}'.replace('\n', ' - '))

from abc import ABC, abstractmethod


class Logger(ABC):
    @abstractmethod
    def debug(self, source: str, message: str):
        pass

    @abstractmethod
    def info(self, source: str, message: str):
        pass

    @abstractmethod
    def warning(self, source: str, message: str):
        pass

    @abstractmethod
    def error(self, source: str, message: str):
        pass

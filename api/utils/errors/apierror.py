import strawberry
from typing import Optional
from abc import ABC, abstractmethod
from api.utils.constants import messages


@strawberry.type
class Error:
    message: str


@strawberry.type
class BaseError(ABC, BaseException):
    @abstractmethod
    def error(self) -> Error:
        pass


@strawberry.type
class APIError(BaseError):
    def __init__(self, message: Optional[str] = None) -> None:
        self.message = message if message != None else messages.DEFAULT_ERROR_MESSAGE

    @strawberry.field
    def error(self) -> Error:
        return Error(self.message)

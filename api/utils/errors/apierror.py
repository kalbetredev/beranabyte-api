import strawberry
from abc import ABC, abstractmethod


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
    @strawberry.field
    def error(self) -> Error:
        return Error("Error occurred trying to fullfill your request. Please try again.")

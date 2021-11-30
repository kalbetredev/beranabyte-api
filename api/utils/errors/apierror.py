import strawberry
from abc import ABC, abstractmethod


@strawberry.type
class Error:
    message: str


@strawberry.type
class BaseAPIError(ABC, BaseException):
    @abstractmethod
    def error(self) -> Error:
        pass


@strawberry.type
class APIError(BaseAPIError):
    @strawberry.field
    def error(self) -> Error:
        return Error("Error occurred trying to fullfill your request. Please try again.")

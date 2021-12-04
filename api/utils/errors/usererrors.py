import strawberry
from api.utils.errors.apierror import APIError, BaseError, Error
from api.utils.constants import messages


@strawberry.type
class UserNotFound(BaseError):
    @strawberry.field
    def error(self) -> Error:
        return APIError(messages.USER_NOT_FOUND)

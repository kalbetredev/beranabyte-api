import strawberry
from api.utils.errors.apierror import APIError, BaseError, Error
from api.utils.constants import messages


@strawberry.type
class ProjectNotFound(BaseError):
    @strawberry.field
    def error(self) -> Error:
        return APIError(messages.PROJECT_NOT_FOUND)

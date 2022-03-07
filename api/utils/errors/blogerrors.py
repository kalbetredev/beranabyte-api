import strawberry
from api.utils.errors.apierror import APIError, BaseError, Error
from api.utils.constants import messages


@strawberry.type
class BlogNotFound(BaseError):
    @strawberry.field
    def error(self) -> Error:
        return APIError(messages.BLOG_NOT_FOUND)


@strawberry.type
class BlogTitleTaken(BaseError):
    @strawberry.field
    def error(self) -> Error:
        return APIError(messages.BLOG_TITLE_TAKEN)


@strawberry.type
class BlogTitleCanNotBeEmpty(BaseError):
    @strawberry.field
    def error(self) -> Error:
        return APIError(messages.BLOG_TITLE_EMPTY)

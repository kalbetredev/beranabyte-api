import strawberry
from typing import Optional
from api.utils.errors.apierror import BaseAPIError, Error


@strawberry.type
class BlogCreationFailedError(BaseAPIError):
    def __init__(self, message_detail: Optional[str] = ""):
        self.message_detail = message_detail

    @strawberry.field
    def error(self) -> Error:
        return Error(f"Error occurred trying to create your blog. {self.message_detail}".strip())


@strawberry.type
class BlogNotFoundError(BaseAPIError):
    def __init__(self, blog_id: str):
        self.blog_id = blog_id

    @strawberry.field
    def error(self) -> Error:
        return Error(f"The blog with id {self.blog_id} could not be found")


@strawberry.type
class BlogUpdateFailedError(BaseAPIError):
    def __init__(self, message_detail: Optional[str] = ""):
        self.message_detail = message_detail

    @strawberry.field
    def error(self) -> Error:
        return Error(f"Error occurred trying to update your blog. {self.message_detail}".strip())

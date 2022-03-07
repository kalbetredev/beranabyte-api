from typing import List, Union
import strawberry
from strawberry.types import Info
from api.database.database import Database
from api.database.models.blog_model import BlogModel
from api.schemas.types.blog import Blog, NewBlog, UpdatedBlog
from api.utils.errors.apierror import APIError
from api.utils.errors.blogerrors import BlogNotFound
from api.schemas.types.responses import Success
from api.utils.constants import messages
from api.utils.errors.validationerror import InputError, InputValidationError
from bson.objectid import ObjectId

DeleteBlogResult = strawberry.union(
    "DeleteBlogResult", [Success, BlogNotFound, APIError]
)


def validate_new_blog_inputs(
    new_blog: NewBlog,
) -> List[InputError]:
    validation_errors: List[InputError] = []
    if new_blog.title is None or new_blog.title == "":
        validation_errors.append(
            InputError(input="title", message=messages.BLOG_TITLE_EMPTY)
        )

    if new_blog.topic is None or new_blog.topic == "":
        validation_errors.append(
            InputError(input="topic", message=messages.BLOG_TOPIC_EMPTY)
        )

    return validation_errors

ModifyBlogResult = strawberry.union(
    "ModifyBlogResult",
    [Blog, BlogNotFound, APIError],
)

DeleteBlogResult = strawberry.union(
    "DeleteBlogResult", [Success, BlogNotFound, APIError]
)


@strawberry.type
class BlogMutation:
    @strawberry.mutation
    async def add_new_blog(
        self, new_blog: NewBlog, info: Info
    ) -> Union[Blog, InputValidationError, APIError]:
        try:
            db: Database = info.context.db

            validation_errors: List[InputError] = validate_new_blog_inputs(new_blog)

            if len(validation_errors) > 0:
                return InputValidationError(validation_errors)

            if await db.get_blog_by_title(new_blog.title) is not None:
                return InputValidationError(
                    [InputError(input="title", message=messages.BLOG_TITLE_TAKEN)]
                )

            blog = BlogModel(**new_blog.__dict__)
            saved_blog = await db.add_new_blog(blog)
            return Blog(**saved_blog.dict()) if saved_blog is not None else APIError()
        except Exception as error:
            info.context.logger.error(__name__, error)
            return APIError()

    @strawberry.mutation
    def update_blog(self, updated_blog: UpdatedBlog, info: Info) -> ModifyBlogResult:
        try:
            db: Database = info.context.db
            return db.update_blog(updated_blog)
        except BlogNotFound as error:
            return error
        except Exception as error:
            info.context.logger.error(__name__, error)
            return APIError()

    @strawberry.mutation
    def delete_blog(self, blog_id: str, info: Info) -> DeleteBlogResult:
        try:
            db: Database = info.context.db
            db.delete_blog(blog_id)
            return Success(messages.BLOG_DELETED_SUCCESSFULLY)
        except BlogNotFound as error:
            return error
        except Exception as error:
            info.context.logger.error(__name__, error)
            return APIError()

    @strawberry.mutation
    def publish_blog(self, blog_id: str, info: Info) -> ModifyBlogResult:
        try:
            db: Database = info.context.db
            return db.publish_blog(blog_id)
        except BlogNotFound as error:
            return error
        except Exception as error:
            info.context.logger.error(__name__, error)
            return APIError()

    @strawberry.mutation
    def increment_blog_view_count(self, blog_id: str, info: Info) -> ModifyBlogResult:
        try:
            db: Database = info.context.db
            return db.increment_blog_view_count(blog_id)
        except BlogNotFound as error:
            return error
        except Exception as error:
            info.context.logger.error(__name__, error)
            return APIError()

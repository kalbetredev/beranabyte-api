from typing import List, Union
import strawberry
from strawberry.types import Info
from api.database.database import Database
from api.database.models.blog_model import BlogModel
from api.schemas.types.blog import Blog, NewBlog, UpdatedBlog
from api.schemas.validators.blog_validators import (
    validate_blog_update_inputs,
    validate_new_blog_inputs,
)
from api.utils.errors.apierror import APIError
from api.utils.errors.blogerrors import BlogNotFound
from api.schemas.types.responses import ActionResult
from api.utils.constants import messages
from api.utils.errors.validationerror import InputError, InputValidationError
from api.utils.helpers import update_attributes
from bson.objectid import ObjectId


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
    async def update_blog(
        self, id: str, updated_blog: UpdatedBlog, info: Info
    ) -> Union[Blog, BlogNotFound, InputValidationError, APIError]:
        try:
            db: Database = info.context.db

            if not ObjectId.is_valid(id):
                return InputValidationError(
                    [InputError(input="id", message=messages.INVALID_ID)]
                )
            else:
                existing_blog = await db.get_blog_by_id(id)
                if existing_blog is None:
                    return BlogNotFound()

                validation_errors: List[InputError] = validate_blog_update_inputs(
                    updated_blog
                )

                if len(validation_errors) > 0:
                    return InputValidationError(validation_errors)

                if (
                    existing_blog.title != updated_blog.title
                    and await db.get_blog_by_title(updated_blog.title) is not None
                ):
                    return InputValidationError(
                        [InputError(input="title", message=messages.BLOG_TITLE_TAKEN)]
                    )

                update_attributes(updated=updated_blog, existing=existing_blog)
                saved_blog = await db.update_blog(existing_blog)
                return (
                    Blog(**saved_blog.dict()) if saved_blog is not None else APIError()
                )
        except Exception as error:
            info.context.logger.error(__name__, error)
            return APIError()

    @strawberry.mutation
    async def delete_blog(self, id: str, info: Info) -> Union[ActionResult, APIError]:
        try:
            db: Database = info.context.db

            if not ObjectId.is_valid(id):
                return ActionResult(
                    is_successfull=False,
                    message=messages.INVALID_ID,
                )
            else:
                existing_blog = await db.get_blog_by_id(id)
                if existing_blog is None:
                    return ActionResult(
                        is_successfull=False,
                        message=messages.BLOG_NOT_FOUND,
                    )

                result = await db.delete_blog(id)
                return ActionResult(
                    is_successfull=result,
                    message=(
                        "Blog deleted successfully"
                        if result
                        else "Unable to delete the blog"
                    ),
                )

        except Exception as error:
            info.context.logger.error(__name__, error)
            return APIError()

    @strawberry.mutation
    async def increment_blog_view_count(
        self, id: str, info: Info
    ) -> Union[Blog, BlogNotFound, InputValidationError, APIError]:
        try:
            db: Database = info.context.db

            if not ObjectId.is_valid(id):
                return InputValidationError(
                    [InputError(input="id", message=messages.INVALID_ID)]
                )
            else:
                existing_blog = await db.get_blog_by_id(id)
                if existing_blog is None:
                    return BlogNotFound()

                existing_blog.view_count += 1
                saved_blog = await db.update_blog(existing_blog)
                return (
                    Blog(**saved_blog.dict()) if saved_blog is not None else APIError()
                )
        except BlogNotFound as error:
            return error
        except Exception as error:
            info.context.logger.error(__name__, error)
            return APIError()

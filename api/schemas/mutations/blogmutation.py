
import strawberry
from api.schemas.types.blog import Blog, NewBlog, UpdatedBlog
from api.utils.errors.apierror import APIError
from api.utils.errors.blogerrors import BlogCreationFailedError, BlogUpdateFailedError
from api import app


CreateNewBlogResponse = strawberry.union(
    "CreateNewBlogResponse",
    [Blog, BlogCreationFailedError, APIError]
)

UpdateBlogResponse = strawberry.union(
    "UpdateBlogResponse",
    [Blog, BlogUpdateFailedError, APIError]
)


@strawberry.type
class BlogMutation:
    @strawberry.mutation
    def create_new_blog(self, new_blog: NewBlog) -> CreateNewBlogResponse:
        try:
            return app.database.create_new_blog(new_blog)
        except BlogCreationFailedError as error:
            return error
        except Exception as error:
            app.logger.error(__name__, error)
            return APIError()

    @strawberry.mutation
    def update_blog(self, updated_blog: UpdatedBlog) -> UpdateBlogResponse:
        try:
            return app.database.update_blog(updated_blog)
        except BlogCreationFailedError as error:
            return error
        except Exception as error:
            app.logger.error(__name__, error)
            return APIError()

import strawberry
from api.schemas.types.blog import Blog, NewBlog
from api.utils.errors.apierror import APIError
from api.utils.errors.blogerrors import BlogCreationFailedError
from api import app


CreateNewBlogResponse = strawberry.union(
    "CreateNewBlogResponse",
    [Blog, BlogCreationFailedError, APIError]
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

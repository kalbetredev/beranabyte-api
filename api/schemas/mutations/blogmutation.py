import strawberry
from api.schemas.types.blog import Blog, NewBlog, UpdatedBlog
from api.utils.errors.apierror import APIError
from api.utils.errors.blogerrors import BlogNotFound, BlogTitleTaken
from api.schemas.types.responses import Success
from api.utils.constants import messages
from api import app


CreateNewBlogResult = strawberry.union(
    "CreateNewBlogResult", [Blog, BlogTitleTaken, APIError]
)

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
    def create_new_blog(self, new_blog: NewBlog) -> CreateNewBlogResult:
        try:
            return app.database.create_new_blog(new_blog)
        except BlogTitleTaken as error:
            return error
        except Exception as error:
            app.logger.error(__name__, error)
            return APIError()

    @strawberry.mutation
    def update_blog(self, updated_blog: UpdatedBlog) -> ModifyBlogResult:
        try:
            return app.database.update_blog(updated_blog)
        except BlogNotFound as error:
            return error
        except Exception as error:
            app.logger.error(__name__, error)
            return APIError()

    @strawberry.mutation
    def delete_blog(self, blog_id: str) -> DeleteBlogResult:
        try:
            app.database.delete_blog(blog_id)
            return Success(messages.BLOG_DELETED_SUCCESSFULLY)
        except BlogNotFound as error:
            return error
        except Exception as error:
            app.logger.error(__name__, error)
            return APIError()

    @strawberry.mutation
    def publish_blog(self, blog_id: str) -> ModifyBlogResult:
        try:
            return app.database.publish_blog(blog_id)
        except BlogNotFound as error:
            return error
        except Exception as error:
            app.logger.error(__name__, error)
            return APIError()

    @strawberry.mutation
    def increment_blog_view_count(self, blog_id: str) -> ModifyBlogResult:
        try:
            return app.database.increment_blog_view_count(blog_id)
        except BlogNotFound as error:
            return error
        except Exception as error:
            app.logger.error(__name__, error)
            return APIError()

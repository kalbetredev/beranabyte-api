import strawberry
from strawberry.types import Info
from api.database.database import Database
from api.schemas.types.blog import Blog, NewBlog, UpdatedBlog
from api.utils.errors.apierror import APIError
from api.utils.errors.blogerrors import BlogNotFound, BlogTitleTaken
from api.schemas.types.responses import Success
from api.utils.constants import messages


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
    def create_new_blog(self, new_blog: NewBlog, info: Info) -> CreateNewBlogResult:
        try:
            db: Database = info.context.db
            return db.create_new_blog(new_blog)
        except BlogTitleTaken as error:
            return error
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

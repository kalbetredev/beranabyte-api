import strawberry
from typing import List, Optional, Union
from api.database.database import Database
from api.database.models import Sort
from api.schemas.types.blog import Blog
from api.utils.errors.apierror import APIError
from api.utils.errors.blogerrors import BlogNotFound
from strawberry.types import Info


@strawberry.type
class GetBlogsResult:
    blogs: List[Blog]


@strawberry.type
class BlogQuery:
    @strawberry.field
    def get_blogs(
        self,
        info: Info,
        user_id: Optional[str] = None,
        is_published: Optional[bool] = None,
        sort_by: Optional[str] = None,
        sort_dir: Optional[int] = 1,
    ) -> Union[GetBlogsResult, APIError]:
        try:
            blogs = GetBlogsResult([])
            db: Database = info.context.db

            query = {}
            if user_id:
                query["user_id"] = user_id
            if is_published is not None:
                query["is_published"] = is_published

            sort = None
            if sort_by is not None:
                sort = Sort(sort_by, sort_dir)

            blogs.blogs = db.get_blogs(query=query, sort=sort)
            return blogs
        except Exception as error:
            info.context.logger.error(__name__, error)
            return APIError()

    @strawberry.field
    def get_blog(
        self,
        blog_id: str,
        info: Info,
    ) -> Union[Blog, BlogNotFound, APIError]:
        try:
            db: Database = info.context.db
            blog = db.get_blog(blog_id)
            if blog == None:
                return BlogNotFound()
            else:
                return blog
        except Exception as error:
            info.context.logger.error(__name__, error)
            return APIError()

    @strawberry.field
    def get_topics(
        self,
        info: Info,
    ) -> List[str]:
        db: Database = info.context.db
        return db.get_all_topics()

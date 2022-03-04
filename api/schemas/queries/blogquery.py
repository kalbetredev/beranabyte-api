from math import ceil
import strawberry
from typing import List, Optional, Union
from api.database.database import Database
from api.database.models import Page, Sort
from api.schemas.types.blog import Blog
from api.utils.errors.apierror import APIError
from api.utils.errors.blogerrors import BlogNotFound
from strawberry.types import Info


@strawberry.type
class GetBlogsResult:
    blogs: List[Blog]
    page_num: int
    page_count: int


def get_page_with_count(max_count, page_size, page_num):
    page_size = page_size if page_size >= 1 else 10
    page_count = ceil(max_count / page_size)
    page_num = 1 if page_num < 1 else page_num
    page_num = page_count if page_num > page_count else page_num
    page = Page(number=page_num, size=page_size)
    return (page, page_count)


@strawberry.type
class BlogQuery:
    @strawberry.field
    async def get_blogs(
        self,
        info: Info,
        user_id: Optional[str] = None,
        is_published: Optional[bool] = None,
        sort_by: Optional[str] = None,
        sort_dir: Optional[int] = 1,
        page_num: Optional[int] = 1,
        page_size: Optional[int] = 10,
    ) -> Union[GetBlogsResult, APIError]:
        try:
            db: Database = info.context.db

            query = {}
            if user_id:
                query["user_id"] = user_id
            if is_published is not None:
                query["is_published"] = is_published

            sort = None
            if sort_by is not None:
                sort = Sort(sort_by, sort_dir)

            page_size = page_size if page_size >= 1 else 10
            page_count = ceil((await db.get_blogs_count()) / page_size)
            page_num = 1 if page_num < 1 else page_num
            page_num = page_count if page_num > page_count else page_num
            page = Page(number=page_num, size=page_size)

            blogs = await db.get_blogs(query=query, sort=sort, page=page)
            return GetBlogsResult(blogs, page_num=page_num, page_count=page_count)
        except Exception as error:
            info.context.logger.error(__name__, error)
            return APIError()

    @strawberry.field
    async def search_blogs(
        self,
        info: Info,
        text: str,
        page_num: Optional[int] = 1,
        page_size: Optional[int] = 10,
    ) -> Union[GetBlogsResult, APIError]:
        try:
            db: Database = info.context.db

            search_limit = 50
            (page, page_count) = get_page_with_count(
                search_limit,
                page_size,
                page_num,
            )

            blogs = await db.search_blogs(
                text=text,
                page=page,
                max_limit=search_limit,
            )
            return GetBlogsResult(blogs, page_num=page.number, page_count=page_count)
        except Exception as error:
            info.context.logger.error(__name__, error)
            return APIError()

    @strawberry.field
    async def get_blog(
        self,
        blog_id: str,
        info: Info,
    ) -> Union[Blog, BlogNotFound, APIError]:
        try:
            db: Database = info.context.db
            blog = await db.get_blog(blog_id)
            if blog == None:
                return BlogNotFound()
            else:
                return blog
        except Exception as error:
            info.context.logger.error(__name__, error)
            return APIError()

    @strawberry.field
    async def get_topics(
        self,
        info: Info,
    ) -> List[str]:
        db: Database = info.context.db
        return await db.get_all_topics()

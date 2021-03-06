from typing import List, Optional, Union
from api.database.database import Database
from api.database.models.sortmodel import SortModel
from api.database.models.usermodel import UserModel, UserRole
from api.schemas.types.blog import Blog, BlogsResult
from api.schemas import utils
from api.utils.errors.apierror import APIError
from api.utils.errors.blogerrors import BlogNotFound
from strawberry.types import Info


async def get_blogs(
    info: Info,
    is_published: Optional[bool] = None,
    sort_by: Optional[str] = None,
    sort_dir: Optional[int] = 1,
    page_num: Optional[int] = 1,
    page_size: Optional[int] = 10,
) -> Union[BlogsResult, APIError]:
    try:
        db: Database = info.context.db

        query = {"is_published": True}

        if not is_published and info.context.current_user is not None:
            user: UserModel = await db.get_user(info.context.current_user.uid)
            if user.role == UserRole.ADMIN:
                if is_published is None:
                    del query["is_published"]
                else:
                    query["is_published"] = False
            elif is_published is not None:
                return BlogsResult([], page_num=1, page_count=1)

        sort = None
        if sort_by is not None:
            sort = SortModel(sort_by, sort_dir)

        (page, page_count) = utils.get_page_with_count(
            await db.get_blogs_count(),
            page_size,
            page_num,
        )

        blog_models = await db.get_blogs(query=query, sort=sort, page=page)
        blogs = [Blog(**blog_model.dict()) for blog_model in blog_models]
        return BlogsResult(blogs, page_num=page_num, page_count=page_count)
    except Exception as error:
        info.context.logger.error(__name__, error)
        return APIError()


async def search_blogs(
    info: Info,
    text: str,
    page_num: Optional[int] = 1,
    page_size: Optional[int] = 10,
) -> Union[BlogsResult, APIError]:
    try:
        db: Database = info.context.db

        search_limit = 50
        (page, page_count) = utils.get_page_with_count(
            search_limit,
            page_size,
            page_num,
        )

        blog_models = await db.search_blogs(
            text=text,
            page=page,
            max_limit=search_limit,
        )
        blogs = [Blog(**blog_model.dict()) for blog_model in blog_models]
        return BlogsResult(blogs, page_num=page.number, page_count=page_count)
    except Exception as error:
        info.context.logger.error(__name__, error)
        return APIError()


async def get_blog(
    blog_id: str,
    info: Info,
) -> Union[Blog, BlogNotFound, APIError]:
    try:
        db: Database = info.context.db
        blog_model = await db.get_blog_by_id(blog_id)
        return Blog(**blog_model.dict()) if blog_model is not None else BlogNotFound()
    except Exception as error:
        info.context.logger.error(__name__, error)
        return APIError()


async def get_topics(
    info: Info,
) -> List[str]:
    db: Database = info.context.db
    return await db.get_all_topics()

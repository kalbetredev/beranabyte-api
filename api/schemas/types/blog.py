import strawberry
from typing import List, Optional

from api.database.models.blogmodel import BlogBase


@strawberry.experimental.pydantic.type(model=BlogBase, all_fields=True)
class Blog:
    id: str


@strawberry.input
class NewBlog:
    title: str
    topic: str
    summary: Optional[str] = ""
    image_url: Optional[str] = ""
    content: Optional[str] = ""
    is_featured: Optional[bool] = False


@strawberry.input
class UpdatedBlog:
    title: Optional[str] = None
    topic: Optional[str] = None
    summary: Optional[str] = None
    image_url: Optional[str] = None
    content: Optional[str] = None
    is_published: Optional[bool] = None


@strawberry.type
class BlogsResult:
    blogs: List[Blog]
    page_num: int
    page_count: int

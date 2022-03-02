from __future__ import annotations
from typing import Optional
import strawberry
from datetime import datetime
from api.schemas.types.user import User


@strawberry.interface
class BlogBase:
    id: strawberry.ID
    title: str


@strawberry.input
class NewBlog:
    title: str
    topic: Optional[str] = None
    summary: Optional[str] = None
    image_url: Optional[str] = None
    content: Optional[str] = None
    is_featured: Optional[bool] = False


@strawberry.input
class UpdatedBlog(NewBlog, BlogBase):
    title: Optional[str] = None
    is_published: Optional[bool] = None


@strawberry.type
class Blog(NewBlog, BlogBase):
    is_published: Optional[bool] = False
    modified_on: Optional[datetime] = datetime.now()
    view_count: Optional[int] = 0
    published_on: Optional[datetime] = None
    author: Optional[User] = None

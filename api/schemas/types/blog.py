from __future__ import annotations
import strawberry
from typing import Optional
from datetime import datetime
from api.schemas.types.user import User


@strawberry.type
class Blog:
    id: str
    title: str
    topic: Optional[str] = None
    summary: Optional[str] = None
    image_url: Optional[str] = None
    content: Optional[str] = None
    is_featured: Optional[bool] = False
    is_published: Optional[bool] = False
    modified_on: Optional[datetime] = datetime.now()
    view_count: Optional[int] = 0
    published_on: Optional[datetime] = None
    author: Optional[User] = None


@strawberry.input
class NewBlog:
    title: str
    topic: Optional[str] = None
    summary: Optional[str] = None
    image_url: Optional[str] = None
    content: Optional[str] = None
    is_featured: Optional[bool] = False


@strawberry.input
class UpdatedBlog(NewBlog):
    title: Optional[str] = None
    is_published: Optional[bool] = None

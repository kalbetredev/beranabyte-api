from __future__ import annotations
from typing import Optional
import strawberry
from datetime import datetime
from api.schemas.types.user import User
from api import app


@strawberry.input
class NewBlog:
    title: str
    topic: str
    summary: str
    image_url: str
    content: str


@strawberry.input
class UpdatedBlog:
    id: strawberry.ID
    title: Optional[str] = None
    topic: Optional[str] = None
    summary: Optional[str] = None
    image_url: Optional[str] = None
    content: Optional[str] = None
    is_featured: Optional[bool] = None
    is_published: Optional[bool] = None


@strawberry.type
class Blog(NewBlog):
    id: strawberry.ID
    is_featured: Optional[bool] = False
    is_published: Optional[bool] = False
    modified_on: Optional[datetime] = datetime.now()
    view_count: Optional[int] = 0
    published_on: Optional[datetime] = None

    @strawberry.field
    def author(root: Blog) -> User:
        return app.database.get_blog_author(root.id)

    @classmethod
    def fromNewBlog(cls, id: str, new_blog: NewBlog):
        return Blog(
            id=id,
            title=new_blog.title,
            topic=new_blog.topic,
            summary=new_blog.summary,
            image_url=new_blog.image_url,
            content=new_blog.content,
        )

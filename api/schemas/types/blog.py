from __future__ import annotations
from typing import Optional
import strawberry
from datetime import datetime
from api.schemas.types.user import User
from api import app
from api.utils.helpers import updateAttributes


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

    @strawberry.field
    def author(root: Blog) -> User:
        return app.database.get_blog_author(root.id)

    @classmethod
    def fromNewBlog(cls, id: str, new_blog: NewBlog):
        blog = Blog(id=id, title=new_blog.title)
        updateAttributes(blog, **new_blog.__dict__)
        return blog

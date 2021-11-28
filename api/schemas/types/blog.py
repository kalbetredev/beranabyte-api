from __future__ import annotations
import strawberry
from datetime import datetime
from api.schemas.types.user import User
from api import app


def author(root: Blog) -> User:
    return app.database.get_blog_author(root.id)


@strawberry.type
class Blog:
    id: strawberry.ID
    title: str
    topic: str
    is_featured: bool
    is_published: bool
    published_on: datetime
    modified_on: datetime
    summary: str
    image_url: str
    view_count: str
    content: str
    author: User = strawberry.field(resolver=author)

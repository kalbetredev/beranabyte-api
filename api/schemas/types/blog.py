import strawberry
from datetime import datetime


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

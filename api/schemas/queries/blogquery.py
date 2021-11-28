import strawberry
from typing import List
from api.schemas.types.blog import Blog
from typing import List
from api import app


def get_blogs() -> List[Blog]:
    return app.database.get_all_blogs()


@strawberry.type
class BlogQuery:
    blogs: List[Blog] = strawberry.field(resolver=get_blogs)

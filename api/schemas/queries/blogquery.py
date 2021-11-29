import strawberry
from typing import List, Optional
from api.schemas.types.blog import Blog
from typing import List
from api import app


def get_blogs(is_published: Optional[bool] = None) -> List[Blog]:
    if is_published == None:
        return app.database.get_all_blogs()
    else:
        return app.database.get_blogs(is_published)


def get_topics() -> List[str]:
    return app.database.get_all_topics()


@strawberry.type
class BlogQuery:
    blogs: List[Blog] = strawberry.field(resolver=get_blogs)
    topics: List[str] = strawberry.field(resolver=get_topics)

    @strawberry.field
    def user_blogs(self, user_id: str) -> List[Blog]:
        return app.database.get_user_blogs(user_id)

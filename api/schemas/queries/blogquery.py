import strawberry
from typing import List, Optional
from api.schemas.types.blog import Blog
from typing import List
from api import app


@strawberry.type
class BlogQuery:
    @strawberry.field
    def blogs(self, is_published: Optional[bool] = None) -> List[Blog]:
        if is_published == None:
            return app.database.get_all_blogs()
        else:
            return app.database.get_blogs(is_published)

    @strawberry.field
    def topics(self) -> List[str]:
        return app.database.get_all_topics()

    @strawberry.field
    def user_blogs(self, user_id: str) -> List[Blog]:
        return app.database.get_user_blogs(user_id)

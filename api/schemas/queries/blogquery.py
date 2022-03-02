import strawberry
from typing import List, Optional
from api.database.database import Database
from api.schemas.types.blog import Blog
from typing import List
from api.utils.errors.blogerrors import BlogNotFound
from strawberry.types import Info

GetBlogResponse = strawberry.union("GetBlogResponse", [Blog, BlogNotFound])


@strawberry.type
class BlogQuery:
    @strawberry.field
    def blogs(self, info: Info, is_published: Optional[bool] = None) -> List[Blog]:
        db: Database = info.context.db
        return db.get_blogs(is_published)

    @strawberry.field
    def blog(
        self,
        blog_id: str,
        info: Info,
    ) -> GetBlogResponse:
        db: Database = info.context.db
        blog = db.get_blog(blog_id)
        if blog == None:
            return BlogNotFound()
        else:
            return blog

    @strawberry.field
    def topics(
        self,
        info: Info,
    ) -> List[str]:
        db: Database = info.context.db
        return db.get_all_topics()

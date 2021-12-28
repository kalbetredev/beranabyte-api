import strawberry
from typing import List, Optional
from api.schemas.types.blog import Blog
from typing import List
from api import app
from api.utils.errors.blogerrors import BlogNotFound


GetBlogResponse = strawberry.union("GetBlogResponse", [Blog, BlogNotFound])


@strawberry.type
class BlogQuery:
    @strawberry.field
    def blogs(self, is_published: Optional[bool] = None) -> List[Blog]:
        if is_published == None:
            return app.database.get_all_blogs()
        else:
            return app.database.get_blogs(is_published)

    @strawberry.field
    def blog(self, blog_id: str) -> GetBlogResponse:
        blog = app.database.get_blog_by_id(blog_id)
        if blog == None:
            return BlogNotFound()
        else:
            return blog

    @strawberry.field
    def topics(self) -> List[str]:
        return app.database.get_all_topics()

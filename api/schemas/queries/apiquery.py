import strawberry
from api.schemas.queries.blogquery import BlogQuery


@strawberry.type
class Query(BlogQuery):
    pass

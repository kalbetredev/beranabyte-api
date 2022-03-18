import strawberry
from api.schemas.queries.blogquery import BlogQuery
from api.schemas.queries.projectquery import ProjectQuery
from api.schemas.queries.userquery import UserQuery


@strawberry.type
class Query(BlogQuery, UserQuery, ProjectQuery):
    pass

import strawberry
from typing import List, Union
from api.schemas.resolvers.blogresovers import (
    get_blog,
    get_blogs,
    search_blogs,
    get_topics,
)
from api.schemas.types.blog import Blog, BlogsResult
from api.utils.errors.apierror import APIError
from api.utils.errors.blogerrors import BlogNotFound


@strawberry.type
class BlogQuery:
    blogs: Union[BlogsResult, APIError] = strawberry.field(resolver=get_blogs)
    search_blogs: Union[BlogsResult, APIError] = strawberry.field(resolver=search_blogs)
    blog: Union[Blog, BlogNotFound, APIError] = strawberry.field(resolver=get_blog)
    topics: List[str] = strawberry.field(resolver=get_topics)

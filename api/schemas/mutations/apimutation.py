import strawberry
from api.schemas.mutations.blogmutation import BlogMutation


@strawberry.type
class Mutation(BlogMutation):
    pass

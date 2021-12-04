import strawberry
from api.schemas.mutations.blogmutation import BlogMutation
from api.schemas.mutations.usermutation import UserMutation


@strawberry.type
class Mutation(BlogMutation, UserMutation):
    pass

import strawberry
from api.schemas.mutations.blogmutation import BlogMutation
from api.schemas.mutations.imagemutation import ImageMutation


@strawberry.type
class Mutation(BlogMutation, ImageMutation):
    pass

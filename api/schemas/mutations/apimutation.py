import strawberry
from api.schemas.mutations.blogmutation import BlogMutation
from api.schemas.mutations.image_mutation import ImageMutation


@strawberry.type
class Mutation(BlogMutation, ImageMutation):
    pass

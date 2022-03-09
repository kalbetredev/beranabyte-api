import strawberry
from api.schemas.mutations.blogmutation import BlogMutation
from api.schemas.mutations.imagemutation import ImageMutation
from api.schemas.mutations.mailmutations import MailMutation


@strawberry.type
class Mutation(BlogMutation, ImageMutation, MailMutation):
    pass

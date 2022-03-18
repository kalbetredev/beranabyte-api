import strawberry
from api.schemas.mutations.blogmutation import BlogMutation
from api.schemas.mutations.imagemutation import ImageMutation
from api.schemas.mutations.mailmutations import MailMutation
from api.schemas.mutations.projectmutation import ProjectMutation


@strawberry.type
class Mutation(
    BlogMutation,
    ImageMutation,
    MailMutation,
    ProjectMutation,
):
    pass

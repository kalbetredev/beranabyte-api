import strawberry


def get_blog() -> str:
    return "My Blog"


@strawberry.type
class Query():
    blog = strawberry.field(resolver=get_blog)

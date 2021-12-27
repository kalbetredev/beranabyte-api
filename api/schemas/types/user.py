import strawberry


@strawberry.type
class User:
    id: strawberry.ID
    email: str

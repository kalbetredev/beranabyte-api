import strawberry


@strawberry.interface
class UserBase:
    email: str


@strawberry.input
class UserAuth(UserBase):
    password: str


@strawberry.type
class User(UserBase):
    id: strawberry.ID

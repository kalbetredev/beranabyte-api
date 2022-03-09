import strawberry

from api.database.models.usermodel import UserBase


@strawberry.experimental.pydantic.type(model=UserBase, all_fields=True)
class User:
    email: str

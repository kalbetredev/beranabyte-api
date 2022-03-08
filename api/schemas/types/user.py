import strawberry

from api.database.models.user_model import UserBase


@strawberry.experimental.pydantic.type(model=UserBase, all_fields=True)
class User:
    email: str

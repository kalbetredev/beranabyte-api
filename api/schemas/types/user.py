import strawberry
from enum import Enum
from typing import Optional


class UserRole(Enum):
    ADMIN = "admin"
    AUTHOR = "author"
    USER = "user"


@strawberry.interface
class UserBase:
    user_id: strawberry.ID
    email: str


@strawberry.type
class UserMeta:
    user_id: strawberry.ID
    role: str
    photo_url: Optional[str] = None


@strawberry.type
class User(UserMeta, UserBase):
    pass

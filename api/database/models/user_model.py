import strawberry
from enum import Enum
from pydantic import BaseModel, Field

from api.auth.models.mongomodel import MongoModel


@strawberry.enum
class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"


class UserBase(BaseModel):
    user_id: str
    role: UserRole
    photo_url: str = Field(default="", kw_only=True)


class UserModel(MongoModel, UserBase):
    pass

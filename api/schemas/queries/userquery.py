from typing import Union
import strawberry
from api.schemas.resolvers.user_resolvers import get_current_user, get_user
from api.schemas.types.user import User
from api.utils.errors.apierror import APIError
from api.utils.errors.usererrors import UserNotAuthenticated, UserNotFound


@strawberry.type
class UserQuery:
    user: Union[User, UserNotFound, APIError] = strawberry.field(resolver=get_user)
    current_user: Union[User, UserNotAuthenticated, APIError] = strawberry.field(
        resolver=get_current_user
    )

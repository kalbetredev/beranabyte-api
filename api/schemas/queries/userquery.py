import strawberry
from api.schemas.types.user import User
from api.utils.errors.usererrors import UserNotFound
from api import app

GetUserResponse = strawberry.union(
    "GetUserResponse",
    [User, UserNotFound]
)


@strawberry.type
class UserQuery:
    @strawberry.field
    def user(self, user_id: str) -> GetUserResponse:
        user = app.database.get_user_by_id(user_id)
        if user == None:
            return UserNotFound()
        else:
            return user

import strawberry
from api.schemas.types.user import User
from api.utils.errors.usererrors import UserNotAuthenticated, UserNotFound
from api import app
from strawberry.types import Info

GetUserResponse = strawberry.union("GetUserResponse", [User, UserNotFound])
GetCurrentUserResponse = strawberry.union(
    "GetCurrentUserResponse", [User, UserNotAuthenticated]
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

    @strawberry.field
    def current_user(self, info: Info) -> GetCurrentUserResponse:
        return (
            User(info.context.user.uid, info.context.user.email)
            if info.context.user is not None
            else UserNotAuthenticated()
        )

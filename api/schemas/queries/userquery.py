import strawberry
from api.auth.firebaseadmin import get_user_record
from api.database.database import Database
from api.schemas.types.user import User
from api.utils.errors.usererrors import UserNotAuthenticated, UserNotFound
from strawberry.types import Info

GetUserResponse = strawberry.union("GetUserResponse", [User, UserNotFound])
GetCurrentUserResponse = strawberry.union(
    "GetCurrentUserResponse", [User, UserNotAuthenticated]
)


@strawberry.type
class UserQuery:
    @strawberry.field
    async def user(self, user_id: str, info: Info) -> GetUserResponse:
        db: Database = info.context.db
        user_record = get_user_record(user_id)
        if user_record == None:
            return UserNotFound()
        else:
            user_meta = await db.get_user_meta(user_record.uid)
            return User(
                email=user_record.email,
                **user_meta.__dict__,
            )

    @strawberry.field
    async def current_user(self, info: Info) -> GetCurrentUserResponse:
        db: Database = info.context.db
        if info.context.current_user is not None:
            user_meta = await db.get_user_meta(info.context.current_user.uid)
            return User(
                email=info.context.current_user.email,
                **user_meta.__dict__,
            )
        else:
            return UserNotAuthenticated()

from typing import Union
from api.auth.firebaseadmin import get_user_record
from api.database.database import Database
from api.schemas.types.user import User
from api.utils.errors.apierror import APIError
from api.utils.errors.usererrors import UserNotAuthenticated, UserNotFound
from strawberry.types import Info


async def get_user(user_id: str, info: Info) -> Union[User, UserNotFound, APIError]:
    try:
        db: Database = info.context.db
        user_record = get_user_record(user_id)
        user_data = await db.get_user(user_id)

        if user_record is None or user_data is None:
            return UserNotFound()
        else:
            data = user_data.dict()
            del data["id"]
            return User(
                email=user_record.email,
                **data,
            )
    except Exception as error:
        info.context.logger.error(__name__, error)
        return APIError()


async def get_current_user(info: Info) -> Union[User, UserNotAuthenticated, APIError]:
    try:
        if info.context.current_user is not None:
            db: Database = info.context.db
            user_id = info.context.current_user.uid
            email = info.context.current_user.email
            user_data = await db.get_user(user_id)

            if user_data is None:
                return UserNotAuthenticated()
            else:
                data = user_data.dict()
                del data["id"]
                return User(email=email, **data)
        else:
            return UserNotAuthenticated()
    except Exception as error:
        info.context.logger.error(__name__, error)
        return APIError()

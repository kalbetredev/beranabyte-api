from strawberry.types import Info
from api.database.database import Database
from api.database.models.user_model import UserModel, UserRole


async def is_current_user_admin(info: Info) -> bool:
    db: Database = info.context.db
    if info.context.current_user is None:
        return False
    else:
        user: UserModel = await db.get_user(info.context.current_user.uid)
        return user.role == UserRole.ADMIN

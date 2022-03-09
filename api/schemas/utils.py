import imghdr
import os
from strawberry.types import Info
from api.database.database import Database
from api.database.models.usermodel import UserModel, UserRole


async def is_current_user_admin(info: Info) -> bool:
    db: Database = info.context.db
    if info.context.current_user is None:
        return False
    else:
        user: UserModel = await db.get_user(info.context.current_user.uid)
        return user.role == UserRole.ADMIN


def update_attributes(updated, existing) -> None:

    for attr, value in updated.__dict__.items():
        if value:
            setattr(existing, attr, value)


def validate_image_type(file) -> bool:
    file_type = imghdr.what(file)
    return file_type in ["png", "jpeg", "gif", "bmp", "webp"]


async def check_file_size(file, max_allowed) -> bool:
    await file.seek(0, os.SEEK_END)
    file_size = file.tell() / 1000000
    await file.seek(0)
    return file_size < max_allowed

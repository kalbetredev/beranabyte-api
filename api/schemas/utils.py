import imghdr
from math import ceil
import os
from strawberry.types import Info
from api.database.database import Database
from api.database.models.pagemodel import PageModel
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


def get_page_with_count(max_count, page_size, page_num):
    page_size = page_size if page_size >= 1 else 10
    page_count = ceil(max_count / page_size)
    page_num = 1 if page_num < 1 else page_num
    page_num = page_count if page_num > page_count else page_num
    page = PageModel(number=page_num, size=page_size)
    return (page, page_count)

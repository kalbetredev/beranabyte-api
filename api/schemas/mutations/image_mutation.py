from typing import Union
import strawberry
from strawberry.types import Info
from strawberry.file_uploads import Upload
from api.database.database import Database
from api.schemas.types.responses import ActionResult, ImageUploadResult
from api.schemas.utils import (
    check_file_size,
    is_current_user_admin,
    validate_image_type,
)
from api.utils.constants import messages
from api.utils.errors.apierror import APIError
from bson.objectid import ObjectId


MAX_ALLOWED_IMAGE_SIZE = 16


@strawberry.type
class ImageMutation:
    @strawberry.mutation
    async def upload_image(
        self, info: Info, blog_id: str, image: Upload
    ) -> Union[ImageUploadResult, APIError]:
        try:
            if not await is_current_user_admin(info):
                return APIError(messages.UNAUTHORIZED_ACCESS)

            if not validate_image_type(image.file):
                return ImageUploadResult(
                    is_successfull=False,
                    img_url="",
                    message="The image type is not supported. Only png, jpeg, gif, bmp and webp are allowed",
                )

            if not check_file_size(image.file, MAX_ALLOWED_IMAGE_SIZE):
                return ImageUploadResult(
                    is_successfull=False,
                    img_url="",
                    message="The image size should not exceed 16MB",
                )

            db: Database = info.context.db

            if not ObjectId.is_valid(blog_id):
                return ImageUploadResult(
                    is_successfull=False,
                    img_url="",
                    message=messages.INVALID_ID,
                )
            else:
                blog = await db.get_blog_by_id(blog_id)
                if blog is None:
                    return ImageUploadResult(
                        is_successfull=False,
                        img_url="",
                        message=messages.BLOG_NOT_FOUND,
                    )

                image_id = await db.save_image(blog_id=blog_id, image=image)
                return ImageUploadResult(
                    is_successfull=True,
                    img_url=image_id,
                    message=messages.UPLOAD_SUCCESS,
                )
        except Exception as error:
            info.context.logger.error(__name__, error)
            return APIError()

    @strawberry.mutation
    async def delete_image(
        self, info: Info, image_id: str
    ) -> Union[ActionResult, APIError]:
        try:
            if not await is_current_user_admin(info):
                return APIError(messages.UNAUTHORIZED_ACCESS)

            db: Database = info.context.db

            if not ObjectId.is_valid(image_id):
                return ActionResult(
                    is_successfull=False,
                    message=messages.INVALID_ID,
                )
            else:
                result = await db.delete_image(image_id)
                return ActionResult(
                    is_successfull=result,
                    message="Image deleted successfully"
                    if result
                    else "Failed to delete the image. Please check the image id",
                )
        except Exception as error:
            info.context.logger.error(__name__, error)
            return APIError()

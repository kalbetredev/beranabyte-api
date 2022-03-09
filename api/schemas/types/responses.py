from distutils.log import error
from email import message
import strawberry


@strawberry.type
class ActionResult:
    is_successfull: bool
    message: str


@strawberry.type
class ImageUploadResult:
    is_successfull: bool
    img_url: str
    message: str

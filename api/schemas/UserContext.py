from fastapi import Depends, Request
from fastapi.security.oauth2 import OAuth2PasswordBearer
from strawberry.fastapi import BaseContext
from api.auth.firebaseadmin import get_current_user
from api.utils.logging.defaultlogger import DefaultLogger
from api.utils.logging.logger import Logger

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/signin")


class UserContext(BaseContext):
    logger: Logger = DefaultLogger()

    def __init__(self, access_token: str | None):
        try:
            self.user = (
                get_current_user(access_token) if access_token is not None else None
            )
        except Exception as error:
            self.logger.error(__name__, error)
            self.user = None


async def user_context_dependency(request: Request) -> UserContext:
    if "Authorization" in request.headers:
        access_token = await oauth2_scheme(request)
        return UserContext(access_token)
    else:
        return UserContext(None)


def get_user_context(user_context=Depends(user_context_dependency)):
    return user_context

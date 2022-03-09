from fastapi import Depends, Request
from fastapi.security.oauth2 import OAuth2PasswordBearer
from strawberry.fastapi import BaseContext
from api.auth.firebaseadmin import get_current_user
from api.database.database import Database
from api.database.mongodatabase import MongoDatabase
from api.utils.logging.defaultlogger import DefaultLogger
from api.utils.logging.logger import Logger

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/signin")


class AppContext(BaseContext):
    def __init__(self, access_token: str | None):
        self.logger: Logger = DefaultLogger()
        self.db: Database = MongoDatabase()
        try:
            self.current_user = (
                get_current_user(access_token) if access_token is not None else None
            )
        except Exception as error:
            self.logger.error(__name__, error)
            self.current_user = None


async def app_context_dependency(request: Request) -> AppContext:
    if "Authorization" in request.headers:
        access_token = await oauth2_scheme(request)
        return AppContext(access_token)
    else:
        return AppContext(None)


def get_app_context(app_context=Depends(app_context_dependency)):
    return app_context

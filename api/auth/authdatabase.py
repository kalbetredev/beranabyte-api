from logging import Logger

import motor.motor_asyncio
from api.auth.constants import (
    DEVICE_COLLECTION,
    REFRESH_TOKENS_COLLECTION,
    SESSION_COLLECTION,
    USER_TOKEN_COLLECTION,
)
from api.auth.models.device import Device
from api.auth.models.session import Session
from api.auth.models.usertoken import UserToken
from api.config.settings import settings
from api.database.databaseerror import DatabaseError
from api.utils.logging.defaultlogger import DefaultLogger
from firebase_admin.credentials import RefreshToken


class AuthDatabase:
    def __init__(self, logger=DefaultLogger()):
        self.logger: Logger = logger
        self.client = motor.motor_asyncio.AsyncIOMotorClient(
            settings.mongodb_url,
        )
        self.auth_db = self.client[settings.auth_db_name]
        self.devices_collection = self.auth_db[DEVICE_COLLECTION]
        self.refresh_token_collection = self.auth_db[REFRESH_TOKENS_COLLECTION]
        self.user_tokens_collection = self.auth_db[USER_TOKEN_COLLECTION]
        self.sessions_collection = self.auth_db[SESSION_COLLECTION]

    async def add_device(self, device: Device) -> str:
        try:
            result = await self.devices_collection.insert_one(device.dict())
            return result.inserted_id
        except Exception as error:
            self.logger.error(__name__, error)
            raise DatabaseError("Unable to Save Device to Database")

    async def add_refresh_token(self, token: RefreshToken) -> str:
        try:
            result = await self.refresh_token_collection.insert_one(token.dict())
            return result.inserted_id
        except Exception as error:
            self.logger.error(__name__, error)
            raise DatabaseError("Unable to Save Refresh Token to Database")

    async def add_user_token(self, token: UserToken) -> str:
        try:
            result = await self.user_tokens_collection.insert_one(token.dict())
            return result.inserted_id
        except Exception as error:
            self.logger.error(__name__, error)
            raise DatabaseError("Unable to Save User Token to Database")

    async def add_session(self, session: Session) -> str | None:
        try:
            result = await self.sessions_collection.insert_one(session.dict())
            return result.inserted_id
        except Exception as error:
            self.logger.error(__name__, error)
            raise DatabaseError("Unable to Save Session to Database")

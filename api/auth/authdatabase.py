from logging import Logger

import motor.motor_asyncio
from api.auth.constants import (DEVICE_COLLECTION, SESSION_COLLECTION,
                                TOKEN_COLLECTION)
from api.auth.models.device import Device
from api.auth.models.session import Session
from api.auth.models.token import Token
from api.config.settings import settings
from api.utils.logging.defaultlogger import DefaultLogger


class AuthDatabase:
    def __init__(self, logger=DefaultLogger()):
        self.logger: Logger = logger
        self.client = motor.motor_asyncio.AsyncIOMotorClient(
            settings.mongodb_url)
        self.auth_db = self.client[settings.auth_db_name]
        self.devices_collection = self.auth_db[DEVICE_COLLECTION]
        self.tokens_collection = self.auth_db[TOKEN_COLLECTION]
        self.sessions_collection = self.auth_db[SESSION_COLLECTION]

    async def add_device(self, device: Device) -> str:
        try:
            result = await self.devices_collection.insert_one(device.dict())
            return result.inserted_id
        except Exception as error:
            self.logger.error(__name__, error)

    async def add_token(self, token: Token) -> str:
        try:
            result = await self.tokens_collection.insert_one(token.dict())
            return result.inserted_id
        except Exception as error:
            self.logger.error(__name__, error)

    async def add_session(self, session: Session) -> str:
        try:
            result = await self.sessions_collection.insert_one(session.dict())
            return result.inserted_id
        except Exception as error:
            self.logger.error(__name__, error)

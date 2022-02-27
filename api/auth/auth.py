import api.auth.firebaseadmin as admin
from api.auth.authdatabase import AuthDatabase
from api.auth.errors.autherrors import AuthError
from api.auth.models.device import Device
from api.auth.models.refreshtoken import RefreshToken
from api.auth.models.session import Session
from api.auth.models.token import TokenResponse
from api.auth.models.userauth import UserAuth
from api.auth.models.userauthresponse import UserAuthResponse
from api.auth.models.usertoken import UserToken
from api.database.databaseerror import DatabaseError
from api.utils.constants.messages import (
    AUTHENTICATION_FAILED,
    SIGNIN_FAILED,
    SIGNUP_FAILED,
)
from api.utils.logging.defaultlogger import DefaultLogger
from api.utils.logging.logger import Logger
from user_agents import parse as parse_user_agent


class Auth:
    def __init__(self, logger=DefaultLogger()):
        self.logger: Logger = logger
        self.auth_db = AuthDatabase()

    async def authenticate_user(
        self,
        user: UserAuthResponse,
        user_auth: UserAuth,
    ):
        try:
            user_agent = parse_user_agent(user_auth.user_agent)
            device = Device(user.user_id, user_auth, user_agent)
            device_id = await self.auth_db.add_device(device)

            refresh_token = RefreshToken(
                user_id=user.user_id,
                created_by_ip=user_auth.ip,
            )
            refresh_token_id = await self.auth_db.add_refresh_token(refresh_token)

            user_token = UserToken.from_user_auth(user, refresh_token_id)
            user_token_id = await self.auth_db.add_user_token(user_token)

            session = Session(
                user_id=user.user_id,
                device_id=device_id,
                token_id=user_token_id,
            )
            await self.auth_db.add_session(session)

            return TokenResponse(
                access_token=user.id_token,
                refresh_token=refresh_token.value,
            )
        except DatabaseError as error:
            self.logger.error(__name__, error)
            raise AuthError(AUTHENTICATION_FAILED)

    async def signup(self, user_auth: UserAuth) -> TokenResponse:
        try:
            user: UserAuthResponse = admin.signup(
                user_auth.email,
                user_auth.password,
            )
            return await self.authenticate_user(user, user_auth)

        except AuthError as error:
            raise error
        except Exception as error:
            self.logger.error(__name__, error)
            raise AuthError(SIGNUP_FAILED)

    async def signin(self, user_auth: UserAuth) -> UserAuthResponse:
        try:
            user: UserAuthResponse = admin.signin(
                user_auth.email,
                user_auth.password,
            )
            return await self.authenticate_user(user, user_auth)

        except AuthError as error:
            raise error
        except Exception as error:
            self.logger.error(__name__, error)
            raise AuthError(SIGNIN_FAILED)

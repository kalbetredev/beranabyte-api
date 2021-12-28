import api.auth.firebaseadmin as admin
from api.auth.authdatabase import AuthDatabase
from api.auth.errors.autherrors import AuthError
from api.auth.models.device import Device
from api.auth.models.session import Session
from api.auth.models.token import Token
from api.auth.models.userauth import UserAuth
from api.auth.models.userauthresponse import UserAuthResponse
from api.utils.constants.messages import SIGNIN_FAILED, SIGNUP_FAILED
from api.utils.logging.defaultlogger import DefaultLogger
from api.utils.logging.logger import Logger
from user_agents import parse as parse_user_agent


class Auth:
    def __init__(self, logger=DefaultLogger()):
        self.logger: Logger = logger
        self.auth_db = AuthDatabase()

    async def signup(self, user_auth: UserAuth) -> UserAuthResponse:
        try:
            user: UserAuthResponse = admin.signup(
                user_auth.email,
                user_auth.password,
            )
            user_agent = parse_user_agent(user_auth.user_agent)

            device = Device(user.user_id, user_auth, user_agent)
            device_id = await self.auth_db.add_device(device)

            token = Token(user)
            token_id = await self.auth_db.add_token(token)

            session = Session(
                user_id=user.user_id,
                device_id=str(device_id),
                token_id=str(token_id),
            )

            await self.auth_db.add_session(session)
            return user
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
            user_agent = parse_user_agent(user_auth.user_agent)

            device = Device(user.user_id, user_auth, user_agent)
            device_id = await self.auth_db.add_device(device)

            token = Token(user)
            token_id = await self.auth_db.add_token(token)

            session = Session(
                user_id=user.user_id,
                device_id=str(device_id),
                token_id=str(token_id),
            )

            await self.auth_db.add_session(session)
            return user
        except AuthError as error:
            raise error
        except Exception as error:
            self.logger.error(__name__, error)
            raise AuthError(SIGNIN_FAILED)

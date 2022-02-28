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
from api.utils.constants.messages import (
    SIGNIN_FAILED,
    SIGNUP_FAILED,
    TOKEN_GENERATION_FAILED,
    TOKEN_REFRESH_FAILED,
)
from api.utils.logging.defaultlogger import DefaultLogger
from api.utils.logging.logger import Logger
from user_agents import parse as parse_user_agent
from user_agents.parsers import UserAgent


class Auth:
    def __init__(self, logger=DefaultLogger()):
        self.logger: Logger = logger
        self.auth_db = AuthDatabase()

    async def signup(self, user_auth: UserAuth) -> TokenResponse:
        try:
            response: UserAuthResponse = admin.signup(
                user_auth.email,
                user_auth.password,
            )
            return await self.generate_user_token(
                response=response,
                user_ip=user_auth.ip,
                user_agent=parse_user_agent(user_auth.user_agent),
            )
        except AuthError as error:
            raise error
        except Exception as error:
            self.logger.error(__name__, error)
            raise AuthError(SIGNUP_FAILED)

    async def signin(self, user_auth: UserAuth) -> UserAuthResponse:
        try:
            response: UserAuthResponse = admin.signin(
                user_auth.email,
                user_auth.password,
            )
            return await self.generate_user_token(
                response=response,
                user_ip=user_auth.ip,
                user_agent=parse_user_agent(user_auth.user_agent),
            )
        except AuthError as error:
            raise error
        except Exception as error:
            self.logger.error(__name__, error)
            raise AuthError(SIGNIN_FAILED)

    async def refresh_token(
        self,
        token: str,
        user_agent: str,
        user_ip: str,
    ) -> TokenResponse:
        try:
            refresh_token = await self.auth_db.get_refresh_token(token)
            user_token = await self.auth_db.get_user_token(refresh_token.id)

            if refresh_token.is_revoked:
                await self.revoke_all_user_tokens(refresh_token.user_id, user_ip)
                raise AuthError(TOKEN_REFRESH_FAILED)
            else:
                result = await self.revoke_user_token(
                    refresh_token.id, user_token.id, user_ip
                )

                if result:
                    response = admin.refresh_id_token(user_token.firebase_refresh_token)

                    if response is not None:
                        return await self.generate_user_token(
                            response=response,
                            user_ip=user_ip,
                            user_agent=parse_user_agent(user_agent),
                        )
                    else:
                        raise AuthError(TOKEN_REFRESH_FAILED)
                else:
                    raise AuthError(TOKEN_REFRESH_FAILED)

        except AuthError as error:
            raise error
        except Exception as error:
            self.logger.error(__name__, error)
            raise AuthError(TOKEN_REFRESH_FAILED)

    async def revoke_all_user_tokens(self, user_id, user_ip):
        admin.revoke_refresh_token(user_id)
        await self.auth_db.revoke_all_user_tokens(user_id)
        await self.auth_db.revoke_all_refresh_tokens(user_id, user_ip)

    async def revoke_user_token(self, refresh_token_id, user_token_id, ip) -> bool:
        refresh_token_result = await self.auth_db.revoke_refersh_token(
            refresh_token_id,
            ip,
        )
        user_token_result = await self.auth_db.revoke_user_token(user_token_id)
        return refresh_token_result and user_token_result

    async def generate_user_token(
        self,
        response: UserAuthResponse,
        user_ip,
        user_agent: UserAgent,
    ) -> TokenResponse | None:
        try:
            refresh_token = RefreshToken(
                user_id=response.user_id,
                created_by_ip=user_ip,
            )
            refresh_token_id = await self.auth_db.add_refresh_token(refresh_token)

            user_token = UserToken.from_user_auth(response, refresh_token_id)
            user_token_id = await self.auth_db.add_user_token(user_token)

            device = Device.from_user(response.user_id, user_ip, user_agent)
            device_id = await self.auth_db.add_device(device)

            session = Session(
                user_id=response.user_id,
                device_id=device_id,
                token_id=user_token_id,
            )
            await self.auth_db.add_session(session)

            return TokenResponse(
                access_token=response.id_token,
                refresh_token=refresh_token.value,
            )
        except Exception as error:
            self.logger.error(__name__, error)
            raise AuthError(TOKEN_GENERATION_FAILED)

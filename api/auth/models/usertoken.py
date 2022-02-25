from datetime import datetime
from typing import Optional
from api.auth.models.mongomodel import MongoModel
from api.auth.models.pyobjectid import PyObjectId

from api.auth.models.userauthresponse import UserAuthResponse


class UserToken(MongoModel):
    user_id: str
    api_refresh_token: PyObjectId
    firebase_refresh_token: str
    issued_on: datetime
    is_revoked: bool
    used_on: Optional[datetime] = None

    @staticmethod
    def from_user_auth(
        user_auth: UserAuthResponse,
        api_refresh_token: PyObjectId,
    ):
        return UserToken(
            user_id=user_auth.user_id,
            api_refresh_token=api_refresh_token,
            firebase_refresh_token=user_auth.refresh_token,
            issued_on=datetime.now(),
            is_revoked=False,
        )

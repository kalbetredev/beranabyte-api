from datetime import datetime
from typing import Optional

from api.auth.models.userauthresponse import UserAuthResponse
from pydantic import BaseModel


class UserToken(BaseModel):
    user_id: str
    api_refresh_token: str
    firebase_refresh_token: str
    issued_on: datetime
    is_revoked: bool
    used_on: Optional[datetime] = None

    def __init__(self, user: UserAuthResponse, api_refresh_token: str):
        super().__init__(
            user_id=user.user_id,
            api_refresh_token=api_refresh_token,
            firebase_refresh_token=user.refresh_token,
            issued_on=datetime.now(),
            is_revoked=False,
        )

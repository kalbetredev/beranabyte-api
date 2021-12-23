from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from api.common.pyobjectid import PyObjectId
from api.schemas.types.auth import UserAuthResponse


class Token(BaseModel):
    user_id: str
    refresh_token: str
    issued_on: datetime
    used_on: Optional[datetime] = None
    is_revoked: bool

    def __init__(self, user: UserAuthResponse):
        super().__init__(
            user_id=user.user_id,
            refresh_token=user.refresh_token,
            issued_on=datetime.now(),
            is_revoked=False
        )

    class Config:
        allow_population_by_field_name = True

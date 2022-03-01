from base64 import b64encode
from datetime import datetime
from secrets import token_bytes
from typing import Optional

from pydantic import Field

from api.auth.models.mongomodel import MongoModel


def generate_token():
    return b64encode(token_bytes(64)).decode()


class RefreshToken(MongoModel):
    user_id: str
    created_by_ip: str
    value: Optional[str] = Field(default_factory=generate_token)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    is_revoked: Optional[bool] = False
    revoked_by_ip: Optional[datetime] = None

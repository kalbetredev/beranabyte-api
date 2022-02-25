from base64 import b64encode
from datetime import datetime
from secrets import token_bytes
from typing import Optional

from api.auth.models.mongomodel import MongoModel


class RefreshToken(MongoModel):
    user_id: str
    created_by_ip: str
    value: Optional[str] = b64encode(token_bytes(64)).decode()
    created_at: Optional[datetime] = datetime.utcnow()
    replaced_by: Optional[datetime] = None
    revoked_by_ip: Optional[datetime] = None

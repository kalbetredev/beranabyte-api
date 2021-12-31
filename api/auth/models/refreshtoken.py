from base64 import b64encode
from datetime import datetime
from secrets import token_bytes
from typing import Optional

from pydantic.main import BaseModel


class RefreshToken(BaseModel):
    user_id: str
    created_by_ip: str
    value: Optional[str] = b64encode(token_bytes(64)).decode()
    created_at: Optional[str] = datetime.utcnow()
    replaced_by: Optional[str] = None
    revoked_by_ip: Optional[str] = None

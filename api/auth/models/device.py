from bson.objectid import ObjectId
import geocoder
from pydantic import BaseModel, Field
from datetime import datetime

from user_agents.parsers import UserAgent
from api.auth.models.userauth import UserAuth


class Device(BaseModel):
    user_id: str
    ip: str
    type: str
    browser: str
    os: str
    last_used_on: datetime
    location: str

    def __init__(self, user_id: str, user_auth: UserAuth, user_agent: UserAgent):
        user_location = geocoder.ip(user_auth.ip).city
        super().__init__(
            user_id=user_id,
            ip=user_auth.ip,
            type=user_agent.get_device(),
            browser=user_agent.get_browser(),
            os=user_agent.get_os(),
            last_used_on=datetime.now(),
            location=user_location if user_location is not None else ""
        )

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: lambda x: str(x)}

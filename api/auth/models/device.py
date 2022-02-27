import geocoder
from datetime import datetime

from user_agents.parsers import UserAgent
from api.auth.models.mongomodel import MongoModel


class Device(MongoModel):
    user_id: str
    ip: str
    type: str
    browser: str
    os: str
    last_used_on: datetime
    location: str

    @staticmethod
    def from_user(user_id: str, user_ip: str, user_agent: UserAgent):
        user_location = geocoder.ip(user_ip).city
        return Device(
            user_id=user_id,
            ip=user_ip,
            type=user_agent.get_device(),
            browser=user_agent.get_browser(),
            os=user_agent.get_os(),
            last_used_on=datetime.now(),
            location=user_location if user_location is not None else "",
        )

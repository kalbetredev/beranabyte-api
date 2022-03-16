from datetime import datetime
from pydantic import EmailStr, Field
from api.auth.models.mongomodel import MongoModel


class SubscriberModel(MongoModel):
    email: EmailStr
    subscribed_on: datetime = Field(default_factory=datetime.utcnow, kw_only=True)

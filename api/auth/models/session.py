from api.auth.models.mongomodel import MongoModel
from api.auth.models.pyobjectid import PyObjectId


class Session(MongoModel):
    user_id: str
    device_id: PyObjectId
    token_id: PyObjectId

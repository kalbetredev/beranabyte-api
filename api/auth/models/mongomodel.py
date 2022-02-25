from pydantic import BaseModel, Field

from api.auth.models.pyobjectid import PyObjectId


class MongoModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            PyObjectId: str,
        }

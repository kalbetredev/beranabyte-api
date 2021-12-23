from pydantic import BaseModel


class Session(BaseModel):
    user_id: str
    device_id: str
    token_id: str

    class Config:
        allow_population_by_field_name = True

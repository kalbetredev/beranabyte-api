from pydantic import BaseModel


class Sort(BaseModel):
    key: str
    dir: int

from pydantic import BaseModel


class SortModel(BaseModel):
    key: str
    dir: int

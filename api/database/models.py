from pydantic import BaseModel


class Sort(BaseModel):
    key: str
    dir: int


class Page(BaseModel):
    number: int
    size: int

from pydantic import BaseModel


class PageModel(BaseModel):
    number: int
    size: int

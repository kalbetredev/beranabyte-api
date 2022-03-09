from pydantic import BaseModel, Field
from datetime import datetime
from api.auth.models.mongomodel import MongoModel


class BlogBase(BaseModel):
    title: str
    topic: str
    summary: str = Field(default="", kw_only=True)
    image_url: str = Field(default="", kw_only=True)
    content: str = Field(default="", kw_only=True)
    is_featured: bool = Field(default=False, kw_only=True)
    is_published: bool = Field(default=False, kw_only=True)
    modified_on: datetime = Field(default_factory=datetime.utcnow, kw_only=True)
    view_count: int = Field(default=0, kw_only=True)
    published_on: datetime = Field(default_factory=datetime.utcnow, kw_only=True)


class BlogModel(MongoModel, BlogBase):
    pass

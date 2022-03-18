from pydantic import BaseModel, Field

from api.auth.models.mongomodel import MongoModel


class ProjectBase(BaseModel):
    title: str
    thumbnail_url: str = Field(default="", kw_only=True)
    git_url: str = Field(default="", kw_only=True)
    tech_stacks: str = Field(default="", kw_only=True)


class ProjectModel(MongoModel, ProjectBase):
    pass

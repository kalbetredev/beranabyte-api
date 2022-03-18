import strawberry
from typing import List, Optional

from api.database.models.projectmodel import ProjectBase


@strawberry.experimental.pydantic.type(model=ProjectBase, all_fields=True)
class Project:
    id: str


@strawberry.input
class NewProject:
    title: str
    git_url: str = ""
    thumbnail_url: Optional[str] = ""
    tech_stacks: Optional[str] = ""


@strawberry.input
class UpdatedProject:
    title: Optional[str] = None
    git_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    tech_stacks: Optional[str] = None


@strawberry.type
class ProjectsResult:
    projects: List[Project]
    page_num: int
    page_count: int

import strawberry
from typing import List, Union
from api.schemas.resolvers.projectresolvers import (
    get_projects,
    search_projects,
    get_project,
)
from api.schemas.types.project import Project, ProjectsResult
from api.utils.errors.apierror import APIError
from api.utils.errors.projecterrors import ProjectNotFound


@strawberry.type
class ProjectQuery:
    projects: Union[ProjectsResult, APIError] = strawberry.field(resolver=get_projects)
    search_projects: Union[ProjectsResult, APIError] = strawberry.field(
        resolver=search_projects
    )
    project: Union[Project, ProjectNotFound, APIError] = strawberry.field(
        resolver=get_project
    )

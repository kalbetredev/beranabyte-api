from typing import Union, Optional
from strawberry.types import Info
from api.database.database import Database
from api.database.models.sortmodel import SortModel
from api.schemas import utils
from api.schemas.types.project import Project, ProjectsResult

from api.utils.errors.apierror import APIError
from api.utils.errors.projecterrors import ProjectNotFound


async def get_projects(
    info: Info,
    sort_by: Optional[str] = None,
    sort_dir: Optional[int] = 1,
    page_num: Optional[int] = 1,
    page_size: Optional[int] = 10,
) -> Union[ProjectsResult, APIError]:
    try:
        db: Database = info.context.db

        sort = None
        if sort_by is not None:
            sort = SortModel(sort_by, sort_dir)

        (page, page_count) = utils.get_page_with_count(
            await db.get_projects_count(),
            page_size,
            page_num,
        )

        project_models = await db.get_projects(sort=sort, page=page)
        projects = [Project(**project_model.dict()) for project_model in project_models]
        return ProjectsResult(projects, page_num=page_num, page_count=page_count)
    except Exception as error:
        info.context.logger.error(__name__, error)
        return APIError()


async def search_projects(
    info: Info,
    text: str,
    page_num: Optional[int] = 1,
    page_size: Optional[int] = 10,
):
    try:
        db: Database = info.context.db

        search_limit = 50
        (page, page_count) = utils.get_page_with_count(
            search_limit,
            page_size,
            page_num,
        )

        project_models = await db.search_projects(
            text=text,
            page=page,
            max_limit=search_limit,
        )
        projects = [Project(**project_model.dict()) for project_model in project_models]
        return ProjectsResult(projects, page_num=page.number, page_count=page_count)
    except Exception as error:
        info.context.logger.error(__name__, error)
        return APIError()


async def get_project(
    project_id: str, info: Info
) -> Union[Project, ProjectNotFound, APIError]:
    try:
        db: Database = info.context.db
        project_model = await db.get_project_by_id(project_id)
        return (
            Project(**project_model.dict())
            if project_model is not None
            else ProjectNotFound()
        )
    except Exception as error:
        info.context.logger.error(__name__, error)
        return APIError()

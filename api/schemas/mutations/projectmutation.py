from typing import List, Union
import strawberry
from strawberry.types import Info
from api.database.database import Database
from api.database.models.projectmodel import ProjectModel

from api.schemas.types.project import NewProject, Project, UpdatedProject
from api.schemas.types.responses import ActionResult
from api.schemas import utils
from api.schemas.validators import projectvalidators
from api.utils.constants import messages
from api.utils.errors.apierror import APIError
from api.utils.errors.projecterrors import ProjectNotFound
from api.utils.errors.validationerror import InputError, InputValidationError
from bson.objectid import ObjectId


@strawberry.type
class ProjectMutation:
    @strawberry.mutation
    async def add_project(
        self, project: NewProject, info: Info
    ) -> Union[Project, InputValidationError, APIError]:
        try:
            db: Database = info.context.db

            if not await utils.is_current_user_admin(info):
                return APIError(messages.UNAUTHORIZED_ACCESS)

            validation_errors: List[
                InputError
            ] = projectvalidators.validate_new_project_inputs(project)

            if len(validation_errors) > 0:
                return InputValidationError(validation_errors)

            if await db.get_project_by_title(project.title) is not None:
                return InputValidationError(
                    [InputError(input="title", message=messages.PROJECT_TITLE_TAKEN)]
                )

            project = ProjectModel(**project.__dict__)
            saved_project = await db.add_project(project)
            return (
                Project(**saved_project.dict())
                if saved_project is not None
                else APIError()
            )
        except Exception as error:
            info.context.logger.error(__name__, error)
            return APIError()


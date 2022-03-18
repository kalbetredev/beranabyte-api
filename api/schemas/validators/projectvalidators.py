from typing import List
from api.schemas.types.project import NewProject, UpdatedProject
from api.utils.constants import messages
from api.utils.errors.validationerror import InputError


def validate_new_project_inputs(new_project: NewProject):
    validation_errors: List[InputError] = []
    if new_project.title is None or new_project.title == "":
        validation_errors.append(
            InputError(input="title", message=messages.PROJECT_TITLE_EMPTY)
        )

    if new_project.git_url is None or new_project.git_url == "":
        validation_errors.append(
            InputError(input="topic", message=messages.PROJECT_GITURL_EMPTY)
        )

    return validation_errors


def validate_project_update_inputs(updated_project: UpdatedProject):
    validation_errors: List[InputError] = []
    if updated_project.title is not None and updated_project.title == "":
        validation_errors.append(
            InputError(input="title", message=messages.PROJECT_TITLE_EMPTY)
        )

    if updated_project.git_url is not None and updated_project.git_url == "":
        validation_errors.append(
            InputError(input="topic", message=messages.PROJECT_GITURL_EMPTY)
        )

    return validation_errors

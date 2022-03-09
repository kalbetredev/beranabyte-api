from typing import List
from api.schemas.types.blog import NewBlog, UpdatedBlog
from api.utils.constants import messages
from api.utils.errors.validationerror import InputError


def validate_new_blog_inputs(
    new_blog: NewBlog,
) -> List[InputError]:
    validation_errors: List[InputError] = []
    if new_blog.title is None or new_blog.title == "":
        validation_errors.append(
            InputError(input="title", message=messages.BLOG_TITLE_EMPTY)
        )

    if new_blog.topic is None or new_blog.topic == "":
        validation_errors.append(
            InputError(input="topic", message=messages.BLOG_TOPIC_EMPTY)
        )

    return validation_errors


def validate_blog_update_inputs(
    updated_blog: UpdatedBlog,
) -> List[InputError]:
    validation_errors: List[InputError] = []
    if updated_blog.title is not None and updated_blog.title == "":
        validation_errors.append(
            InputError(input="title", message=messages.BLOG_TITLE_EMPTY)
        )

    if updated_blog.topic is not None and updated_blog.topic == "":
        validation_errors.append(
            InputError(input="topic", message=messages.BLOG_TOPIC_EMPTY)
        )

    return validation_errors

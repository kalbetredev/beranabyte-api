import strawberry
from typing import List
from pydantic import ValidationError


@strawberry.type
class InputError:
    input: str
    message: str


@strawberry.type
class InputValidationError(Exception):
    def __init__(self, errors: List[InputError]) -> None:
        self.errors = errors

    @strawberry.field
    def errors(self) -> List[InputError]:
        return self.errors

    @classmethod
    def fromPydanticError(cls, error: ValidationError):
        input_errors: List[InputError] = []
        for error_dict in error.errors():
            input_errors.append(
                InputError(error_dict["loc"][0], error_dict["msg"]),
            )

        return InputValidationError(input_errors)

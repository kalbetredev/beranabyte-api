import strawberry
from typing import List
from pydantic import ValidationError


@strawberry.type
class InputError:
    input: str
    message: str


@strawberry.type
class InputValidationError(BaseException):
    def __init__(self, errors: List[InputError]) -> None:
        self.errors = errors

    @strawberry.field
    def errors(self) -> List[InputError]:
        return self.errors

    @classmethod
    def fromPydanticError(cls, error: ValidationError):
        inputErrors: List[InputError] = []
        for errorDict in error.errors():
            inputErrors.append(InputError(
                errorDict['loc'][0], errorDict['msg']))

        return InputValidationError(inputErrors)

import strawberry
from api.schemas.types.user import User, UserAuth
from api.utils.errors.apierror import APIError
from api.utils.errors.usererrors import EmailAlreadyRegistered
from api.utils.errors.validationerror import InputValidationError
from api import app

RegisterUserResult = strawberry.union(
    "RegisterUserResult",
    [User, EmailAlreadyRegistered, InputValidationError, APIError]
)


@strawberry.type
class UserMutation:
    @strawberry.mutation
    def register_new_user(self, user: UserAuth) -> RegisterUserResult:
        try:
            return app.database.register_user(user)
        except (EmailAlreadyRegistered, InputValidationError) as error:
            return error
        except Exception as error:
            app.logger.error(__name__, error)
            return APIError()

from typing import Union
from pydantic import EmailError, validate_email
import strawberry
from strawberry.types import Info
from api.database.database import Database
from api.schemas.types.responses import ActionResult
from api.utils.errors.apierror import APIError
from api.utils.errors.validationerror import InputError, InputValidationError


@strawberry.type
class MailMutation:
    @strawberry.mutation
    async def subscribe(
        self, info: Info, email: str
    ) -> Union[ActionResult, InputValidationError, APIError]:
        try:
            validate_email(email)
            db: Database = info.context.db
            result = await db.add_subscriber(email)
            return ActionResult(
                is_successfull=result,
                message="Email subscribed to the mailing list successfully"
                if result
                else "Failed to subscribe the email to the mailing list. Please try again",
            )

        except EmailError as error:
            return InputValidationError(
                [InputError(input="email", message="Invalid Email Address")]
            )
        except Exception as error:
            info.context.logger.error(__name__, error)
            return APIError()

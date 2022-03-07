import strawberry


@strawberry.type
class ActionResult:
    is_successfull: bool
    message: str

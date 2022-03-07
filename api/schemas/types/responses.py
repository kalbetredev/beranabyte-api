import strawberry


@strawberry.type
class Success:
    message: str


@strawberry.type
class ActionResult:
    is_successfull: bool
    message: str

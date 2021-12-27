from enum import Enum
from api.auth import constants


class FirebaseError(Enum):
    EMAIL_NOT_FOUND = constants.EMAIL_NOT_FOUND
    INVALID_PASSWORD = constants.INVALID_PASSWORD
    USER_DISABLED = constants.USER_DISABLED
    EMAIL_EXISTS = constants.EMAIL_EXISTS
    OTHER = 'OTHER'

    @staticmethod
    def from_str(error: str):
        match error:
            case constants.EMAIL_NOT_FOUND:
                return FirebaseError.EMAIL_NOT_FOUND
            case constants.INVALID_PASSWORD:
                return FirebaseError.INVALID_PASSWORD
            case constants.USER_DISABLED:
                return FirebaseError.USER_DISABLED
            case constants.EMAIL_EXISTS:
                return FirebaseError.EMAIL_EXISTS
            case _:
                return FirebaseError.OTHER

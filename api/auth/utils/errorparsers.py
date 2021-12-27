from pydantic.error_wrappers import ValidationError
from requests.models import Response

from api.auth.errors.firebaseerror import FirebaseError


def parse_validation_error(error: ValidationError):
    validation_errors = [{'field': ','.join(e['loc']), 'msg': e['msg']}
                         for e in error.errors()]
    return {
        'type': 'validation',
        'details': validation_errors
    }


def parse_firebase_error(response: Response) -> FirebaseError:
    message = response.json()['error']['message']
    return FirebaseError.from_str(message)


def parse_token_error_message(response: Response) -> FirebaseError:
    return response.json()['error']['message']

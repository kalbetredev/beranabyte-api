import json

import firebase_admin
import requests
from api.auth.errors.autherrors import AuthError
from api.auth.errors.firebaseerror import FirebaseError
from api.auth.models.userauthresponse import UserAuthResponse
from api.auth.utils.errorparsers import parse_firebase_error, parse_token_error_message
from api.config.settings import settings
from api.utils.constants.messages import (ACCOUNT_DISABLED, EMAIL_EXISTS,
                                          INVALID_LOGIN_INPUTS, SIGNIN_FAILED,
                                          SIGNUP_FAILED)
from api.utils.logging.defaultlogger import DefaultLogger
from api.utils.logging.logger import Logger
from firebase_admin import auth, credentials
from firebase_admin._user_mgt import UserRecord
from requests.models import Response

cred = credentials.Certificate(settings.get_google_application_credentials())
default_app = firebase_admin.initialize_app(cred)
headers = {'Content-Type': 'application/json'}
logger: Logger = DefaultLogger()


def get_user(uid: str) -> UserRecord:
    user: UserRecord = auth.get_user(uid)
    return user


def signup(email, password) -> UserAuthResponse:
    try:
        endpoint = f'{settings.auth_api_endpoint}signUp?key={settings.firebase_web_api_key}'
        data = {
            'email': email,
            'password': password,
            'returnSecureToken': True
        }

        response: Response = requests.post(
            url=endpoint, data=json.dumps(data), headers=headers)

        if response.status_code != 200:
            firebase_error = parse_firebase_error(response)
            if firebase_error == FirebaseError.EMAIL_EXISTS:
                raise AuthError(EMAIL_EXISTS)
            else:
                raise AuthError(SIGNUP_FAILED)

        return UserAuthResponse.from_response(response.json())
    except AuthError as error:
        raise error
    except Exception as error:
        logger.error(__name__, error)


def signin(email, password) -> UserAuthResponse:
    try:
        endpoint = f'{settings.auth_api_endpoint}signInWithPassword?key={settings.firebase_web_api_key}'
        data = {
            'email': email,
            'password': password,
            'returnSecureToken': True
        }

        response: Response = requests.post(
            url=endpoint, data=json.dumps(data), headers=headers)

        if response.status_code != 200:
            firebase_error = parse_firebase_error(response)
            if firebase_error in (FirebaseError.EMAIL_NOT_FOUND, FirebaseError.INVALID_PASSWORD):
                raise AuthError(INVALID_LOGIN_INPUTS)
            elif firebase_error == FirebaseError.USER_DISABLED:
                raise AuthError(ACCOUNT_DISABLED)
            else:
                raise AuthError(SIGNIN_FAILED)

        return UserAuthResponse.from_response(response.json())
    except AuthError as error:
        raise error
    except Exception as error:
        logger.error(__name__, error)


def refresh_id_token(refresh_token: str):
    try:
        endpoint = f'{settings.refresh_token_url}?key={settings.firebase_web_api_key}'
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }

        response: Response = requests.post(
            url=endpoint, data=json.dumps(data), headers=headers)

        if response.status_code != 200:
            message = parse_token_error_message(response)
            raise AuthError(message)

        return UserAuthResponse.from_response(response.json())
    except Exception as error:
        logger.error(__name__, error)

import json

import firebase_admin
import requests
from requests.models import Response
from api.auth.models.userauthresponse import UserAuthResponse
from api.config.settings import settings
from firebase_admin import auth, credentials
from firebase_admin._user_mgt import UserRecord
from api.utils.logging.defaultlogger import DefaultLogger
from api.utils.logging.logger import Logger

cred = credentials.Certificate(settings.get_google_application_credentials())
default_app = firebase_admin.initialize_app(cred)
headers = {'Content-Type': 'application/json'}
logger: Logger = DefaultLogger()


class FirbaseException(Exception):
    def __init__(self, response: Response):
        super().__init__(response.json()['error']['message'])


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
            raise FirbaseException(response)

        return UserAuthResponse.from_response(response.json())
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
            raise FirbaseException(response)

        return UserAuthResponse.from_response(response.json())
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
            raise FirbaseException(response)

        return UserAuthResponse.from_response(response.json())
    except Exception as error:
        logger.error(__name__, error)

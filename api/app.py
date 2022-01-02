from typing import Optional
from http import HTTPStatus
import strawberry
import uvicorn
from fastapi import Depends, FastAPI, Header, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security.oauth2 import OAuth2PasswordBearer
from pydantic.error_wrappers import ValidationError
from strawberry.fastapi import GraphQLRouter
from tests.testdatabase import TestDatabase

from api.auth.auth import Auth
from api.auth.errors.autherrors import AuthError
from api.auth.models.userauth import UserAuth
from api.auth.utils.errorparsers import parse_validation_error
from api.config.settings import settings
from api.database.database import Database
from api.schemas.mutations.apimutation import Mutation
from api.schemas.queries.apiquery import Query
from api.utils.constants.messages import (
    INVALID_LOGIN_INPUTS,
    SIGNIN_FAILED,
    SIGNUP_FAILED,
)
from api.utils.logging.defaultlogger import DefaultLogger
from api.utils.logging.logger import Logger

schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQLRouter(schema, graphiql=settings.graphiql)

database: Database = TestDatabase()
logger: Logger = DefaultLogger()
auth = Auth()

app = FastAPI()
app.include_router(graphql_app, prefix="/api")

origins = [settings.client_url]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/signup")
async def signup(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_agent: Optional[str] = Header(None),
):
    try:
        user_auth = UserAuth(
            email=form_data.username,
            password=form_data.password,
            user_agent=user_agent,
            ip=request.client.host,
        )
        response = await auth.signup(user_auth)
        return response.get_json()
    except ValidationError as error:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail={"error": parse_validation_error(error)},
        )
    except AuthError as error:
        logger.error(__name__, error.message)
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=error.message,
        )
    except Exception as error:
        logger.error(__name__, error)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=SIGNUP_FAILED
        )


@app.post("/signin")
async def signin(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_agent: Optional[str] = Header(None),
):
    try:
        user_auth = UserAuth(
            email=form_data.username,
            password=form_data.password,
            user_agent=user_agent,
            ip=request.client.host,
        )
        response = await auth.signin(user_auth)
        return response.get_json()
    except ValidationError as error:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail=INVALID_LOGIN_INPUTS
        )
    except AuthError as error:
        logger.error(__name__, error.message)
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=error.message,
        )
    except Exception as error:
        logger.error(__name__, error)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=SIGNIN_FAILED
        )


@app.get("/blog")
def get_blog(token: str = Depends(oauth2_scheme)):
    return {"token": token}


def start_app():
    uvicorn.run("api.app:app", host="0.0.0.0", port=8000, reload=True)

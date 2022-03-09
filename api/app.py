from typing import Optional
from http import HTTPStatus
import strawberry
import uvicorn
from fastapi import Depends, FastAPI, Header, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from pydantic.error_wrappers import ValidationError
from strawberry.fastapi import GraphQLRouter
from api.appcontext import AppContext, app_context_dependency, get_app_context
from api.auth.auth import Auth
from api.auth.errors.autherrors import AuthError
from api.auth.models.userauth import UserAuth
from api.auth.utils.errorparsers import parse_validation_error
from api.config.settings import settings
from api.database.database import Database
from api.database.mongodatabase import MongoDatabase
from api.schemas.mutations.apimutation import Mutation
from api.schemas.queries.apiquery import Query
from api.utils.constants.messages import (
    INVALID_LOGIN_INPUTS,
    SIGNIN_FAILED,
    SIGNUP_FAILED,
    TOKEN_REFRESH_FAILED,
)
from api.utils.logging.defaultlogger import DefaultLogger
from api.utils.logging.logger import Logger
from fastapi.responses import StreamingResponse

schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQLRouter(
    schema,
    graphiql=settings.graphiql,
    context_getter=get_app_context,
)

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


@app.post("/auth/signup")
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
        return await auth.signup(user_auth)
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


@app.post("/auth/signin")
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
        return await auth.signin(user_auth)
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


@app.post("/auth/refresh")
async def refresh_token(
    request: Request,
    refresh_token: str,
    user_agent: Optional[str] = Header(None),
):
    try:
        return await auth.refresh_token(
            refresh_token,
            user_agent,
            request.client.host,
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
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=TOKEN_REFRESH_FAILED
        )


@app.get("/images/{image_name}")
async def get_image(image_name: str, request: Request):
    try:
        db: Database = MongoDatabase()
        app_context: AppContext = await app_context_dependency(request)
        user_uid = app_context.current_user.uid if app_context.current_user else None
        (file, content_type) = await db.read_image(
            image_id=image_name, user_id=user_uid
        )
        if file is None:
            raise AuthError(
                "No image found with the specified name or you are not authorized to access the image"
            )
        return StreamingResponse(file, media_type=content_type)
    except AuthError as error:
        logger.error(__name__, error.message)
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=error.message,
        )
    except Exception as error:
        logger.error(__name__, error)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR)


def start_app():
    uvicorn.run("api.app:app", host="0.0.0.0", port=8000, reload=True)

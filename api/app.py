from typing import Optional

import strawberry
import uvicorn
from fastapi import Depends, FastAPI, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security.oauth2 import OAuth2PasswordBearer
from strawberry.fastapi import GraphQLRouter
from tests.testdatabase import TestDatabase

from api.auth.auth import Auth
from api.auth.models.userauth import UserAuth
from api.config.settings import settings
from api.database.database import Database
from api.schemas.mutations.apimutation import Mutation
from api.schemas.queries.apiquery import Query
from api.utils.logging.defaultlogger import DefaultLogger
from api.utils.logging.logger import Logger

schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQLRouter(schema, graphiql=settings.graphiql)

database: Database = TestDatabase()
logger: Logger = DefaultLogger()
auth = Auth()

app = FastAPI()
app.include_router(graphql_app, prefix='/api')

origins = [
    settings.client_url
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post('/signup')
async def signup(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), user_agent: Optional[str] = Header(None)):
    try:
        user_auth = UserAuth(
            email=form_data.username,
            password=form_data.password,
            user_agent=user_agent,
            ip=request.client.host
        )
        response = await auth.signup(user_auth)
        return response.get_json()
    except Exception as error:
        logger.error(__name__, error)


@app.post('/signin')
def signin(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), user_agent: Optional[str] = Header(None)):
    try:
        user_auth = UserAuth(
            email=form_data.username,
            password=form_data.password,
            user_agent=user_agent,
            ip=request.client.host
        )
        response = auth.signin(user_auth)
        return response.get_json()
    except Exception as error:
        logger.error(__name__, error)


def start_app():
    uvicorn.run("api.app:app", host="0.0.0.0", port=8000, reload=True)

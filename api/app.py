import uvicorn
import strawberry
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from api.config.settings import settings
from api.database.database import Database
from api.schemas.queries.apiquery import Query
from api.schemas.mutations.apimutation import Mutation
from api.utils.logging.logger import Logger
from api.utils.logging.defaultlogger import DefaultLogger

schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQLRouter(schema, graphiql=settings.graphiql)

database: Database = None
logger: Logger = DefaultLogger()

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


def start_app():
    uvicorn.run("api.app:app", host="0.0.0.0", port=8000, reload=True)

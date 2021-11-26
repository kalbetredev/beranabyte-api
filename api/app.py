import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.config.settings import settings


app = FastAPI()


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

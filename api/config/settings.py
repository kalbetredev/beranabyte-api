from pydantic import BaseSettings


class Settings(BaseSettings):
    client_url: str
    graphiql: bool

    class Config:
        env_file = '.env'


settings = Settings()

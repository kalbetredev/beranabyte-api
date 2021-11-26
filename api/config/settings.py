from pydantic import BaseSettings


class Settings(BaseSettings):
    client_url: str

    class Config:
        env_file = '.env'


settings = Settings()

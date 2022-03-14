from pydantic import BaseSettings
import base64
import json


class Settings(BaseSettings):
    client_url: str
    graphiql: bool
    google_application_credentials: bytes
    refresh_token_url: str
    auth_api_endpoint: str
    firebase_web_api_key: str
    mongodb_url: str
    auth_db_name: str
    main_db_name: str
    jwt_secrete: str
    jwt_algorithm: str

    def get_google_application_credentials(self):
        decoded = base64.b64decode(self.google_application_credentials)
        return json.loads(decoded.decode("ascii"))

    class Config:
        env_file = ".env"


settings = Settings()

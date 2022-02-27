from pydantic import BaseModel


class UserAuthResponse(BaseModel):
    user_id: str
    id_token: str
    refresh_token: str

    @classmethod
    def from_response(cls, response):
        response_data = response.json()
        if "localId" in response_data:
            return UserAuthResponse(
                user_id=response_data["localId"],
                id_token=response_data["idToken"],
                refresh_token=response_data["refreshToken"],
            )
        else:
            return UserAuthResponse(
                user_id=response_data["user_id"],
                id_token=response_data["id_token"],
                refresh_token=response_data["refresh_token"],
            )

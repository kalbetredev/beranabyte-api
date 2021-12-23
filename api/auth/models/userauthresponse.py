from pydantic import BaseModel


class UserAuthResponse(BaseModel):
    user_id: str
    id_token: str
    refresh_token: str

    @classmethod
    def from_response(cls, response):
        return UserAuthResponse(
            user_id=response['localId'],
            id_token=response['idToken'],
            refresh_token=response['refreshToken']
        )

    def get_json(self):
        return {
            "userId": self.user_id,
            "idToken": self.id_token,
            "refreshToken": self.refresh_token
        }

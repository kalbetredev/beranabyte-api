from pydantic import BaseModel, EmailStr, constr


# TODO: Repeat Password for SignUp
class UserAuth(BaseModel):
    email: EmailStr
    password: constr(min_length=6)
    user_agent: str
    ip: str

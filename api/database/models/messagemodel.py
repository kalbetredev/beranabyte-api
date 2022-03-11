from pydantic import BaseModel, EmailStr


class MessageModel(BaseModel):
    email: EmailStr
    message: str

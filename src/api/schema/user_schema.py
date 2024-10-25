from pydantic import BaseModel, EmailStr


class UserRequestBody(BaseModel):
    name: str
    email: EmailStr

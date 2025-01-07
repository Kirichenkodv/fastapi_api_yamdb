from typing import Optional
from pydantic import BaseModel, EmailStr

class ThunedModel(BaseModel):
    class Config:
        from_attributes=True


class UserCreateResponse(ThunedModel):
    email: EmailStr
    username: str

class UserCreate(BaseModel):
    email: EmailStr
    username: str






from pydantic import BaseModel, EmailStr


class ThunedModel(BaseModel):
    class Config:
        from_attributes = True


class UserCreateResponse(ThunedModel):
    email: EmailStr
    username: str


class UserCreate(BaseModel):
    email: EmailStr
    username: str


class TokenCreate(BaseModel):
    username: str
    confirmation_code: str


class TokenResponse(BaseModel):
    token: str

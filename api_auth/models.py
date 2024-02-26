from pydantic import BaseModel, EmailStr, UUID4, field_validator


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    token_type: str
    token: UUID4

    @field_validator('token')
    def uuid_to_hex(cls, value):
        return value.hex


class UserToken(BaseModel):
    sub: int
    token: Token={}

class AuthToken(BaseModel):
    token: str
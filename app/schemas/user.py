import pydantic
from typing import Optional


class UserCreate(pydantic.BaseModel):
    email: str
    username: str
    password: str
    repeated_password: str


class UserLogin(pydantic.BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    password: str


class UserToken(pydantic.BaseModel):
    token: str

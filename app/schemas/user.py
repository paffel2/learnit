import pydantic


class UserCreate(pydantic.BaseModel):
    email: str
    username: str
    password: str
    repeated_password: str

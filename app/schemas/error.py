import pydantic


class ErrorResponse(pydantic.BaseModel):
    detail: str

import pydantic
from typing import Optional


class SubjectSchema(pydantic.BaseModel):
    name: str
    is_deleted: bool
    id: int
    order: int


class SubjectCreate(pydantic.BaseModel):
    name: str


class SubjectUpdate(pydantic.BaseModel):
    name: str
    order: int


class SubjectDetail(SubjectUpdate):
    id: int


class SubjectPartialUpdate(pydantic.BaseModel):
    name: Optional[str] = None
    order: Optional[int] = None

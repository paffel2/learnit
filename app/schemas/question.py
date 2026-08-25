import pydantic
from typing import Optional


class QuestionCreateSchema(pydantic.BaseModel):
    name: str
    is_deleted: bool
    order: int
    text: str
    content: str  # TODO


class QuestionSchema(pydantic.BaseModel):
    name: str
    is_deleted: bool
    order: int
    subject_id: int
    theme_id: int
    text: str
    content: str  # TODO
    id: int


class QuestionPartialUpdateSchema(pydantic.BaseModel):
    text: Optional[str] = None
    name: Optional[str] = None
    order: Optional[int] = None
    content: Optional[str] = None
    theme_id: Optional[int] = None
    subject_id: Optional[int] = None


class QuestionListSchema(pydantic.BaseModel):
    id: int
    name: str

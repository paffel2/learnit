import pydantic


class ThemeSchema(pydantic.BaseModel):
    id: int
    name: str
    is_deleted: bool
    subject_id: int
    order: int


class ThemeCreateSchema(pydantic.BaseModel):
    name: str

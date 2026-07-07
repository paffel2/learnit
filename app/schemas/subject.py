import pydantic


class SubjectSchema(pydantic.BaseModel):
    name: str
    is_deleted: bool
    id: int
    order: int

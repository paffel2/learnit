import pydantic


class Theme(pydantic.BaseModel):
    name: str
    is_deleted: bool
    subject_id: int
    order: int

from sqladmin import ModelView
from app.models.subject import Subject


class SubjectAdmin(ModelView, model=Subject):
    column_list = ["id", "name"]
    form_excluded_columns = [Subject.updated_at, Subject.created_at]

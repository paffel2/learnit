from sqladmin import ModelView
from app.models.question import Question


class QuestionAdmin(ModelView, model=Question):
    column_list = ["id", "name"]
    form_excluded_columns = [Question.updated_at, Question.created_at]

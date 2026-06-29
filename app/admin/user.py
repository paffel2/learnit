from sqladmin import ModelView
from app.models.user import User


class UserAdmin(ModelView, model=User):
    column_list = ["id", "email", "username"]
    form_excluded_columns = [User.updated_at, User.created_at, User.subjects]

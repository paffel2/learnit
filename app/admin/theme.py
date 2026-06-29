from sqladmin import ModelView
from app.models.theme import Theme


class ThemeAdmin(ModelView, model=Theme):
    column_list = ["id", "name"]
    form_excluded_columns = [Theme.updated_at, Theme.created_at]

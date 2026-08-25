from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse
from app.utils.users import hash_password, get_user_by_username_and_password
from app.config.database import get_db_context


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool | RedirectResponse:
        form = await request.form()
        username, password = form["username"], form["password"]

        hashed_password = hash_password(password)
        with get_db_context() as db:

            user = get_user_by_username_and_password(username, hashed_password, db)
            if user and user.is_superuser:
                request.session.update({"token": "..."})
            return True

    async def logout(self, request: Request) -> bool | RedirectResponse:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        return True

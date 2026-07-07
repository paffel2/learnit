from fastapi import Depends, APIRouter, Response, Cookie
from app.schemas.user import UserCreate, UserLogin
from app.config.database import get_db
from sqlalchemy.orm import Session
from app.utils.users import create_user, auth, refresh_access_token

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/registration")
async def registration(
    user_data: UserCreate, response: Response, db: Session = Depends(get_db)
):
    response_code, response_data = create_user(user_data, session=db)
    response.status_code = response_code
    return response_data


@router.post("/login")
async def login(
    user_data: UserLogin, response: Response, db: Session = Depends(get_db)
):
    response_code, response_data, refresh_token = auth(user_data, session=db)
    response.status_code = response_code
    response.set_cookie(
        key="refresh_token", value=refresh_token, httponly=True, max_age=60 * 60 * 24
    )
    return response_data


@router.get("/refresh")
async def refresh(
    response: Response,
    refresh_token=Cookie(None),
):
    response_code, response_data = refresh_access_token(refresh_token)
    response.status_code = response_code
    return response_data

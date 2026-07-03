from typing import List
from fastapi import FastAPI, HTTPException, Depends, APIRouter, Response
from app.queries.themes import get_themes_by_subject
from app.schemas.theme import Theme as ThemeSchema
from app.schemas.user import UserCreate, UserLogin
from app.config.database import get_db
from sqlalchemy.orm import Session
from app.utils.users import create_user, auth

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
    response_code, response_data = auth(user_data, session=db)
    response.status_code = response_code
    return response_data

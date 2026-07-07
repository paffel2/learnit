from typing import List
from fastapi import FastAPI, HTTPException, Depends, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.queries.subjects import get_subjects
from app.schemas.subject import SubjectSchema
from app.config.database import get_db
from sqlalchemy.orm import Session
from app.utils.users import get_current_user

router = APIRouter(
    prefix="/subjects",
    tags=["subjects"],
)

PAGE_SIZE = 10


@router.get("/", response_model=List[SubjectSchema])
async def list_subjects(
    page: int = 1,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    return get_subjects(session=db, user_id=user_id, page=page, page_size=PAGE_SIZE)

from typing import List
from fastapi import FastAPI, HTTPException, Depends, APIRouter
from app.queries.themes import get_themes_by_subject
from app.schemas.theme import Theme as ThemeSchema
from app.config.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/subjects",
    tags=["subjects"],
)


@router.get("/{subject_id}/themes", response_model=List[ThemeSchema])
async def get_themes(subject_id: int, db: Session = Depends(get_db)):
    return get_themes_by_subject(subject_id, session=db)

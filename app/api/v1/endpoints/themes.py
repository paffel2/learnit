from typing import List
from fastapi import Depends, APIRouter
from app.queries.themes import get_themes_by_subject
from app.schemas.theme import Theme as ThemeSchema
from app.config.database import get_db
from sqlalchemy.orm import Session
from app.utils.users import get_current_user

router = APIRouter(
    prefix="/subjects",
    tags=["subjects"],
)


@router.get("/{subject_id}/themes", response_model=List[ThemeSchema])
async def get_themes(
    subject_id: int, db: Session = Depends(get_db), user_id=Depends(get_current_user)
):
    return get_themes_by_subject(subject_id, user_id, session=db)


@router.post("/{subject_id}/themes", response_model=ThemeSchema)
async def create_theme(
    subject_id: int,
    theme: ThemeSchema,
    db: Session = Depends(get_db),
    user_id=Depends(get_current_user),
):

    return


@router.get("/{subject_id}/themes/{theme_id}", response_model=ThemeSchema)
async def get_theme(
    subject_id: int,
    theme_id: int,
    db: Session = Depends(get_db),
    user_id=Depends(get_current_user),
):

    return


@router.put("/{subject_id}/themes/{theme_id}", response_model=ThemeSchema)
async def update_theme(
    subject_id: int,
    theme_id: int,
    theme: ThemeSchema,
    db: Session = Depends(get_db),
    user_id=Depends(get_current_user),
):

    return


@router.delete("/{subject_id}/themes/{theme_id}")
async def delete_theme(
    subject_id: int,
    theme_id: int,
    db: Session = Depends(get_db),
    user_id=Depends(get_current_user),
):

    return


@router.patch("/{subject_id}/themes/{theme_id}", response_model=ThemeSchema)
async def patch_theme(
    subject_id: int,
    theme_id: int,
    theme: ThemeSchema,
    db: Session = Depends(get_db),
    user_id=Depends(get_current_user),
):

    return

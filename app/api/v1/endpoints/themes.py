from typing import List
from fastapi import Depends, APIRouter
from app.queries.themes import (
    get_themes_by_subject,
    create_theme_in_db,
    get_theme_detail,
    full_update_theme,
    delete_theme_from_db,
    partial_update_theme,
)
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
    return create_theme_in_db(
        name=theme.name, user_id=user_id, subject_id=subject_id, session=db
    )


@router.get("/{subject_id}/themes/{theme_id}", response_model=ThemeSchema)
async def get_theme(
    subject_id: int,
    theme_id: int,
    db: Session = Depends(get_db),
    user_id=Depends(get_current_user),
):

    return get_theme_detail(subject_id, user_id, theme_id, session=db)


@router.put("/{subject_id}/themes/{theme_id}", response_model=ThemeSchema)
async def update_theme(
    subject_id: int,
    theme_id: int,
    theme: ThemeSchema,
    session: Session = Depends(get_db),
    user_id=Depends(get_current_user),
):

    return full_update_theme(
        theme_id=theme_id,
        subject_id=subject_id,
        user_id=user_id,
        name=theme.name,
        order=theme.order,
        session=session,
    )


@router.delete("/{subject_id}/themes/{theme_id}")
async def delete_theme(
    subject_id: int,
    theme_id: int,
    db: Session = Depends(get_db),
    user_id=Depends(get_current_user),
):

    return delete_theme_from_db(subject_id, theme_id, user_id, session=db)


@router.patch("/{subject_id}/themes/{theme_id}", response_model=ThemeSchema)
async def patch_theme(
    subject_id: int,
    theme_id: int,
    theme: ThemeSchema,
    db: Session = Depends(get_db),
    user_id=Depends(get_current_user),
):

    return partial_update_theme(
        subject_id=subject_id,
        theme_id=theme_id,
        user_id=user_id,
        name=theme.name,
        order=theme.order,
        session=db,
    )

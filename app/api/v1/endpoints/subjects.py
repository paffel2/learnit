from typing import List
from fastapi import HTTPException, Depends, APIRouter
from app.queries.subjects import (
    get_subjects,
    create_subject_in_db,
    get_subject_detail,
    fuLL_update_subject,
    delete_subject_from_db,
    partial_update_subject,
)
from app.schemas.subject import (
    SubjectDetail,
    SubjectCreate,
    SubjectPartialUpdate,
    SubjectUpdate,
)
from app.config.database import get_db
from sqlalchemy.orm import Session
from app.utils.users import get_current_user

router = APIRouter(
    prefix="/subjects",
    tags=["subjects"],
)

PAGE_SIZE = 10


@router.get("/", response_model=List[SubjectDetail])
async def list_subjects(
    page: int = 1,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    return get_subjects(session=db, user_id=user_id, page=page, page_size=PAGE_SIZE)


@router.post("/", response_model=SubjectDetail)
async def create_subject(
    subject: SubjectCreate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_subject_in_db(name=subject.name, user_id=user_id, session=db)


@router.get("/{subject_id}", response_model=SubjectDetail)
async def get_subject(
    subject_id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    subject = get_subject_detail(subject_id=subject_id, user_id=user_id, session=db)
    if subject:
        return subject
    else:
        raise HTTPException(status_code=404, detail="Subject not found")


@router.put("/{subject_id}", response_model=SubjectDetail)
async def update_subject(
    subject_id: int,
    subject: SubjectUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    return fuLL_update_subject(
        subject_id=subject_id,
        user_id=user_id,
        name=subject.name,
        order=subject.order,
        session=db,
    )


@router.delete("/{subject_id}")
async def delete_subject(
    subject_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    return delete_subject_from_db(subject_id=subject_id, user_id=user_id, session=db)


@router.patch("/{subject_id}")
async def patch_subject(
    subject_id: int,
    subject: SubjectPartialUpdate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    return partial_update_subject(
        subject_id=subject_id,
        user_id=user_id,
        name=subject.name,
        order=subject.order,
        session=db,
    )

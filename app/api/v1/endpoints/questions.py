from typing import List
from fastapi import Depends, APIRouter
from app.queries.questions import (
    get_questions_by_subject_and_themes,
    create_question_in_db,
    get_question_detail,
    full_update_question,
    delete_question_from_db,
    partial_update_question,
)
from app.schemas.question import (
    QuestionListSchema,
    QuestionSchema,
    QuestionCreateSchema,
    QuestionPartialUpdateSchema,
)
from app.config.database import get_db
from sqlalchemy.orm import Session
from app.utils.users import get_current_user

router = APIRouter(
    prefix="/questions",
    tags=["questions"],
)


@router.get(
    "/{subject_id}/themes/{theme_id}/questions", response_model=List[QuestionListSchema]
)
async def get_questions(
    subject_id: int,
    theme_id: int,
    db: Session = Depends(get_db),
    user_id=Depends(get_current_user),
):
    return get_questions_by_subject_and_themes(
        subject_id, user_id, theme_id, session=db
    )


@router.post("/{subject_id}/themes/{theme_id}/questions", response_model=QuestionSchema)
async def create_question(
    subject_id: int,
    theme_id: int,
    question: QuestionCreateSchema,
    db: Session = Depends(get_db),
    user_id=Depends(get_current_user),
):
    return create_question_in_db(
        name=question.name,
        text=question.text,
        content=question.content,
        user_id=user_id,
        subject_id=subject_id,
        theme_id=theme_id,
        session=db,
    )


@router.get(
    "/{subject_id}/themes/{theme_id}/questions/{question_id}",
    response_model=QuestionSchema,
)
async def get_question(
    subject_id: int,
    theme_id: int,
    question_id: int,
    db: Session = Depends(get_db),
    user_id=Depends(get_current_user),
):

    return get_question_detail(subject_id, user_id, theme_id, question_id, session=db)


@router.put(
    "/{subject_id}/themes/{theme_id}/questions/{question_id}",
    response_model=QuestionSchema,
)
async def update_question(
    subject_id: int,
    theme_id: int,
    question_id: int,
    question: QuestionCreateSchema,
    session: Session = Depends(get_db),
    user_id=Depends(get_current_user),
):

    return full_update_question(
        theme_id=theme_id,
        subject_id=subject_id,
        question_id=question_id,
        user_id=user_id,
        name=question.name,
        order=question.order,
        text=question.text,
        content=question.content,
        session=session,
    )


@router.delete("/{subject_id}/themes/{theme_id}/questions/{question_id}")
async def delete_question(
    subject_id: int,
    theme_id: int,
    question_id: int,
    db: Session = Depends(get_db),
    user_id=Depends(get_current_user),
):

    return delete_question_from_db(
        subject_id, theme_id, question_id, user_id, session=db
    )


@router.patch(
    "/{subject_id}/themes/{theme_id}/questions/{question_id}",
    response_model=QuestionSchema,
)
async def patch_theme(
    subject_id: int,
    theme_id: int,
    question_id: int,
    question: QuestionPartialUpdateSchema,
    db: Session = Depends(get_db),
    user_id=Depends(get_current_user),
):

    return partial_update_question(
        subject_id=subject_id,
        theme_id=theme_id,
        user_id=user_id,
        question_id=question_id,
        name=question.name,
        order=question.order,
        text=question.text,
        content=question.content,
        session=db,
    )

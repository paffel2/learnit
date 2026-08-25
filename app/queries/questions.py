from sqlalchemy.orm import Session
from app.models.theme import Theme
from app.models.subject import Subject
from app.models.question import Question
from sqlalchemy import update as sa_update


def get_questions_by_subject_and_themes(
    subject_id: int, user_id: int, theme_id, session: Session
):
    return (
        session.query(Question)
        .join(Subject, Question.subject_id == Subject.id)
        .join(Theme, Question.theme_id == Theme.id)
        .filter(
            Question.subject_id == subject_id,
            Question.theme_id == theme_id,
            Subject.user_id == user_id,
        )
        .all()
    )


def create_question_in_db(
    user_id: int,
    subject_id: int,
    theme_id: int,
    session: Session,
    name: str,
    text: str,
    content,
) -> Question:

    last_question = (
        session.query(Question)
        .join(Subject, Question.subject_id == Subject.id)
        .join(Theme, Question.theme_id == Theme.id)
        .filter(
            Question.subject_id == subject_id,
            Question.theme_id == theme_id,
            Subject.user_id == user_id,
        )
        .order_by(Question.order.desc())
        .first()
    )

    order = 0
    if last_question:
        order = last_question.order + 1
    question = Question(
        name=name,
        text=text,
        content=content,
        theme_id=theme_id,
        subject_id=subject_id,
        order=order,
    )
    session.add(question)
    session.commit()
    session.refresh(question)
    return question


def get_question_detail(
    subject_id: int, user_id: int, theme_id: int, question_id: int, session: Session
) -> Question:
    return (
        session.query(Question)
        .join(Subject, Question.subject_id == Subject.id)
        .join(Theme, Question.theme_id == Theme.id)
        .filter(
            Question.subject_id == subject_id,
            Subject.user_id == user_id,
            Question.theme_id == theme_id,
            Question.id == question_id,
        )
        .first()
    )


def full_update_question(
    theme_id: int,
    subject_id: int,
    question_id: int,
    user_id: int,
    name: str,
    text: str,
    content,
    order: int,
    session: Session,
):
    query = (
        (
            sa_update(Question).where(
                Question.theme_id == theme_id,
                Question.subject_id == subject_id,
                Question.subject.has(Subject.user_id == user_id),
                Question.id == question_id,
            )
        )
        .values(
            name=name,
            order=order,
            subject_id=subject_id,
            text=text,
            content=content,
            theme_id=theme_id,
        )
        .returning(Question)
    )

    result = session.execute(query).scalar_one()
    session.commit()
    return result


def delete_question_from_db(
    subject_id: int, theme_id: int, question_id: int, user_id: int, session: Session
):
    return (
        session.query(Question)
        .join(Subject, Question.subject_id == Subject.id)
        .join(Theme, Question.theme_id == theme_id)
        .filter(
            Question.subject_id == subject_id,
            Subject.user_id == user_id,
            Question.theme_id == theme_id,
            Question.id == question_id,
        )
        .update({"is_deleted": True})
    )


def partial_update_question(
    subject_id: int | None,
    theme_id: int | None,
    user_id: int,
    question_id: int,
    name: str | None,
    order: int | None,
    text: str | None,
    content: str | None,
    session: Session,
):
    query = sa_update(Question).where(
        Question.id == question_id,
        Question.theme_id == theme_id,
        Question.subject_id == subject_id,
        Question.subject.has(Subject.user_id == user_id),
    )

    if name is not None:
        query = query.values(name=name)
    if order is not None:
        query = query.values(order=order)
    if subject_id is not None:
        query = query.values(subject_id=subject_id)
    if text is not None:
        query = query.values(text=text)
    if content is not None:
        query = query.values(content=content)
    if theme_id is not None:
        query = query.values(theme_id=theme_id)
    query = query.returning(Theme)

    result = session.execute(query).scalar_one()
    session.commit()
    return result

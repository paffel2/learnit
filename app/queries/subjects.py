from sqlalchemy.orm import Session
from app.models.subject import Subject
from sqlalchemy import update as sa_update


def get_subjects(page: int, user_id: int, page_size: int, session: Session):
    offset = (page - 1) * page_size
    return (
        session.query(Subject)
        .filter_by(user_id=user_id, is_deleted=False)
        .order_by(Subject.order)
        .limit(page_size)
        .offset(offset)
        .all()
    )


def create_subject_in_db(name: str, user_id: int, session: Session) -> Subject:

    last_subject = (
        session.query(Subject)
        .filter_by(user_id=user_id)
        .order_by(Subject.order.desc())
        .first()
    )
    order = 0
    if last_subject:
        order = last_subject.order + 1
    subject = Subject(name=name, user_id=user_id, order=order)
    session.add(subject)
    session.commit()
    session.refresh(subject)
    return subject


def get_subject_detail(subject_id: int, user_id: int, session: Session) -> Subject:
    return session.query(Subject).filter_by(id=subject_id, user_id=user_id).first()


def full_update_subject(
    subject_id: int, user_id: int, name: str, order: int, session: Session
):
    query = (
        (sa_update(Subject).where(Subject.id == subject_id, Subject.user_id == user_id))
        .values(name=name, order=order)
        .returning(Subject)
    )

    result = session.execute(query).scalar_one()
    session.commit()
    return result


def delete_subject_from_db(subject_id: int, user_id: int, session: Session) -> Subject:
    return (
        session.query(Subject)
        .filter_by(id=subject_id, user_id=user_id)
        .update({"is_deleted": True})
    )


def partial_update_subject(
    subject_id: int, user_id: int, name: str | None, order: int | None, session: Session
):
    query = sa_update(Subject).where(
        Subject.id == subject_id, Subject.user_id == user_id
    )

    if name is not None:
        query = query.values(name=name)
    if order is not None:
        query = query.values(order=order)

    query = query.returning(Subject)

    result = session.execute(query).scalar_one()
    session.commit()
    return result

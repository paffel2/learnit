from sqlalchemy.orm import Session
from app.models.subject import Subject


def get_subjects(page: int, user_id: int, page_size: int, session: Session):
    offset = (page - 1) * page_size
    return (
        session.query(Subject)
        .filter_by(user_id=user_id)
        .order_by(Subject.order)
        .limit(page_size)
        .offset(offset)
        .all()
    )

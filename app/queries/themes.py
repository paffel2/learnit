from sqlalchemy.orm import Session
from app.models.theme import Theme


def get_themes_by_subject(subject_id: int, session: Session):
    return session.query(Theme).filter_by(subject_id=subject_id).all()

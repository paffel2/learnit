from sqlalchemy.orm import Session
from app.models.theme import Theme
from app.models.subject import Subject


def get_themes_by_subject(subject_id: int, user_id: int, session: Session):
    return (
        session.query(Theme)
        .join(Subject, Theme.subject_id == Subject.id)
        .filter(
            Theme.subject_id == subject_id,
            Subject.user_id == user_id,
        )
        .all()
    )

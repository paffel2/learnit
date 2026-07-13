from sqlalchemy.orm import Session
from app.models.theme import Theme
from app.models.subject import Subject
from sqlalchemy import update as sa_update


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


def create_theme_in_db(
    name: str, user_id: int, subject_id: int, session: Session
) -> Theme:

    last_theme = (
        session.query(Theme)
        .join(Subject, Theme.subject_id == Subject.id)
        .filter(Theme.subject_id == subject_id, Subject.user_id == user_id)
        .order_by(Theme.order.desc())
        .first()
    )
    order = 0
    if last_theme:
        order = last_theme.order + 1
    theme = Theme(name=name, user_id=user_id, subject_id=subject_id, order=order)
    session.add(theme)
    session.commit()
    session.refresh(theme)
    return theme


def get_theme_detail(
    subject_id: int, user_id: int, theme_id: int, session: Session
) -> Theme:
    return (
        session.query(Theme)
        .join(Subject, Theme.subject_id == Subject.id)
        .filter(
            Theme.subject_id == subject_id,
            Subject.user_id == user_id,
            Theme.id == theme_id,
        )
        .first()
    )


def full_update_theme(
    theme_id: int,
    subject_id: int,
    user_id: int,
    name: str,
    order: int,
    session: Session,
):
    query = (
        (
            sa_update(Theme).where(
                Theme.id == theme_id,
                Theme.subject_id == subject_id,
                Theme.subject.has(Subject.user_id == user_id),
            )
        )
        .values(name=name, order=order, subject_id=subject_id)
        .returning(Theme)
    )

    result = session.execute(query).scalar_one()
    session.commit()
    return result


def delete_theme_from_db(
    subject_id: int, theme_id: int, user_id: int, session: Session
) -> Subject:
    return (
        session.query(Theme)
        .join(Subject, Theme.subject_id == Subject.id)
        .filter(
            Theme.subject_id == subject_id,
            Subject.user_id == user_id,
            Theme.id == theme_id,
        )
        .update({"is_deleted": True})
    )


def partial_update_theme(
    subject_id: int | None,
    theme_id: int,
    user_id: int,
    name: str | None,
    order: int | None,
    session: Session,
):
    query = sa_update(Theme).where(
        Theme.id == theme_id,
        Theme.subject_id == subject_id,
        Theme.subject.has(Subject.user_id == user_id),
    )

    if name is not None:
        query = query.values(name=name)
    if order is not None:
        query = query.values(order=order)
    if subject_id is not None:
        query = query.values(subject_id=subject_id)

    query = query.returning(Theme)

    result = session.execute(query).scalar_one()
    session.commit()
    return result

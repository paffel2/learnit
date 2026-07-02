from sqlalchemy.orm import Session
from app.models.user import User
from sqlalchemy import or_


def create_user(
    username: str, email: str, hashed_password: str, session: Session
) -> User:
    existed_user = (
        session.query(User)
        .filter(or_(User.username == username, User.email == email))
        .first()
    )
    if existed_user:
        raise Exception("User already exists")
    user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        is_active=True,
        is_deleted=False,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user.id

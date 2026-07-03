from sqlalchemy.orm import Session
from app.models.user import User
from app.queries.users import create_user as create_user_in_db
from app.queries.users import (
    get_user_by_email_and_password,
    get_user_by_username_and_password,
)
from app.schemas.user import UserCreate, UserToken, UserLogin
from app.schemas.error import ErrorResponse
from app.config.config import settings
from cryptography.fernet import Fernet
import hashlib
import base64
import jwt


def hash_password(password):
    secret = settings.SECRET_KEY
    hash_bytes = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), secret.encode(), 100000
    )
    return base64.b64encode(hash_bytes).decode("utf-8")


def create_user(user_data: UserCreate, session: Session) -> User:
    if user_data.password != user_data.repeated_password:
        return 400, ErrorResponse(detail="Passwords don't match")
    try:
        hashed_password = hash_password(user_data.password)
        return 201, create_user_in_db(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            session=session,
        )
    except Exception as e:
        return 400, ErrorResponse(detail=str(e))


def auth(user_data: UserLogin, session: Session):
    user = None
    hashed_password = hash_password(user_data.password)
    if user_data.email:
        user = get_user_by_email_and_password(
            email=user_data.email, hashed_password=hashed_password, session=session
        )
    elif user_data.username:
        user = get_user_by_username_and_password(
            username=user_data.username,
            hashed_password=hashed_password,
            session=session,
        )
    if user:
        token = create_jwt_token(user.id)
        return 201, UserToken(token=token)
    else:
        return 404, ErrorResponse(detail="Not found")


def create_jwt_token(user_id: int):
    return jwt.encode({"user_id": user_id}, settings.SECRET_KEY, algorithm="HS256")

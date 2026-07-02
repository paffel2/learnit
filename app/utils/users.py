from sqlalchemy.orm import Session
from app.models.user import User
from app.queries.users import create_user as create_user_in_db
from app.schemas.user import UserCreate
from app.schemas.error import ErrorResponse
from app.config.config import settings
from cryptography.fernet import Fernet
import hashlib
import base64


def get_cipher():
    # Преобразуем любой секрет в ключ Fernet
    key = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
    key = base64.urlsafe_b64encode(key)
    return Fernet(key)


def create_user(user_data: UserCreate, session: Session) -> User:
    if user_data.password != user_data.repeated_password:
        return 400, ErrorResponse(detail="Passwords don't match")
    try:
        cipher = get_cipher()
        hashed_password = cipher.encrypt(user_data.password.encode()).decode()
        return 201, create_user_in_db(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            session=session,
        )
    except Exception as e:
        return 400, ErrorResponse(detail=str(e))

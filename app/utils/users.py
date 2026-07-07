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
import hashlib
import base64
import jwt
import datetime
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends


def hash_password(password):
    secret = settings.PASSWORD_SECRET_KEY
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
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        return 201, UserToken(token=access_token), refresh_token
    else:
        return 404, ErrorResponse(detail="Not found"), None


def refresh_access_token(refresh_token: str):
    token_info = jwt.decode(
        refresh_token, settings.REFRESH_SECRET_KEY, algorithms=["HS256"]
    )
    access_token = create_access_token(token_info["user_id"])
    now = datetime.datetime.now().timestamp()
    exp_date = token_info["exp"]
    if exp_date < now:
        return 401, ErrorResponse(detail="Refresh token expired"), None
    # TODO сделать запись refresh токена в redis
    return 201, UserToken(token=access_token)


def create_access_token(user_id: int):
    return create_jwt_token(user_id, settings.ACCESS_SECRET_KEY)


def create_refresh_token(user_id: int):
    return create_jwt_token(user_id, settings.REFRESH_SECRET_KEY, 60 * 60 * 24)


def create_jwt_token(user_id: int, secret_key, exp=900):
    now = datetime.datetime.now()
    exp = now + datetime.timedelta(seconds=exp)
    return jwt.encode(
        {
            "user_id": user_id,
            "exp": exp,
        },
        secret_key,
        algorithm="HS256",
    )


security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    return jwt.decode(token, settings.ACCESS_SECRET_KEY, algorithms=["HS256"]).get(
        "user_id"
    )

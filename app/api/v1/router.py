from fastapi import APIRouter
from app import api
from app.api.v1.endpoints import themes, users, subjects

api_router = APIRouter()
api_router.include_router(users.router, tags=["users"])
api_router.include_router(themes.router, tags=["subjects"])
api_router.include_router(subjects.router, tags=["subjects"])

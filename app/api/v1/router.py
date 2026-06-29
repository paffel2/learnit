from fastapi import APIRouter
from app.api.v1.endpoints import themes

api_router = APIRouter()
# api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(themes.router, prefix="/subjects", tags=["subjects"])

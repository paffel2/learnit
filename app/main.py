from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.config.config import settings
from app.config.database import engine
from sqladmin import Admin
from app.admin import admin_models
from app.admin.auth import AdminAuth

app = FastAPI(title=settings.PROJECT_NAME)
authentication_backend = AdminAuth(secret_key="...")
admin = Admin(app, engine=engine, authentication_backend=authentication_backend)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",  # Если используете стандартный порт Vite
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
for model in admin_models:
    admin.add_view(model)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

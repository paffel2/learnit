from fastapi import FastAPI
from app.api.v1.router import api_router
from app.config.config import settings
from app.config.database import engine
from sqladmin import Admin
from app.admin import admin_models

app = FastAPI(title=settings.PROJECT_NAME)
admin = Admin(app, engine=engine)

for model in admin_models:
    admin.add_view(model)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "LearnIt"
    DATABASE_URL: str
    SECRET_KEY: str = "secret"

    class Config:
        env_file = ".env"


settings = Settings()

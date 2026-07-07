from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "LearnIt"
    DATABASE_URL: str
    ACCESS_SECRET_KEY: str = "access_secret"
    REFRESH_SECRET_KEY: str = "refresh_secret"
    PASSWORD_SECRET_KEY: str = "secret"

    class Config:
        env_file = ".env"


settings = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    SECRET_KEY: str = "change_me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DEBUG: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

settings = Settings()

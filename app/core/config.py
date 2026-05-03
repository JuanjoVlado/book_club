from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # App
    APP_NAME: str = "Book Club MS"
    DEBUG: bool = False

    DB_HOST: str | None = None
    DB_PORT: int | None = None
    DB_USERNAME: str | None = None
    DB_PASSWORD: str | None = None
    DB_DBNAME: str | None = None
    DATABASE_URL: str | None = None

    # Celery
    CELERY_REDIS_URL: str | None = "redis://redis:6379"

    @property
    def db_connection_str(self):
        if self.DATABASE_URL:
            return self.DATABASE_URL
        
        if not all([self.DB_HOST, self.DB_PORT, self.DB_USERNAME, self.DB_PASSWORD, self.DB_DBNAME]):
            raise ValueError("Unable to build a valid connection string, at least one require value is missing.")
        
        return f"postgresql://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DBNAME}"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()

class TestSettings(Settings):
    DEV_DB_HOST: str | None = None
    DEV_DB_PORT: int | None = None
    DEV_DB_USERNAME: str | None = None
    DEV_DB_PASSWORD: str | None = None
    DEV_DB_DBNAME: str | None = None

    @property
    def dev_db_connection_str(self):
        if not all([self.DEV_DB_HOST, self.DEV_DB_PORT, self.DEV_DB_USERNAME, self.DEV_DB_PASSWORD, self.DEV_DB_DBNAME]):
            raise ValueError("Unable to build a valid connection string, at least one require value is missing.")
        
        return f"postgresql://{self.DEV_DB_USERNAME}:{self.DEV_DB_PASSWORD}@{self.DEV_DB_HOST}:{self.DEV_DB_PORT}/{self.DEV_DB_DBNAME}"

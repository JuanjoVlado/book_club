from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # App
    APP_NAME: str = "Book Club MS"
    DEBUG: bool = False

    DB_HOST: str
    DB_PORT: int
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_DBNAME: str

    DEV_DB_HOST: str
    DEV_DB_PORT: int
    DEV_DB_USERNAME: str
    DEV_DB_PASSWORD: str
    DEV_DB_DBNAME: str

    @property
    def db_connection_str(self):
        return f"postgresql://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DBNAME}"
        
    @property
    def dev_db_connection_str(self):
        return f"postgresql://{self.DEV_DB_USERNAME}:{self.DEV_DB_PASSWORD}@{self.DEV_DB_HOST}:{self.DEV_DB_PORT}/{self.DEV_DB_DBNAME}"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

settings = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseSettings(BaseSettings):
    db_host: str
    db_port: int
    db_username: str
    db_password: str
    db_dbname: str

    @property
    def db_connection_str(self):
        return f"postgresql://{self.db_username}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_dbname}"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  # Ignore additional variables in .env
    )

database_settings = DatabaseSettings()

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    azure_storage_connection_string: str = ""
    azure_container_name: str = ""

    pg_host: str = "localhost"
    pg_port: int = 5432
    pg_username: str = "postgres"
    pg_password: str = "postgres"
    pg_db_name: str = "postgres"
    pg_db_driver: str = "postgresql"

    redis_url: str = "redis://localhost:6379"
    redis_ttl: int = 60

    sentry_dsn: str | None = None
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    @property
    def postgres(self):
        return (
            f"{self.pg_db_driver}+asyncpg://{self.pg_username}:{self.pg_password}@"
            f"{self.pg_host}:{self.pg_port}/{self.pg_db_name}"
        )

    @property
    def postgres_sync(self):
        return (
            f"postgresql://{self.pg_username}:{self.pg_password}@"
            f"{self.pg_host}:{self.pg_port}/{self.pg_db_name}"
        )


settings = Settings()
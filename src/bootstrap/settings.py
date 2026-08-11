from pydantic_settings import BaseSettings, SettingsConfigDict


class PgSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".dev.env",
        env_nested_delimiter="__",
        extra="ignore",
    )

    host: str = "localhost"
    port: int = 5432
    db: str = "project_name"
    user: str = "project_name"
    password: str = "project_name"

    @property
    def sqlalchemy_url(self) -> str:
        return (
            "postgresql+asyncpg://"
            f"{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
        )


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".dev.env",
        env_prefix="redis__",
        extra="ignore",
    )

    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: str | None = None


class RmqSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".dev.env",
        env_prefix="rmq__",
        extra="ignore",
    )

    rabbit_broker_url: str = "amqp://guest:guest@localhost:5672/"


class MinioSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".dev.env",
        env_prefix="minio__",
        extra="ignore",
    )

    endpoint_url: str = "http://localhost:9000"
    aws_access_key_id: str = "minioadmin"
    aws_secret_access_key: str = "minioadmin"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".dev.env",
        env_nested_delimiter="__",
        extra="ignore",
    )

    pg: PgSettings = PgSettings()
    redis: RedisSettings = RedisSettings()
    rmq: RmqSettings = RmqSettings()
    minio: MinioSettings = MinioSettings()

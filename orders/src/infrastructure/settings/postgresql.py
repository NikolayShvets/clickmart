from functools import cached_property, lru_cache

from pydantic import PostgresDsn, SecretStr

from infrastructure.settings.base import Settings


class PostgreSQLSettings(Settings):
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: SecretStr = SecretStr("postgres")
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "postgres"

    @cached_property
    def dsn(self) -> str:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD.get_secret_value(),
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        ).unicode_string()


@lru_cache(maxsize=1)
def get_settings() -> PostgreSQLSettings:
    return PostgreSQLSettings()

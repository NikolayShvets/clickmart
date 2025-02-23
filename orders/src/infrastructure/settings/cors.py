from functools import lru_cache

from infrastructure.settings.base import Settings


class CORSSettings(Settings):
    CORS_ALLOW_ORIGINS: list[str] = ["http://localhost:8000"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_HEADERS: list[str] = ["*"]


@lru_cache(maxsize=1)
def get_settings() -> CORSSettings:
    return CORSSettings()

from infrastructure.configs.base import Settings


class CORSConfig(Settings):
    CORS_ALLOW_ORIGINS: list[str] = ["http://localhost:8000"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_HEADERS: list[str] = ["*"]


settings = CORSConfig()

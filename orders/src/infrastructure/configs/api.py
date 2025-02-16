from infrastructure.configs.base import Settings


class ApiSettings(Settings):
    ROOT_PATH: str = "/orders"
    TITLE: str = "Orders API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "API для управления заказами"
    OPENAPI_URL: str = "/openapi.json"
    REDOC_URL: str = "/redoc"
    DOCS_URL: str = "/docs"
    CORS_ALLOW_ORIGINS: list[str] = ["*"]


settings = ApiSettings()

from dishka import make_async_container
from dishka.integrations.litestar import setup_dishka
from litestar import Litestar, Router
from litestar.config.cors import CORSConfig
from litestar.openapi.config import OpenAPIConfig

from infrastructure.configs.api import settings as api_settings
from infrastructure.configs.cors import settings as cors_settings
from infrastructure.ioc import IoC


def create_app(route_handlers: list[Router]) -> Litestar:
    container = make_async_container(IoC())

    app = Litestar(
        route_handlers=route_handlers,
        openapi_config=OpenAPIConfig(
            title=api_settings.TITLE,
            version=api_settings.VERSION,
            description=api_settings.DESCRIPTION,
            path=api_settings.ROOT_PATH,
        ),
        cors_config=CORSConfig(
            allow_origins=cors_settings.CORS_ALLOW_ORIGINS,
            allow_credentials=cors_settings.CORS_ALLOW_CREDENTIALS,
            allow_methods=["*"],
            allow_headers=cors_settings.CORS_ALLOW_HEADERS,
        ),
        debug=True,
    )

    setup_dishka(container, app)

    return app

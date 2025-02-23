from litestar import Litestar

from infrastructure.litestar import create_app
from infrastructure.settings.api import get_settings as get_api_settings
from infrastructure.settings.cors import get_settings as get_cors_settings
from presentation.api.v1 import v1_router


def get_app() -> Litestar:
    api_settings = get_api_settings()
    cors_settings = get_cors_settings()

    return create_app(api_settings, cors_settings, [v1_router])

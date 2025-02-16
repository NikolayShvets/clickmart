from litestar import Litestar

from infrastructure.litestar import create_app
from presentation.api.v1 import v1_router


def get_app() -> Litestar:
    return create_app([v1_router])

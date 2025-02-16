from litestar import Router

from presentation.api.v1.routers import order_router

router = Router(
    path="/api/v1",
    route_handlers=[order_router],
)

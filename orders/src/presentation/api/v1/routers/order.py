from dishka.integrations.litestar import FromDishka as Depends
from dishka.integrations.litestar import inject
from litestar import Controller, Router, post

from application.dto import CreateOrderDTO, OrderItemDTO
from application.use_cases import CreateOrderUseCase
from domain.value_objects import SKU
from presentation.api.v1.schemas import (
    OrderCreateSchema,
    OrderItemBaseSchema,
    OrderRetrieveSchema,
)


class OrderController(Controller):
    # TODO: тут из каллорий только use_case.execute, остальное - создание DTO и схем
    # как сделать лучше?
    @post("/")
    @inject
    async def create(
        self,
        data: OrderCreateSchema,
        use_case: Depends[CreateOrderUseCase],
    ) -> OrderRetrieveSchema:
        dto = CreateOrderDTO(
            customer_id=data.customer_id,
            items=[
                OrderItemDTO(
                    product_sku=SKU(item.product_sku),
                    quantity=item.quantity,
                )
                for item in data.items
            ],
        )
        created = await use_case.execute(dto)

        return OrderRetrieveSchema(
            number=str(created.number),
            customer_id=created.customer_id,
            status=created.status,
            items=[
                OrderItemBaseSchema(
                    product_sku=str(item.product.sku),
                    quantity=item.quantity,
                )
                for item in created.items
            ],
        )


router = Router(
    path="/orders",
    route_handlers=[OrderController],
)

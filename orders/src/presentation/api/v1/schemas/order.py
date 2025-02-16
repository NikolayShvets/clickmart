import msgspec

from domain.entities.order import OrderStatus


class OrderItemBaseSchema(msgspec.Struct):
    product_sku: str
    quantity: int


class OrderBaseSchema(msgspec.Struct):
    customer_id: str
    items: list[OrderItemBaseSchema]


class OrderCreateSchema(OrderBaseSchema): ...


class OrderUpdateSchema(OrderBaseSchema): ...


class OrderRetrieveSchema(OrderBaseSchema):
    number: str
    status: OrderStatus

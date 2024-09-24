from datetime import datetime

from pydantic import BaseModel


class OrderItemSchema(BaseModel):
    product_id: int
    product_quantity: int


class OrderCreateSchema(BaseModel):
    order_items: list[OrderItemSchema]


class StatusSchema(BaseModel):
    id: int
    name: str


class OrderSchema(OrderCreateSchema):
    id: int
    created_at: datetime
    status: StatusSchema

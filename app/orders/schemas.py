from datetime import datetime

from pydantic import BaseModel


class StatusSchema(BaseModel):
    id: int
    name: str


class OrderItemSchema(BaseModel):
    product_id: int
    product_quantity: int

class OrderCreateSchema(BaseModel):
    order_items: list[OrderItemSchema]

class OrderSchema(OrderCreateSchema):
    id: int
    created_at: datetime
    status: StatusSchema

class OrderListSchema(BaseModel):
    orders: list[OrderSchema]
